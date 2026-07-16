import pytest
from unittest.mock import patch

# INTENTIONAL RED PHASE
from storage_engine.file_manager.services.file_synchronizer import FileSynchronizer
from storage_engine.file_manager.entities.file_handle import FileHandle
from storage_engine.file_manager.enums.file_access_mode import FileAccessMode
from storage_engine.file_manager.enums.file_lock_mode import FileLockMode

@pytest.fixture
def synchronizer():
    return FileSynchronizer()

@pytest.fixture
def handle():
    return FileHandle(handle_id=1, file_id=99, access_mode=FileAccessMode.READ_WRITE, lock_mode=FileLockMode.NONE)

def test_ut_sync_01_valid_expansion(synchronizer, handle):
    # Given
    with patch("os.truncate") as mock_truncate:
        # When
        new_offset = synchronizer.expand_file(handle, size_bytes=4096)
        
        # Then
        mock_truncate.assert_called_once()
        assert isinstance(new_offset, int)

def test_ut_sync_02_expansion_fails(synchronizer, handle):
    # Given
    with patch("os.truncate", side_effect=OSError("Insufficient disk space")):
        # When & Then
        with pytest.raises(Exception, match="OutOfSpaceException"):
            synchronizer.expand_file(handle, size_bytes=4096)

def test_ut_sync_03_flush_dirty_buffers(synchronizer, handle):
    # Given
    with patch("os.fsync") as mock_fsync:
        # When
        synchronizer.fsync(handle)
        
        # Then
        mock_fsync.assert_called_once()
