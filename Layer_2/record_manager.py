from .buffer_manager import BufferManager

class RecordManager:
    def __init__(self, buffer_manager: BufferManager):
        self.buffer_manager = buffer_manager
        
    def insert_record(self, page_id: int, data: bytes) -> int:
        return 0
        
    def read_record(self, page_id: int, slot_id: int) -> bytes:
        return b""
        
    def delete_record(self, page_id: int, slot_id: int) -> bool:
        return True
