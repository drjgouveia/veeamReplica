from modules import hashing


def test_hashing_001():
    """Check if the MD5 checksum is correct"""
    assert "098f6bcd4621d373cade4e832627b4f6" == hashing.file_md5("./tests/test_file")


def test_hashing_002():
    """Check if returns None when the user refers a non existing file"""
    assert hashing.file_md5("./tests/noexist") is None


def test_hashing_003():
    """Check if returns None when the user doesn't have permissions"""
    assert hashing.file_md5("/") is None
