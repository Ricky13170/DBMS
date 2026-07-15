# TDD Unit Tests — Storage Engine

Tài liệu này chứa danh sách các Unit Test cases thiết kế theo chuẩn BDD (Given-When-Then) ứng với từng phương thức đã được bóc tách từ Sequence Diagram trong tài liệu D6.

---

## 1. Unit Tests cho `File Manager`

Dựa trên Sequence Diagram `06a_seq_file_management.md` và Detailed Class Diagram `04_class_detail_file_management.md`, chúng ta có các Test Cases độc lập sau:

### 1.1. Test Cases: `FileLifecycleManager.create_file()`

*Kịch bản tham chiếu: Operation 1 - createFile()*

**Test Case 1: Tạo file thành công (Happy Path)**
- **GIVEN:** Đường dẫn `path` hợp lệ, Hệ điều hành (Fake OS) có chỗ trống, `OpenFileManager` (được Mock) sẵn sàng nội suy.
- **WHEN:** Gọi `FileLifecycleManager.create_file("test.db", FileType.DATA)`
- **THEN:**
  - Kết quả trả về (Output) là một `FileHandle` hợp lệ (is_valid = True).
  - Trạng thái `DataFile` ban đầu là CREATING, sau đó chuyển thành OPEN.
  - Hàm `IFileSynchronizer.allocate_on_disk()` phải được gọi lướt qua (Verified in Mock).
  - Hàm `IOpenFileManager.register()` được gọi với `access_mode=READ_WRITE`.

**Test Case 2: Tạo file thất bại do File đã tồn tại (Sad Path)**
- **GIVEN:** File `"test.db"` đã tồn tại vật lý trên ổ cứng. `IFileSynchronizer.allocate_on_disk()` (Mock) được cài đặt để quăng ra lỗi `FileAlreadyExistsException`.
- **WHEN:** Gọi `FileLifecycleManager.create_file("test.db", FileType.DATA)`
- **THEN:** 
  - Hệ thống ném ra đúng Exception `FileAlreadyExistsException`.
  - Hàm `IOpenFileManager.register()` KHÔNG BAO GIỜ được gọi.

### 1.2. Test Cases: `FileLifecycleManager.open_file()`

*Kịch bản tham chiếu: Operation 2 - openFile()*

**Test Case 3: Mở file mới lần đầu tiên (Happy Path)**
- **GIVEN:** `IOpenFileManager.is_already_open("test.db")` trả về False. File `"test.db"` có sẵn trên đĩa.
- **WHEN:** Gọi `open_file("test.db", READ_WRITE, EXCLUSIVE)`
- **THEN:**
  - Trả về `FileHandle`.
  - Static method `DataFile.load()` phải được gọi đúng 1 lần.
  - `IOpenFileManager.register()` được gọi.

**Test Case 4: Mở file đã được mở trước đó (Reuse - Happy Path)**
- **GIVEN:** `IOpenFileManager.is_already_open("test.db")` trả về True. Hàm `get_handle("test.db")` trả về một `FileHandle(ID=12)`.
- **WHEN:** Gọi `open_file("test.db", READ_ONLY, SHARED)`
- **THEN:**
  - Trả về đúng `FileHandle(ID=12)` đã tồn tại.
  - `DataFile.load()` và `register()` KHÔNG bị gọi. (Chống lãng phí Handle của OS).

**Test Case 5: File không tồn tại (Sad Path)**
- **GIVEN:** File `"test.db"` không nằm trên đĩa. `DataFile.load()` ném lỗi `FileNotFoundException`.
- **WHEN:** Gọi `open_file("test.db", READ_ONLY, SHARED)`
- **THEN:**
  - Trả về lỗi `FileNotFoundException`.

---

### 1.3. Test Cases: `OpenFileManager.register()`

*Kịch bản tham chiếu: Việc ghi chép Handle vào RAM*

**Test Case 6: Ghi danh thành công**
- **GIVEN:** Bảng `OpenFileTable` rỗng. 
- **WHEN:** Gọi `OpenFileManager.register(DataFile("test.db"), READ_WRITE, EXCLUSIVE)`
- **THEN:**
  - Kết quả trả về `FileHandle(is_valid=True)`.
  - `OpenFileTable.add_entry()` được gọi.
  - Bộ đếm `open_count` của Entry bằng 1.

**Test Case 7: Vượt quá số lượng file tối đa (Sad Path)**
- **GIVEN:** `OpenFileManager` khởi tạo với `max_open = 100`. Bảng `OpenFileTable` đang chứa đúng 100 Entries.
- **WHEN:** Gọi `register()` cho một File thứ 101.
- **THEN:**
  - Trả về lỗi `TooManyFilesOpenException`.
  - Bảng `OpenFileTable` vẫn giữ nguyên mốc 100.
