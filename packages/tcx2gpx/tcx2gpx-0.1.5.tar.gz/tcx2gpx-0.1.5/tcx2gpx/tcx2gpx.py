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
"""Class for converting tcx to gpx."""
import logging
from datetime import datetime
from pathlib import Path

import dateutil.parser
from dateutil.parser import ParserError

from gpxpy import gpx
from tcxparser import TCXParser

# pylint: disable=logging-format-interpolation
# pylint: disable=logging-fstring-interpolation

LOGGER = logging.getLogger("tcx2gpx")


class TCX2GPX:

    """Convert tcx files to gpx."""

    def __init__(self, tcx_path: str | Path) -> None:
        """Initialise the class.

        Parameter
        ---------
        tcx_path: str
            Valid path to a TCX file.
        """
        self.tcx_path = Path(tcx_path)
        self.tcx = None
        self.track_points = None
        self.gpx = gpx.GPX()

    def convert(self) -> None:
        """Convert tcx to gpx."""
        self.read_tcx()
        self.extract_track_points()
        self.create_gpx()
        self.write_gpx()

    def read_tcx(self) -> None:
        """Read a TCX file."""
        try:
            self.tcx = TCXParser(str(self.tcx_path.resolve()))
            LOGGER.info(f"Reading                     : {self.tcx_path}")
        except TypeError as not_pathlib:
            raise TypeError("File path did not resolve.") from not_pathlib

    def extract_track_points(self) -> None:
        """Extract and combine features from tcx."""
        self.track_points = zip(self.tcx.position_values(), self.tcx.altitude_points(), self.tcx.time_values())
        LOGGER.info(f"Extracting track points from : {self.tcx_path}")

    def set_track_name(self) -> None:
        """Set the GPX trackname to the TCX Started At."""
        try:
            self.gpx.name = dateutil.parser.parse(self.tcx.started_at).isoformat()
        except ParserError as pe:  # pylint: disable=invalid-name
            raise ParserError(f"The start date/time in TCX file {self.tcx_path} is not in ISO format.") from pe

    def create_gpx(self) -> None:
        """Create GPX object."""
        self.set_track_name()
        self.gpx.description = ""
        gpx_track = gpx.GPXTrack(
            name=dateutil.parser.parse(self.tcx.started_at).isoformat(),
            description="",
        )
        gpx_track.type = self.tcx.activity_type
        self.gpx.tracks.append(gpx_track)
        gpx_segment = gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)
        for track_point in self.track_points:
            gpx_trackpoint = gpx.GPXTrackPoint(
                latitude=track_point[0][0],
                longitude=track_point[0][1],
                elevation=track_point[1],
                time=datetime.fromisoformat(track_point[2]),
            )
            gpx_segment.points.append(gpx_trackpoint)
        LOGGER.info(f"Creating GPX for             : {self.tcx_path}")

    def write_gpx(self) -> None:
        """Write GPX object to file."""
        out = Path(str(self.tcx_path.resolve()).replace(".tcx", ".gpx"))
        with out.open("w", encoding="utf8") as output:
            output.write(self.gpx.to_xml())
        LOGGER.info(f"GPX written to               : {out}")
