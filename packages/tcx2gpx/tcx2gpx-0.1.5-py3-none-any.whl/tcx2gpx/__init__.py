"""Initialise the module."""  # noqa: D104
import sys
import logging

from importlib.metadata import version, PackageNotFoundError

# Copyright 2020 Neil Shephard
#
# This file is part of tcx2gpx.
#
# tcx2gpx is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, version 3 of the License.
#
#
# tcx2gpx is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with tcx2gpx. If not, see
# <https://www.gnu.org/licenses/>.

LOG_FORMATTER = logging.Formatter("%(asctime)s [%(levelname)s][%(name)s] %(message)s", datefmt="%Y-%m-%d %H:%MS")
LOG_ERR_FORMATTER = logging.Formatter(
    "%(asctime)s [%(levelname)s][%(name)s][%(filename)s:%(lineno)d] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
LOGGER_NAME = "tcx2gpx"

STD_OUT_STREAMHANDLER = logging.StreamHandler(sys.stdout)
STD_OUT_STREAMHANDLER.setLevel(logging.DEBUG)
STD_OUT_STREAMHANDLER.setFormatter(LOG_FORMATTER)

STD_ERR_STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STD_ERR_STREAM_HANDLER.setLevel(logging.ERROR)
STD_ERR_STREAM_HANDLER.setFormatter(LOG_ERR_FORMATTER)

try:
    __version__ = version("tcx2gpx")
except PackageNotFoundError:
    pass
