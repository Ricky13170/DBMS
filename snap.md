# Báo Cáo Triển Khai TDD (Test-Driven Development) — File Manager

Tài liệu này lưu lại nguyên vẹn quy trình (Snapshots) chuyển đổi từ RED Phase sang GREEN Phase trong quá trình code tính năng `create_file` của module `File Manager`. Dùng để báo cáo tiến trình áp dụng Agile TDD cho Quản lý.

## 1. Bản Chất Của Vòng Lặp TDD

Trong TDD, **File Unit Test (`test_lifecycle_manager.py`) LÀ BẤT DI BẤT DỊCH**. Chúng ta không bao giờ xóa hay đổi file test. File test chính là "bản hợp đồng" do quản lý/kiến trúc sư đặt ra.

Điều thay đổi duy nhất nằm ở **File Mã Nguồn (`lifecycle_manager.py`)**. Chúng ta cố tình viết mã nguồn sai (RED) để chứng minh Test hoạt động, sau đó đắp logic vào mã nguồn (GREEN) để vượt qua bài test.

---

## 2. Lịch Sử: RED Phase (Pha Đỏ)

### A. Tình trạng Mã Nguồn (`lifecycle_manager.py`)
Code cố tình ném lỗi để kiểm tra sự khắc nghiệt của bài test.
```python
    def create_file(self, path: str, file_type: FileType) -> FileHandle:
        """
        TDD Step 1: Chủ đích đưa ra lỗi NotImplementedError.
        Unit Test chạy ở bước này bắt buộc phải THẤT BẠI (Red Phase).
        """
        raise NotImplementedError("TDD Đỏ: Chưa lập trình logic khởi tạo file, test phải thất bại!")
```

### B. Output thực tế trên Terminal (Failures)
Như đã chụp lại được trên terminal, hệ thống ném ra màn hình đỏ chót với 2 test cases đều FAILED:
```text
tests/unit_tests/test_lifecycle_manager.py::test_create_file_happy_path FAILED                                  [ 50%]
tests/unit_tests/test_lifecycle_manager.py::test_create_file_sad_path_already_exists FAILED                     [100%] 

>       raise NotImplementedError("TDD Đỏ: Chưa lập trình logic khởi tạo file, test phải thất bại!")
E       NotImplementedError: TDD Đỏ: Chưa lập trình logic khởi tạo file, test phải thất bại!

================================================= 2 failed in 0.21s ================================================== 
```

---

## 3. Lịch Sử: GREEN Phase (Pha Xanh)

### A. Tình trạng Mã Nguồn (`lifecycle_manager.py`)
Developer được giao nhiệm vụ viết logic 3 bước để vượt qua bài test. Lỗi `NotImplemented` bị xóa bỏ thay bằng logic tích hợp thật.
```python
    def create_file(self, path: str, file_type: FileType) -> FileHandle:
        # Bước 1: Yêu cầu cấp phát không gian vật lý
        self._synchronizer.allocate_on_disk(path)
        
        # Bước 2: Tạo đối tượng DataFile đại diện trên RAM
        data_file = DataFile(file_id=self._next_file_id, 
                             path=path, 
                             file_type=file_type, 
                             state=FileState.OPEN, 
                             size_bytes=0)
        self._next_file_id += 1
        
        # Bước 3: Đăng ký Handle với OpenFileManager
        file_handle = self._open_file_mgr.register(
            file=data_file, 
            mode=FileAccessMode.READ_WRITE, 
            lock=FileLockMode.EXCLUSIVE
        )
        
        return file_handle
```

### B. Output thực tế trên Terminal (Passed)
Sau khi nạp mã nguồn logic ở trên, file Test vẫn giữ nguyên nhưng Output khi gõ lệnh `pytest` đã hoàn toàn xanh rực rỡ báo hiệu Code đạt chất lượng nghiệp vụ:
```text
tests/unit_tests/test_lifecycle_manager.py::test_create_file_happy_path PASSED                                  [ 50%]
tests/unit_tests/test_lifecycle_manager.py::test_create_file_sad_path_already_exists PASSED                     [100%] 

================================================= 2 passed in 0.12s ================================================== 
```

---
**Kết luận gửi Quản lý:** 
Tính năng `create_file` của Storage Engine đã hoàn toàn "Decoupled" (Tách rời) và vượt qua quy trình kiểm định TDD độc lập. Sẵn sàng tích hợp cấp cao hoặc chuyển sang Module tiếp theo (Page Manager).
