import pytest
from unittest.mock import Mock

# INTENTIONAL RED PHASE: These imports will fail because the classes do not exist yet!
from storage_engine.file_manager.services.file_lifecycle_manager import FileLifecycleManager
from storage_engine.file_manager.enums.file_type import FileType
from storage_engine.file_manager.entities.file_handle import FileHandle

@pytest.fixture
def mock_open_file_mgr():
    return Mock()

@pytest.fixture
def mock_reader():
    return Mock()

@pytest.fixture
def mock_writer():
    return Mock()

@pytest.fixture
def mock_synchronizer():
    return Mock()

@pytest.fixture
def lifecycle_mgr(mock_open_file_mgr, mock_reader, mock_writer, mock_synchronizer):
    return FileLifecycleManager(mock_open_file_mgr, mock_reader, mock_writer, mock_synchronizer)

def test_ut_flm_01_happy_create(lifecycle_mgr, mock_synchronizer, mock_open_file_mgr):
    # Given
    mock_synchronizer.allocate_on_disk.return_value = None
    mock_open_file_mgr.register.return_value = Mock(spec=FileHandle)

    # When
    handle = lifecycle_mgr.create_file("db.txt", FileType.DATA)

    # Then
    mock_synchronizer.allocate_on_disk.assert_called_once_with("db.txt")
    mock_open_file_mgr.register.assert_called_once()
    assert handle is not None

def test_ut_flm_02_sad_create_exists(lifecycle_mgr, mock_synchronizer, mock_open_file_mgr):
    # Given
    mock_synchronizer.allocate_on_disk.side_effect = Exception("FileAlreadyExists")

    # When & Then
    with pytest.raises(Exception, match="FileAlreadyExists"):
        lifecycle_mgr.create_file("db.txt", FileType.DATA)
    mock_open_file_mgr.register.assert_not_called()

def test_ut_flm_03_happy_delete(lifecycle_mgr, mock_open_file_mgr, mock_synchronizer):
    # Given
    mock_open_file_mgr.is_already_open.return_value = False

    # When
    result = lifecycle_mgr.delete_file("db.txt")

    # Then
    assert result is True
    mock_synchronizer.delete_from_disk.assert_called_once_with("db.txt")

def test_ut_flm_04_sad_delete_in_use(lifecycle_mgr, mock_open_file_mgr, mock_synchronizer):
    # Given
    mock_open_file_mgr.is_already_open.return_value = True

    # When & Then
    with pytest.raises(Exception, match="FileInUseException"):
        lifecycle_mgr.delete_file("db.txt")
    mock_synchronizer.delete_from_disk.assert_not_called()
