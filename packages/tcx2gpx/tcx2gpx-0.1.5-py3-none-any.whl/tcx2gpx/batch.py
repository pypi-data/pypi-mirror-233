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
"""Batch convert tcx to gpx files."""
import logging
from pathlib import Path
import argparse as arg
from multiprocessing import Pool

from tqdm import tqdm

from tcx2gpx.tcx2gpx import TCX2GPX

# pylint: disable=logging-format-interpolation

LOGGER = logging.getLogger("batch tcx2gpx")


def create_parser() -> arg:
    """Parse arguments for smooth scoring."""
    parser = arg.ArgumentParser()
    parser.add_argument(
        "-d", "--directory", default=".", help="Directory containing tcx files for conversion.", required=False
    )
    parser.add_argument("-o", "--output", default=".", help="Directory output will be written to.", required=False)
    parser.add_argument("-j", "--cores", default="4", help="Number of processors to use.", required=False)
    return parser.parse_args()


def process_tcx(file_path: str | Path) -> None:
    """Convert individual tcx files to gpx."""
    to_convert = TCX2GPX(file_path)
    to_convert.convert()


def tcx2gpx():
    """Process the batch."""
    parser = create_parser()
    tcx_dir = Path(parser.directory)
    LOGGER.info(f"Searching for files in          : {tcx_dir}")
    tcx_files = sorted(tcx_dir.glob("**/*.tcx"))

    LOGGER.info("Found {len(tcx_files)} files, processing...")
    with Pool(int(parser.cores)) as pool:
        with tqdm(total=len(tcx_files), desc=f"Found {len(tcx_files)} TCX files under {tcx_dir}") as pbar:
            for _ in pool.map(process_tcx, tcx_files):
                pbar.update()
