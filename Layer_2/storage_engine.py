# class FileManager:
#     pass


# class PageManager:
#     pass


# class BufferManager:
#     pass


# class RecordManager:
#     pass


# class AccessMethods:
#     pass


# class StorageAllocation:
#     pass


# class StorageEngineFacade:
#     def __init__(self):
#         self.file_manager = FileManager()
#         self.page_manager = PageManager()
#         self.buffer_manager = BufferManager()
#         self.record_manager = RecordManager()
#         self.access_methods = AccessMethods()
#         self.storage_allocation = StorageAllocation()
from .file_manager import FileManager
from .page_manager import PageManager
from .buffer_manager import BufferManager
from .record_manager import RecordManager
from .access_methods import AccessMethods
from .storage_allocation import StorageAllocation

class StorageEngineFacade:
    def __init__(self):
        self.file_manager = FileManager()
        self.storage_allocation = StorageAllocation(self.file_manager)
        self.page_manager = PageManager(self.file_manager)
        self.buffer_manager = BufferManager(self.page_manager)
        self.record_manager = RecordManager(self.buffer_manager)
        self.access_methods = AccessMethods(self.buffer_manager, self.record_manager)
