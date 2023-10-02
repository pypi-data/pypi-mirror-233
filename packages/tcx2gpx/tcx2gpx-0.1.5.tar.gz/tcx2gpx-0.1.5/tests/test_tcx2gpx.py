"""Test tcx2gpy."""
from pathlib import Path

from tcxparser import TCXParser
from gpxpy.gpx import GPX
from tcx2gpx.tcx2gpx import TCX2GPX

TCX_DIR = Path(__file__).resolve().parents[0]
GPX_FILE = TCX_DIR / "resources" / "2019-10-20 12:51:21.0.gpx"


def test_tcx2gpx_init(tcx_file: TCX2GPX) -> None:
    """Test instantiation results in the correct object type."""
    assert isinstance(tcx_file.tcx_path, Path)
    assert isinstance(tcx_file.gpx, GPX)


def test_read_tcx(tcx_file: TCX2GPX) -> None:
    """Test reading of TCX."""
    tcx_file.read_tcx()

    assert isinstance(tcx_file.tcx, TCXParser)


def test_extract_track_points(tcx_file: TCX2GPX) -> None:
    """Test reading of TCX."""
    tcx_file.read_tcx()
    tcx_file.extract_track_points()

    assert isinstance(tcx_file.track_points, zip)


def test_set_track_name(tcx_file: TCX2GPX) -> None:
    """Test extraction of start time and setting as GPX track name."""
    tcx_file.read_tcx()
    tcx_file.set_track_name()

    assert tcx_file.gpx.name == "2019-10-20T12:50:19+00:00"


def test_create_gpx(tcx_file: TCX2GPX) -> None:
    """Test creation of GPX."""
    tcx_file.read_tcx()
    tcx_file.extract_track_points()
    tcx_file.create_gpx()

    assert isinstance(tcx_file.gpx, GPX)


def test_write_gpx(tcx_file: TCX2GPX) -> None:
    """Test writing of GPX."""
    tcx_file.read_tcx()
    tcx_file.extract_track_points()
    tcx_file.create_gpx()
    tcx_file.write_gpx()

    assert GPX_FILE.exists()


def test_convert(tcx_file: TCX2GPX) -> None:
    """Test conversion wrapper."""
    tcx_file.convert()

    assert isinstance(tcx_file.track_points, zip)
    assert isinstance(tcx_file.gpx, GPX)
