"""Objectify an FMU case (results) as it appears on the disk."""

import os
from pathlib import Path
import uuid
import glob
import time
import logging
import warnings
import datetime

import yaml
import json
import pandas as pd
import hashlib
import base64

from fmu.sumo.uploader._fileondisk import FileOnDisk
from fmu.sumo.uploader._upload_files import upload_files
from fmu.dataio import ExportData
from fmu.dataio._utils import read_parameters_txt


logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)

# pylint: disable=C0103 # allow non-snake case variable names


class CaseOnDisk:
    """
    Class to hold information about an ERT run on disk.

    The CaseOnDisk object is a representation of files belonging to an FMU case,
    as they are stored on the Scratch disk.

    A Case in this context is a set of metadata describing this particular case,
    and an arbitrary number of files belonging to this case. Each file is in reality
    a file pair, consisting of a data file (could be any file type) and a metadata file
    (yaml formatted, according) to FMU standards.

    Example for initialization:
        >>> from fmu import sumo

        >>> env = 'dev'
        >>> case_metadata_path = 'path/to/case_metadata.yaml'
        >>> search_path = 'path/to/search_path/'

        >>> sumo_connection = sumo.SumoConnection(env=env)
        >>> case = sumo.CaseOnDisk(
                case_metadata_path=case_metadata_path,
                sumo_connection=sumo_connection)

        After initialization, files must be explicitly indexed into the CaseOnDisk object:

        >>> case.add_files(search_path)

        When initialized, the case can be uploaded to Sumo:

        >>> case.upload()

    Args:
        case_metadata_path (str): Path to the case_metadata file for the case
        sumo_connection (fmu.sumo.SumoConnection): SumoConnection object


    """

    def __init__(
        self, case_metadata_path: str, sumo_connection, verbosity="INFO"
    ):
        """Initialize CaseOnDisk.

        Args:
            case_metadata_path (str): Path to case_metadata for case
            sumo_connection (fmu.sumo.SumoConnection): Connection to Sumo.
            verbosity (str): Python logging level.
        """

        self.verbosity = verbosity
        logger.setLevel(level=verbosity)

        self.sumo_connection = sumo_connection

        logger.debug("case metadata path: %s", case_metadata_path)
        self._case_metadata_path = Path(case_metadata_path)
        self.case_metadata = _load_case_metadata(case_metadata_path)
        self._fmu_case_uuid = self._get_fmu_case_uuid()
        logger.debug("self._fmu_case_uuid is %s", self._fmu_case_uuid)
        self._sumo_parent_id = self._get_sumo_parent_id()
        logger.debug("self._sumo_parent_id is %s", self._sumo_parent_id)
        self._files = []

        self._sumo_logger = sumo_connection.api.getLogger("log_2_server_caseondisk")
        self._sumo_logger.setLevel(logging.INFO)
        # Avoid that logging to sumo-server also is visible in local logging:
        self._sumo_logger.propagate = False 
        self._sumo_logger.info("Upload init for sumo_parent_id: " 
                              + str(self._sumo_parent_id))

    def __str__(self):
        s = f"{self.__class__}, {len(self._files)} files."

        if self._sumo_parent_id is not None:
            s += f"\nInitialized on Sumo. Sumo_ID: {self._sumo_parent_id}"
        else:
            s += "\nNot initialized on Sumo."

        return s

    def __repr__(self):
        return str(self.__str__)

    @property
    def sumo_parent_id(self):
        """Return the sumo parent ID"""
        return self._sumo_parent_id

    @property
    def fmu_case_uuid(self):
        """Return the fmu_case_uuid"""
        return self._fmu_case_uuid

    @property
    def files(self):
        """Return the files"""
        return self._files

    def add_files(self, search_string):
        """Add files to the case, based on search string"""

        logger.info("Searching for files at %s", search_string)
        file_paths = _find_file_paths(search_string)

        for file_path in file_paths:
            try:
                file = FileOnDisk(path=file_path, verbosity=self.verbosity)
                self._files.append(file)
                logger.info("File appended: %s", file_path)

            except IOError as err:
                info = f"{err}. No metadata, skipping file."
                warnings.warn(info)

    def _get_sumo_parent_id(self):
        """Get the sumo parent ID.

        If parent id is cached on disk, use that. Else call sumo to get it based on
        fmu_case_uuid."""

        # If a relatively new cached file exists we use that and avoid calling Sumo
        cached_key = "sumo-case-id"
        cached_file = Path(
            self._case_metadata_path.parent / "sumo_parent_id.yml"
        )
        if cached_file.exists():
            file_age = (
                datetime.datetime.today()
                - datetime.datetime.fromtimestamp(cached_file.lstat().st_mtime)
            )
            if file_age.days < 1:
                logger.debug(
                    "cached sumo_parent_id is less than 1 days, using it."
                )
                with open(str(cached_file), "r") as infile:
                    filecontents = yaml.safe_load(infile)
                sumo_parent_id = filecontents.get(cached_key)
                logger.debug(
                    "Got sumo_parent_id from cache: %s", sumo_parent_id
                )
                try:
                    test_uuid = uuid.UUID(sumo_parent_id)
                    logger.debug("Getting sumo parent id from cached file")
                    return sumo_parent_id
                except ValueError:
                    pass  # Not a valid uuid, will call Sumo

        # No valid cached file, need to call Sumo to get the parent id
        query = f"class:case AND fmu.case.uuid:{self.fmu_case_uuid}"
        search_results = self.sumo_connection.api.get(
            "/search", query=query, size=2, **{"from": 0}
        )

        # To catch crazy rare situation when index is empty (first upload to new index)
        if not search_results.get("hits"):
            return None

        hits = search_results.get("hits").get("hits")

        if len(hits) == 0:
            return None

        if len(hits) == 1:
            sumo_parent_id = hits[0].get("_id")

            try:
                # Cache the parent id in a file
                my_dict = {cached_key: sumo_parent_id}
                with open(str(cached_file), "w") as outfile:
                    yaml.dump(my_dict, outfile)
                logger.debug("Caching sumo parent id")
            except:
                # Might be concurrency issues, just skip caching to file this time
                pass

            return sumo_parent_id

        raise ValueError(
            f"More than one hit for fmu.case.uuid {self.fmu_case_uuid} found on Sumo"
        )

    def register(self):
        """Register this case on Sumo.

        Assumptions: If registering an already existing case, it will be overwritten.
        ("register" might be a bad word for this...)

        Returns:
            sumo_parent_id (uuid4): Unique ID for this case on Sumo
        """

        logger.info("Registering case on Sumo")

        sumo_parent_id = self._upload_case_metadata(self.case_metadata)
        self._sumo_parent_id = sumo_parent_id

        logger.info("Case registered. SumoID: {}".format(sumo_parent_id))

        return sumo_parent_id

    def _upload_case_metadata(self, case_metadata: dict):
        """Upload case metadata to Sumo."""

        response = self.sumo_connection.api.post(
            path="/objects", json=case_metadata
        )

        returned_object_id = response.json().get("objectid")

        return returned_object_id

    def _get_fmu_case_uuid(self):
        """Return case_id from case_metadata."""

        fmu_case_uuid = self.case_metadata.get("fmu").get("case").get("uuid")

        if not fmu_case_uuid:
            raise ValueError("Could not get fmu_case_uuid from case metadata")

        return fmu_case_uuid

    def upload_parameters_txt(
        self,
        glob_var_path: str = "./fmuconfig/output/global_variables.yml",
        parameters_path: str = "./parameters.txt",
    ):
        """Upload parameters.txt if it is not present in Sumo for the current realization"""
        logger.info("Uploading parameters.txt")

        fmu_id = self.fmu_case_uuid
        realization_id = self.files[0].metadata["fmu"]["realization"]["uuid"]
        query = f"fmu.case.uuid:{fmu_id} AND fmu.realization.uuid:{realization_id} AND data.content:parameters"
        search_res = self.sumo_connection.api.get("/search", query=query)

        if search_res["hits"]["total"]["value"] == 0:
            with open(glob_var_path, "r") as variables_yml:
                global_config = yaml.safe_load(variables_yml)

            parameters = read_parameters_txt(parameters_path)

            exd = ExportData(
                config=global_config, content="parameters", name="parameters"
            )
            metadata = exd.generate_metadata(parameters)

            bytes = json.dumps(parameters).encode("utf-8")
            digester = hashlib.md5(bytes)
            md5 = base64.b64encode(digester.digest()).decode("utf-8")
            metadata["_sumo"] = {"blob_size": len(bytes), "blob_md5": md5}

            upload_res = self.sumo_connection.api.post(
                f"/objects('{fmu_id}')", json=metadata
            )
            self.sumo_connection.api.blob_client.upload_blob(
                blob=bytes, url=upload_res.json()["blob_url"]
            )
        else:
            logger.info("Parameters.txt already exists")

    def upload(self, threads=4, max_attempts=1, register_case=False):
        """Trigger upload of files.

        Get sumo_parent_id. If None, case is not registered on Sumo.

        Upload all indexed files. Collect the files that have been uploaded OK, the
        ones that have failed and the ones that have been rejected.

        Retry the failed uploads X times."""

        if self.sumo_parent_id is None:
            logger.info("Case is not registered on Sumo")

            if register_case:
                self.register()
                logger.info(
                    "Waiting 1 minute for Sumo to create the case container"
                )
                time.sleep(20)  # Wait for Sumo to create the container
            else:
                # We catch the situation where case is not registered on Sumo but
                # an upload is attempted anyway. In the FMU context, this can happen
                # if something goes wrong with the initial case metadata creation and
                # upload. If, for some reason, this fails and the case is never uploaded
                # to Sumo, we (currently) want this script to not fail (and stop the
                # workflow). Outside FMU context, this can be different and we retain
                # the possibility for allowing this script to register the case.

                logger.info(
                    "Case was not found on Sumo. If you are in the FMU context "
                    "something may have gone wrong with the case registration "
                    "or you have not specified that the case shall be uploaded."
                    "A warning will be issued, and the script will stop. "
                    "If you are NOT in the FMU context, you can specify that "
                    "this script also registers the case by passing "
                    "register=True. This should not be done in the FMU context."
                )
                warnings.warn(
                    "Case is not registered on Sumo.",
                    UserWarning,
                )
                return

        if not self.files:
            raise FileExistsError("No files to upload. Check search string.")

        ok_uploads = []
        failed_uploads = []
        rejected_uploads = []
        files_to_upload = [f for f in self.files]

        attempts = 0
        _t0 = time.perf_counter()

        logger.debug("files_to_upload: %s", files_to_upload)

        while files_to_upload and attempts < max_attempts:
            upload_results = upload_files(
                files=files_to_upload,
                sumo_parent_id=self.sumo_parent_id,
                sumo_connection=self.sumo_connection,
                threads=threads,
            )

            ok_uploads += upload_results.get("ok_uploads")
            rejected_uploads += upload_results.get("rejected_uploads")
            failed_uploads = upload_results.get("failed_uploads")

            if not failed_uploads:
                break

            files_to_upload = [f.get("file") for f in failed_uploads]

            attempts += 1

            time.sleep(3)
            logger.debug(
                "Retrying {} failed uploads after waiting 3 seconds".format(
                    len(failed_uploads)
                )
            )

        if failed_uploads:
            warnings.warn("Stopping after {} attempts".format(attempts))

        _dt = time.perf_counter() - _t0

        upload_statistics = ""
        if len(ok_uploads) > 0:
            upload_statistics = _calculate_upload_stats(ok_uploads)
            logger.info(upload_statistics)

        if rejected_uploads:
            logger.info(
                f"\n\n{len(rejected_uploads)} files rejected by Sumo. First 5 rejected files:"
            )

            for u in rejected_uploads[0:4]:
                logger.info("\n" + "=" * 50)

                logger.info(f"Filepath: {u.get('blob_file_path')}")
                logger.info(
                    f"Metadata: [{u.get('metadata_upload_response_status_code')}] "
                    f"{u.get('metadata_upload_response_text')}"
                )
                logger.info(
                    f"Blob: [{u.get('blob_upload_response_status_code')}] "
                    f"{u.get('blob_upload_response_status_text')}"
                )
                self._sumo_logger.info(_get_log_msg(self.sumo_parent_id, u))

        if failed_uploads:
            logger.info(
                f"\n\n{len(failed_uploads)} files failed by Sumo. First 5 failed files:"
            )

            for u in failed_uploads[0:4]:
                logger.info("\n" + "=" * 50)

                logger.info(f"Filepath: {u.get('blob_file_path')}")
                logger.info(
                    f"Metadata: [{u.get('metadata_upload_response_status_code')}] "
                    f"{u.get('metadata_upload_response_text')}"
                )
                logger.info(
                    f"Blob: [{u.get('blob_upload_response_status_code')}] "
                    f"{u.get('blob_upload_response_status_text')}"
                )
                self._sumo_logger.info(_get_log_msg(self.sumo_parent_id, u))

        logger.info("Summary:")
        logger.info("Total files count: %s", str(len(self.files)))
        logger.info("OK: %s", str(len(ok_uploads)))
        logger.info("Failed: %s", str(len(failed_uploads)))
        logger.info("Rejected: %s", str(len(rejected_uploads)))
        logger.info("Wall time: %s sec", str(_dt))

        summary = {
            "upload_summary": {
                "parent_id": self.sumo_parent_id,
                "total_files_count": str(len(self.files)),
                "ok_files": str(len(ok_uploads)),
                "failed_files": str(len(failed_uploads)),
                "rejected_files": str(len(rejected_uploads)),
                "wall_time_seconds": str(_dt),
                "upload_statistics": upload_statistics
            }
        }
        self._sumo_logger.info(str(summary))

        return ok_uploads

def _get_log_msg(sumo_parent_id, status):
    """Return a suitable logging for upload issues."""

    json = {
        "upload_issue": {
            "case_uuid": str(sumo_parent_id),
            "filepath": str(status.get('blob_file_path')),
            "metadata": {
                "status_code": str(status.get('metadata_upload_response_status_code')),
                "response_text": status.get('metadata_upload_response_text')
            },
            "blob": {
                "status_code": str(status.get('blob_upload_response_status_code')),
                "response_text": ((status.get('blob_upload_response_status_text')))
            }
        }
    }
    return json


def _sanitize_datetimes(data):
    """Sanitize datetimes.

    Given a dictionary, find and replace all datetime objects
    with isoformat string, so that it does not cause problems for
    JSON later on."""

    if isinstance(data, datetime.datetime):
        return data.isoformat()

    if isinstance(data, dict):
        for key in data.keys():
            data[key] = _sanitize_datetimes(data[key])

    elif isinstance(data, list):
        data = [_sanitize_datetimes(element) for element in data]

    return data


def _load_case_metadata(case_metadata_path: str):
    """Load the case metadata."""

    if not os.path.isfile(case_metadata_path):
        raise IOError(f"case metadata not found: {case_metadata_path}")

    with open(case_metadata_path, "r") as stream:
        yaml_data = yaml.safe_load(stream)

    logger.debug("Sanitizing datetimes from loaded case metadata")
    yaml_data = _sanitize_datetimes(yaml_data)

    return yaml_data


def _find_file_paths(search_string):
    """Find files and return as list of FileOnDisk instances."""

    files = [f for f in glob.glob(search_string) if os.path.isfile(f)]

    if len(files) == 0:
        info = "No files found! Please, check the search string."
        warnings.warn(info)

        info = f"Search string: {search_string}"
        warnings.warn(info)

    return files


def _calculate_upload_stats(uploads):
    """Calculate upload statistics.

    Given a list of results from file upload, calculate and return
    timing statistics for uploads."""

    df = pd.DataFrame().from_dict(uploads)

    stats = {
        "blob": {
            "upload_time": {
                "mean": df["blob_upload_time_elapsed"].mean(),
                "max": df["blob_upload_time_elapsed"].max(),
                "min": df["blob_upload_time_elapsed"].min(),
                "std": df["blob_upload_time_elapsed"].std(),
            },
        },
        "metadata": {
            "upload_time": {
                "mean": df["metadata_upload_time_elapsed"].mean(),
                "max": df["metadata_upload_time_elapsed"].max(),
                "min": df["metadata_upload_time_elapsed"].min(),
                "std": df["metadata_upload_time_elapsed"].std(),
            },
        },
    }

    return stats