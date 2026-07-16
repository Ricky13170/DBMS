import pytest
from unittest.mock import Mock, patch

# INTENTIONAL RED PHASE
from storage_engine.file_manager.services.file_reader import FileReader
from storage_engine.file_manager.services.file_writer import FileWriter
from storage_engine.file_manager.entities.file_handle import FileHandle
from storage_engine.file_manager.enums.file_access_mode import FileAccessMode
from storage_engine.file_manager.enums.file_lock_mode import FileLockMode

@pytest.fixture
def file_reader():
    return FileReader()

@pytest.fixture
def file_writer():
    return FileWriter()

@pytest.fixture
def read_write_handle():
    return FileHandle(handle_id=1, file_id=1, access_mode=FileAccessMode.READ_WRITE, lock_mode=FileLockMode.NONE)

@pytest.fixture
def read_only_handle():
    return FileHandle(handle_id=2, file_id=1, access_mode=FileAccessMode.READ_ONLY, lock_mode=FileLockMode.NONE)

def test_ut_io_01_write_valid_block(file_writer, read_write_handle):
    # Given
    data_to_write = b"HelloDBMS"
    
    with patch("os.pwrite") as mock_pwrite:
        # When
        file_writer.write_block(read_write_handle, offset=1024, data=data_to_write)
        
        # Then
        mock_pwrite.assert_called_once()

def test_ut_io_02_write_invalid_handle(file_writer, read_only_handle):
    # Given read_only_handle has AccessMode = READ_ONLY
    
    # When & Then
    with pytest.raises(Exception, match="InvalidHandleException"):
        file_writer.write_block(read_only_handle, offset=0, data=b"data")

def test_ut_io_03_read_valid_block(file_reader, read_write_handle):
    # Given
    expected_data = b"DBMS_PAGE_DATA"
    with patch("os.pread", return_value=expected_data) as mock_pread:
        # When
        result = file_reader.read_block(read_write_handle, offset=0, size=14)
        
        # Then
        assert result == expected_data
        mock_pread.assert_called_once()

def test_ut_io_04_read_out_of_bounds(file_reader, read_write_handle):
    # Given
    with patch("os.pread", side_effect=EOFError("EOFException")):
        # When & Then
        with pytest.raises(Exception, match="EOFException"):
            file_reader.read_block(read_write_handle, offset=999999, size=4096)
