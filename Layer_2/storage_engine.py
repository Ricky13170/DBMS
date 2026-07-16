class FileManager:
    pass


class PageManager:
    pass


class BufferManager:
    pass


class RecordManager:
    pass


class AccessMethods:
    pass


class StorageAllocation:
    pass


class StorageEngineFacade:
    def __init__(self):
        self.file_manager = FileManager()
        self.page_manager = PageManager()
        self.buffer_manager = BufferManager()
        self.record_manager = RecordManager()
        self.access_methods = AccessMethods()
        self.storage_allocation = StorageAllocation()
