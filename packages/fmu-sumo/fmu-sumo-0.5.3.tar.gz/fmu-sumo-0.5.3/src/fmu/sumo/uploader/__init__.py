"""Top-level package for fmu.sumo.uploader"""

try:
    from .version import version

    __version__ = version
except ImportError:
    __version__ = "0.0.0"

from fmu.sumo.uploader.caseondisk import CaseOnDisk
from fmu.sumo.uploader.caseonjob import CaseOnJob
from fmu.sumo.uploader._connection import (
    SumoConnection,
    SumoConnectionWithOutsideToken,
)

# from fmu.sumo.uploader._fileondisk import FileOnDisk
# from fmu.sumo.uploader._fileonjob import FileOnJob
