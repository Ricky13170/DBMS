from .page_manager import PageManager

class BufferManager:
    def __init__(self, page_manager: PageManager):
        self.page_manager = page_manager
        self.buffer_pool = {}
        
    def pin_page(self, page_id: int) -> bool:
        return True
        
    def unpin_page(self, page_id: int, is_dirty: bool) -> bool:
        return True
        
    def flush_all(self) -> bool:
        return True
