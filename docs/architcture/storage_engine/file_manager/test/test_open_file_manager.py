import pytest
from unittest.mock import Mock

# INTENTIONAL RED PHASE: These imports will fail because the classes do not exist yet!
from storage_engine.file_manager.services.open_file_manager import OpenFileManager
from storage_engine.file_manager.entities.data_file import DataFile
from storage_engine.file_manager.enums.file_access_mode import FileAccessMode
from storage_engine.file_manager.enums.file_lock_mode import FileLockMode

@pytest.fixture
def open_file_mgr():
    # Set max_open limit to 2 for testing limit breaching
    return OpenFileManager(max_open=2)

@pytest.fixture
def mock_data_file():
    df = Mock(spec=DataFile)
    df.path = "test_db.txt"
    df.file_id = 99
    return df

def test_ut_ofm_01_fresh_registration(open_file_mgr, mock_data_file):
    # When
    handle = open_file_mgr.register(mock_data_file, FileAccessMode.READ_WRITE, FileLockMode.NONE)

    # Then
    assert handle is not None
    assert open_file_mgr.is_already_open("test_db.txt") is True

def test_ut_ofm_02_handle_limit_breached(open_file_mgr, mock_data_file):
    # Given: Fill up the OpenFileManager to its max limit (2)
    mock_df2 = Mock(spec=DataFile)
    mock_df2.path = "test_db2.txt"
    mock_df2.file_id = 100
    
    open_file_mgr.register(mock_data_file, FileAccessMode.READ_WRITE, FileLockMode.NONE)
    open_file_mgr.register(mock_df2, FileAccessMode.READ_WRITE, FileLockMode.NONE)

    # When / Then: Trying to register a 3rd file exceeds limits
    mock_df3 = Mock(spec=DataFile)
    mock_df3.path = "test_db3.txt"
    
    with pytest.raises(Exception, match="MaxOpenFilesExceededException"):
        open_file_mgr.register(mock_df3, FileAccessMode.READ_WRITE, FileLockMode.NONE)

def test_ut_ofm_03_releasing_handle_decrements_count(open_file_mgr, mock_data_file):
    # Given
    handle1 = open_file_mgr.register(mock_data_file, FileAccessMode.READ_WRITE, FileLockMode.NONE)
    handle2 = open_file_mgr.register(mock_data_file, FileAccessMode.READ_WRITE, FileLockMode.NONE)
    
    # When
    open_file_mgr.release_handle(handle1)
    
    # Then
    assert open_file_mgr.is_already_open("test_db.txt") is True # Entry is not purged functionally

def test_ut_ofm_04_auto_evict_handle(open_file_mgr, mock_data_file):
    # Given
    handle = open_file_mgr.register(mock_data_file, FileAccessMode.READ_WRITE, FileLockMode.NONE)
    
    # When
    open_file_mgr.release_handle(handle)
    
    # Then
    assert open_file_mgr.is_already_open("test_db.txt") is False # Structurally removed
