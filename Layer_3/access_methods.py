from .buffer_manager import BufferManager
from .record_manager import RecordManager

class AccessMethods:
    def __init__(self, buffer_manager: BufferManager, record_manager: RecordManager):
        self.buffer_manager = buffer_manager
        self.record_manager = record_manager
