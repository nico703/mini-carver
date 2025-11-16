# einfache Smoke-Tests für mini-carver
import os, tempfile
from carver import carve

def test_no_signatures(tmp_path):
    empty = b"just some text without signatures"
    outdir = tmp_path / "recovered"
    carve(empty, str(outdir))
    assert (not os.listdir(outdir)) if outdir.exists() else True
