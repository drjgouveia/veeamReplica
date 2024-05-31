import os
import shutil

import pytest

from modules import syncer


def test_filesystem_001():
    """Check if the function create_filesystem_tree is outputting the right filesystem tree structure"""
    if os.path.exists("./tests/output"):
        shutil.rmtree("./tests/output")
    fs = syncer.Syncer("./tests", "./tests/output")
    assert fs.create_filesystem_tree("./tests/test_dir") == {'.gitkeep': {'md5': 'd41d8cd98f00b204e9800998ecf8427e', 'path': './tests/test_dir/.gitkeep'}}


def test_filesystem_002():
    """Check if create_filesystem_tree handles non-existing directory correctly"""
    with pytest.raises(FileNotFoundError):
        fs = syncer.Syncer("./tests", "./tests/not_exists", force_create=False)

    with pytest.raises(FileNotFoundError):
        fs = syncer.Syncer("./not_exists", "./tests/test_dir")


def test_filesystem_003():
    """Check if the function copy is copying the file correctly"""
    fs = syncer.Syncer("./tests", "./tests/output")
    fs.copy("./tests/test_file", "./tests/output/test_file")
    assert os.path.exists("./tests/output/test_file")

    os.remove("./tests/output/test_file")
