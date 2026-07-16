import os
from typing import Dict

class FileManager:
    PAGE_SIZE = 4096

    def __init__(self):
        self._open_files: Dict[int, int] = {}
        
    def _get_file_handle(self, file_id: int) -> int:
        if file_id not in self._open_files:
            raise IOError(f"File ID {file_id} chưa được mở!")
        return self._open_files[file_id]

    def create_file(self, file_path: str, file_id: int) -> bool:
        try:
            with open(file_path, 'wb') as f:
                pass
            return True
        except Exception:
            return False

    def open_file(self, file_path: str, file_id: int) -> bool:
        try:
            flags = os.O_RDWR | getattr(os, 'O_BINARY', 0)
            fd = os.open(file_path, flags)
            self._open_files[file_id] = fd
            return True
        except Exception:
            return False

    def close_file(self, file_id: int) -> bool:
        if file_id in self._open_files:
            fd = self._open_files.pop(file_id)
            os.close(fd)
            return True
        return False

    def read_block(self, file_id: int, block_id: int) -> bytes:
        fd = self._get_file_handle(file_id)
        os.lseek(fd, block_id * self.PAGE_SIZE, os.SEEK_SET)
        data = os.read(fd, self.PAGE_SIZE)
        return data

    def write_block(self, file_id: int, block_id: int, data: bytes) -> bool:
        if len(data) != self.PAGE_SIZE:
            raise ValueError(f"Dữ liệu bắt buộc phải đúng {self.PAGE_SIZE} bytes.")
            
        fd = self._get_file_handle(file_id)
        os.lseek(fd, block_id * self.PAGE_SIZE, os.SEEK_SET)
        bytes_written = os.write(fd, data)
        return bytes_written == self.PAGE_SIZE
