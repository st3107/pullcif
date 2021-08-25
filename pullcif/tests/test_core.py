import pytest

import pullcif.core as core
from diffpy.structure import loadStructure, Structure


@pytest.mark.skip
def test_main(tmp_path):
    core.main(str(tmp_path))
    # there are files output
    fs = list(tmp_path.glob("*"))
    assert len(fs) > 0
    # all files can be loaded by diffpy.structure
    for f in tmp_path.glob("*"):
        stru = loadStructure(str(f), fmt="cif")
        assert isinstance(stru, Structure)
