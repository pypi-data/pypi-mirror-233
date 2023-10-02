"""Fixtures for test_tcx2gpx."""
from pathlib import Path
import pytest

from tcx2gpx.tcx2gpx import TCX2GPX

TCX_DIR = Path(__file__).resolve().parents[0]


TCX_FILE = TCX_DIR / "resources" / "2019-10-20 12:51:21.0.tcx"
TCX_MILLISECOND_FILE = TCX_DIR / "resources" / "tcx_with_milliseconds.tcx"
GPX_FILE = TCX_DIR / "resources" / "2019-10-20 12:51:21.0.gpx"


@pytest.fixture()
def tcx_file() -> TCX2GPX:
    """Fixture of TCX file."""
    return TCX2GPX(TCX_FILE)


@pytest.fixture()
def tcx_milliseconds_file() -> TCX2GPX:
    """Fixture of TCX file with miliseconds in date-time fields."""
    return TCX2GPX(TCX_MILLISECOND_FILE)
