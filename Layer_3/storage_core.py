from .file_manager import FileManager
from .page_manager import PageManager
from .buffer_manager import BufferManager
from .record_manager import RecordManager
from .access_methods import AccessMethods
from .storage_allocation import StorageAllocation

class StorageEngineFacade:
    """Lớp điều phối trung tâm của riêng cụm Storage Engine"""
    def __init__(self):
        self.file_manager = FileManager()
        self.storage_allocation = StorageAllocation(self.file_manager)
        self.page_manager = PageManager(self.file_manager)
        self.buffer_manager = BufferManager(self.page_manager)
        self.record_manager = RecordManager(self.buffer_manager)
        self.access_methods = AccessMethods(self.buffer_manager, self.record_manager)
