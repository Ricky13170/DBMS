from .file_manager import FileManager

class PageManager:
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
        
    def format_page(self, page_id: int) -> bool:
        return True
