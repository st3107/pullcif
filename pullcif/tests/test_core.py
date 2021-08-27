import pytest

import pullcif.core as core


@pytest.mark.skip
def test_main(tmp_path):
    core.main(str(tmp_path))
    # there are files output
    fs = list(tmp_path.glob("*"))
    assert len(fs) > 0
