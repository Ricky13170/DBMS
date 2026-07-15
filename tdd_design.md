# Chiến Lược TDD & Thiết Kế Kiểm Thử (D7)

Theo hướng dẫn của quản lý ở tệp `approach_analysis.md`, quy trình thiết kế hướng kiểm thử (Test-Driven Design - TDD) của dự án DBMS này tuân thủ nguyên tắc: **Định nghĩa Test Case trước khi viết Code**. 

## 1. Mối Liên Hệ Mindmap ↔ Sequence ↔ Class ↔ Test

Quy trình chuẩn của hệ thống đi theo trục cuốn chiếu:

1. **Mindmap (Layer 1,2,3):** Liệt kê các F1, F2 (Features). Trả lời: *"Hệ thống có những Tính năng nào?"*
2. **Sequence Diagram (D6):** Mô phỏng kịch bản chạy (Luồng). Trả lời: *"Các class gọi nhau như thế nào để thực hiện tính năng đó?"* -> *Từ đây đẻ ra các Method.*
3. **Class Detail (D4):** Chốt hạ chữ ký hàm (Input/Output). Trả lời: *"Cấu trúc code tĩnh trông ra sao?"*
4. **TDD / Unit Tests (D7, D8):** Viết test dựa trên Method của D4 và Kịch bản của D6. Trả lời: *"Làm sao biết hàm đó chạy đúng kịch bản?"*

## 2. Phân Biệt Các Loại Test trong Dự Án

### 2.1. Unit Test (Kiểm thử mức Đơn vị)
- **Mục đích:** Test *độc lập* một Method của một Class cụ thể (ví dụ `FileLifecycleManager.create_file()`). Giúp bắt lỗi cực kì chính xác (sai ở dòng nào, class nào).
- **Nguyên tắc:** Mock/Fake đi các thành phần phụ thuộc. Ví dụ: test `FileLifecycleManager` thì tạo một Fake `IFileSynchronizer`, khi gọi `delete_from_disk()` nó không xoá thật trên OS mà chỉ trả về `True`.
- **Dựa vào đâu để viết:** Bê y nguyên **Happy Path** và **Sad Path** trong nhánh **Sequence Diagram chi tiết (D6)** sang làm Test Case.
- **Nơi phân bổ:** Tham khảo folder `tests/unit/`

### 2.2. Integration Test (Kiểm thử Tích hợp / Test theo Luồng)
- **Mục đích:** Test sự kết hợp của một chuỗi dài các component (ví dụ Query Parser gọi xuống Optimizer, truyền xuống Storage Engine). 
- **Nguyên tắc:** Sử dụng implementation thật, ghi dữ liệu xuống đĩa thật (nhưng trỏ vào thư mục `/tmp/test_db/`).
- **Dựa vào đâu để viết:** Dựa vào **Sequence Diagram mức High-Level (D5)** (ví dụ: `SELECT Query end-to-end`).
- **Nơi phân bổ:** Tham khảo folder `tests/integration/`

## 3. Tiêu chuẩn viết Test Case (Given - When - Then)

Mọi Test Case trong tài liệu yêu cầu dùng chuẩn BDD (Behavior-Driven Development) để mô tả logic:

- **GIVEN (Bối cảnh ban đầu):** Trạng thái giả định hoặc đầu vào hệ thống (Input).
  *(VD: Hệ thống hiện đang chưa mở file nào. OpenFileTable trống rỗng).*
- **WHEN (Hành động):** Hành động được kích hoạt (Execute).
  *(VD: Caller gọi hàm `open_file("data.db")`).*
- **THEN (Kết quả mong đợi):** Kết quả trả ráp (Output) và sự thay đổi trạng thái (State Validation).
  *(VD: Hàm phải ném ra lỗi `FileNotFoundException`. Bảng `OpenFileTable` vẫn rỗng).*

---
*(Xem chi tiết việc áp dụng chiến lược này vào File Manager tại tệp `tests/unit/storage_engine_tests.md`)*
