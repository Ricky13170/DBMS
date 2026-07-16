import unittest
import os
import sys
import tempfile

# Trỏ PYTHONPATH về thư mục gốc (Database_management_system) để nhận dạng package "src"
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.Layer_3.storage_engine.file_manager import FileManager

class TestFileManager(unittest.TestCase):

    
    def setUp(self):

        self.fm = FileManager()
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.test_dir.name, "test_db_data.dat")
        self.file_id = 99 # Mock một file_id
        
    def tearDown(self):

        for _, fd in list(self.fm._open_files.items()):
            try:
                os.close(fd)
            except OSError:
                pass
        self.fm._open_files.clear()
        

        self.test_dir.cleanup()

    def test_create_and_open_file(self):
        """Test tính năng tạo file vật lý và mở file (lưu cache fd)."""
   
        created = self.fm.create_file(self.test_file, self.file_id)
        opened = self.fm.open_file(self.test_file, self.file_id)
        
     
        self.assertTrue(created, "Phải tạo file thành công")
        self.assertTrue(opened, "Phải mở file thành công")
        self.assertTrue(os.path.exists(self.test_file), "File vật lý phải tồn tại trên đĩa")
        self.assertEqual(len(self.fm._open_files), 1, "Bộ đệm File Descriptor phải có 1 file đang mở")

    def test_write_and_read_block(self):
        """Test tuần tự: Tạo -> Mở -> Ghi 1 block (4096 bytes) -> Đọc lại block đó."""
        self.fm.create_file(self.test_file, self.file_id)
        self.fm.open_file(self.test_file, self.file_id)
        
        block_id = 0
   
        test_data = b"A" * FileManager.PAGE_SIZE 
        
  
        is_written = self.fm.write_block(self.file_id, block_id, test_data)
        self.assertTrue(is_written, "Hàm ghi block phải trả về True")
        
     
        read_data = self.fm.read_block(self.file_id, block_id)
        

        self.assertEqual(len(read_data), FileManager.PAGE_SIZE, "Độ dài block đọc lên phải bằng đúng PAGE_SIZE")
        self.assertEqual(read_data, test_data, "Nội dung byte đọc lên bị sai lệch so với lúc ghi")
        
    def test_close_file(self):
        """Test tính năng đóng handle an toàn chống tràn nhỡ nhớ."""
        self.fm.create_file(self.test_file, self.file_id)
        self.fm.open_file(self.test_file, self.file_id)
        
        closed = self.fm.close_file(self.file_id)
        self.assertTrue(closed, "Đóng file phải trả về True")
        self.assertEqual(len(self.fm._open_files), 0, "Biến dict đệm _open_files phải trống")

if __name__ == '__main__':
    unittest.main()
