# Detailed Class Diagram — File Manager (Storage Engine)

Tài liệu này đặc tả chi tiết Layer 4 cho sub-module **File Manager**, bao gồm đầy đủ thuộc tính (properties), phương thức (methods), kiểu dữ liệu (Python type hint), và quan hệ giữa các lớp. (Cập nhật sau khi phân tích luồng Sequence D5/D6).

---

## 1. Chi Tiết Các Sub-Groups

### Sub-Group 1: File Lifecycle
Chịu trách nhiệm tạo mới, xóa bỏ, đổi tên và kiểm soát trạng thái vật lý của các file dữ liệu trên hệ thống.

```mermaid
classDiagram
    class FileType {
        <<enumeration>>
        DATA
        LOG
        TEMP
    }
    class FileState {
        <<enumeration>>
        OPEN
        CLOSED
        CREATING
        CORRUPTED
    }
    class DataFile {
        <<entity>>
        +file_id: int
        +path: str
        +file_type: FileType
        +state: FileState
        +size_bytes: int
        +__init__(file_id: int, path: str, file_type: FileType, state: FileState, size_bytes: int)
        +load(path: str) DataFile$
    }
    class IFileLifecycleManager {
        <<interface>>
        +create_file(path: str, file_type: FileType) FileHandle
        +open_file(path: str, mode: FileAccessMode, lock: FileLockMode) FileHandle
        +close_file(handle: FileHandle) None
        +delete_file(path: str) bool
        +allocate_space(handle: FileHandle, size_bytes: int) int
    }
    class FileLifecycleManager {
        -_open_file_mgr: IOpenFileManager
        -_reader: IFileReader
        -_writer: IFileWriter
        -_synchronizer: IFileSynchronizer
        +__init__(open_file_mgr: IOpenFileManager, reader: IFileReader, writer: IFileWriter, synchronizer: IFileSynchronizer)
        +create_file(path: str, file_type: FileType) FileHandle
        +open_file(path: str, mode: FileAccessMode, lock: FileLockMode) FileHandle
        +close_file(handle: FileHandle) None
        +delete_file(path: str) bool
        +allocate_space(handle: FileHandle, size_bytes: int) int
        -_lookup_data_file(path: str) DataFile
    }

    IFileLifecycleManager <|.. FileLifecycleManager
    FileLifecycleManager ..> DataFile : creates/lookups
    DataFile ..> FileType
    DataFile ..> FileState
```

### Sub-Group 2: File Open/Close Management
Quản lý việc ánh xạ các file đang mở (OpenFileTable), cơ chế đếm số lần sử dụng (reference counting), và cơ chế khóa file nhằm đảm bảo tính toàn vẹn đa luồng/tiến trình.

```mermaid
classDiagram
    class FileAccessMode {
        <<enumeration>>
        READ_ONLY
        WRITE_ONLY
        READ_WRITE
    }
    class FileLockMode {
        <<enumeration>>
        SHARED
        EXCLUSIVE
        NONE
    }
    class FileHandle {
        <<entity>>
        +handle_id: int
        +file_id: int
        +access_mode: FileAccessMode
        +lock_mode: FileLockMode
        +is_valid: bool
        +__init__(handle_id: int, file_id: int, access_mode: FileAccessMode, lock_mode: FileLockMode)
        +invalidate() None
    }
    class OpenFileEntry {
        <<entity>>
        +file_id: int
        +handle: FileHandle
        +open_count: int
        +last_accessed: int
        +__init__(file_id: int, handle: FileHandle)
        +increment_open_count() None
        +decrement_open_count() int
    }
    class OpenFileTable {
        <<entity>>
        -_entries: dict~int, OpenFileEntry~
        +__init__()
        +has_entry(path: str) bool
        +add_entry(file: DataFile, mode: FileAccessMode, lock: FileLockMode) OpenFileEntry
        +find_entry(path: str) OpenFileEntry
        +remove_entry(handle_id: int) None
        +validate_handle(handle: FileHandle) bool
    }
    class IOpenFileManager {
        <<interface>>
        +get_handle(path: str) FileHandle
        +is_already_open(path: str) bool
        +register(file: DataFile, mode: FileAccessMode, lock: FileLockMode) FileHandle
        +release_handle(handle: FileHandle) bool
    }
    class OpenFileManager {
        -_table: OpenFileTable
        -_max_open: int
        -_next_handle_id: int
        +__init__(max_open: int)
        +get_handle(path: str) FileHandle
        +is_already_open(path: str) bool
        +register(file: DataFile, mode: FileAccessMode, lock: FileLockMode) FileHandle
        +release_handle(handle: FileHandle) bool
    }

    IOpenFileManager <|.. OpenFileManager
    OpenFileManager *-- OpenFileTable
    OpenFileTable *-- OpenFileEntry
    OpenFileEntry *-- FileHandle
    FileHandle ..> FileAccessMode
    FileHandle ..> FileLockMode
```

### Sub-Group 3: Data Read/Write
Xử lý các thao tác đọc và ghi dữ liệu mức tối thấp (block-level read/write) tại một offset cụ thể.

```mermaid
classDiagram
    class IFileReader {
        <<interface>>
        +read_block(handle: FileHandle, offset: int, size: int) bytes
    }
    class FileReader {
        -_file_descriptors: dict~int, object~
        +__init__()
        +read_block(handle: FileHandle, offset: int, size: int) bytes
    }
    class IFileWriter {
        <<interface>>
        +write_block(handle: FileHandle, offset: int, data: bytes) None
    }
    class FileWriter {
        -_file_descriptors: dict~int, object~
        +__init__()
        +write_block(handle: FileHandle, offset: int, data: bytes) None
    }

    IFileReader <|.. FileReader
    IFileWriter <|.. FileWriter
```

### Sub-Group 4: Disk Synchronization
Đảm bảo cơ chế đồng bộ hóa dữ liệu từ bộ nhớ đệm (OS cache) xuống thiết bị lưu trữ vật lý nhằm đáp ứng tiêu chí ACID (phần Durability). Cũng quản lý việc không gian tĩnh.

```mermaid
classDiagram
    class IFileSynchronizer {
        <<interface>>
        +allocate_on_disk(path: str) None
        +delete_from_disk(path: str) None
        +expand_file(handle: FileHandle, size_bytes: int) int
        +fsync(handle: FileHandle) None
        +flush_buffers(handle: FileHandle) None
    }
    class FileSynchronizer {
        +__init__()
        +allocate_on_disk(path: str) None
        +delete_from_disk(path: str) None
        +expand_file(handle: FileHandle, size_bytes: int) int
        +fsync(handle: FileHandle) None
        +flush_buffers(handle: FileHandle) None
    }

    IFileSynchronizer <|.. FileSynchronizer
```

---

## 2. Toàn Bộ Detailed Class Diagram (Gộp & Quan Hệ Hoàn Chỉnh)

Sơ đồ quan hệ phụ thuộc giữa các lớp thực thi và interface trong cấu trúc File Manager (bao gồm các dependency injection):

```mermaid
classDiagram
    direction TB

    %% File Lifecycle
    class DataFile {
        +file_id: int
        +path: str
        +file_type: FileType
        +state: FileState
        +size_bytes: int
        +load(path) DataFile$
    }
    class FileLifecycleManager {
        -_open_file_mgr: IOpenFileManager
        -_reader: IFileReader
        -_writer: IFileWriter
        -_synchronizer: IFileSynchronizer
        +create_file(path: str, file_type: FileType) FileHandle
        +open_file(path: str, mode: FileAccessMode, lock: FileLockMode) FileHandle
        +close_file(handle: FileHandle) None
        +delete_file(path: str) bool
        +allocate_space(handle: FileHandle, size_bytes: int) int
    }

    %% Open/Close Manager
    class FileHandle {
        +handle_id: int
        +file_id: int
        +access_mode: FileAccessMode
        +lock_mode: FileLockMode
        +is_valid: bool
    }
    class OpenFileEntry {
        +file_id: int
        +handle: FileHandle
        +open_count: int
        +last_accessed: int
    }
    class OpenFileTable {
        -entries: dict~int, OpenFileEntry~
        +add_entry(file: DataFile, mode: FileAccessMode, lock: FileLockMode) OpenFileEntry
        +find_entry(path: str) OpenFileEntry
        +validate_handle(handle: FileHandle) bool
        +remove_entry(handle_id: int) None
    }
    class OpenFileManager {
        -_table: OpenFileTable
        -_max_open: int
        -_next_handle_id: int
        +is_already_open(path: str) bool
        +get_handle(path: str) FileHandle
        +register(file: DataFile, mode: FileAccessMode, lock: FileLockMode) FileHandle
        +release_handle(handle: FileHandle) bool
    }

    %% Read/Write
    class FileReader {
        -_file_descriptors: dict~int, object~
        +read_block(handle: FileHandle, offset: int, size: int) bytes
    }
    class FileWriter {
        -_file_descriptors: dict~int, object~
        +write_block(handle: FileHandle, offset: int, data: bytes) None
    }

    %% Synchronizer
    class FileSynchronizer {
        +allocate_on_disk(path: str) None
        +delete_from_disk(path: str) None
        +expand_file(handle: FileHandle, size_bytes: int) int
        +fsync(handle: FileHandle) None
        +flush_buffers(handle: FileHandle) None
    }

    %% Interfaces
    class IFileLifecycleManager { <<interface>> }
    class IOpenFileManager { <<interface>> }
    class IFileReader { <<interface>> }
    class IFileWriter { <<interface>> }
    class IFileSynchronizer { <<interface>> }

    %% Realizations
    IFileLifecycleManager <|.. FileLifecycleManager
    IOpenFileManager <|.. OpenFileManager
    IFileReader <|.. FileReader
    IFileWriter <|.. FileWriter
    IFileSynchronizer <|.. FileSynchronizer

    %% Aggregations (Facade dependency Injection)
    FileLifecycleManager o--> IOpenFileManager : delegates handle track
    FileLifecycleManager o--> IFileReader      : delegates reads
    FileLifecycleManager o--> IFileWriter      : delegates writes
    FileLifecycleManager o--> IFileSynchronizer: delegates syncs

    %% Compositions
    OpenFileManager *-- OpenFileTable
    OpenFileTable *-- OpenFileEntry
    OpenFileEntry *-- FileHandle

    %% Dependencies
    FileLifecycleManager ..> DataFile : creates/lookups
```

---

## 3. Bản Đồ Properties & Methods Chi Tiết

Dưới đây là thống kê toàn bộ thuộc tính và phương thức với kiểu dữ liệu của File Manager chuẩn bị cho TDD:

| Class / Entity | Type | Properties | Methods & Signatures |
| :--- | :--- | :--- | :--- |
| **`DataFile`** | Entity | - `file_id: int`<br>- `path: str`<br>- `file_type: FileType`<br>- `state: FileState`<br>- `size_bytes: int` | - `__init__(file_id, path, file_type, state, size_bytes)`<br>- `load(path: str) -> DataFile` (Static) |
| **`FileHandle`** | Entity | - `handle_id: int`<br>- `file_id: int`<br>- `access_mode: FileAccessMode`<br>- `lock_mode: FileLockMode`<br>- `is_valid: bool` | - `__init__(handle_id, file_id, access_mode, lock_mode)`<br>- `invalidate() -> None` |
| **`OpenFileEntry`** | Entity | - `file_id: int`<br>- `handle: FileHandle`<br>- `open_count: int`<br>- `last_accessed: int` | - `__init__(file_id, handle)`<br>- `increment_open_count() -> None`<br>- `decrement_open_count() -> int` |
| **`OpenFileTable`** | Entity | - `_entries: dict[int, OpenFileEntry]` | - `__init__()`<br>- `has_entry(path: str) -> bool`<br>- `add_entry(file, mode, lock) -> OpenFileEntry`<br>- `find_entry(path: str) -> OpenFileEntry`<br>- `remove_entry(handle_id)`<br>- `validate_handle(handle) -> bool` |
| **`FileLifecycleManager`** | Facade | - `_open_file_mgr: IOpenFileManager`<br>- `_reader: IFileReader`<br>- `_writer: IFileWriter`<br>- `_synchronizer: IFileSynchronizer` | - `__init__(open_file_mgr, reader, writer, synchronizer)`<br>- `create_file(path, file_type) -> FileHandle`<br>- `open_file(path, mode, lock) -> FileHandle`<br>- `close_file(handle) -> None`<br>- `delete_file(path) -> bool`<br>- `allocate_space(handle, size_bytes) -> int`<br>- `_lookup_data_file(path) -> DataFile` |
| **`OpenFileManager`** | Service | - `_table: OpenFileTable`<br>- `_max_open: int`<br>- `_next_handle_id: int` | - `__init__(max_open)`<br>- `get_handle(path: str) -> FileHandle`<br>- `is_already_open(path: str) -> bool`<br>- `register(file, mode, lock) -> FileHandle`<br>- `release_handle(handle) -> bool` |
| **`FileReader`** | Service | - `_file_descriptors: dict[int, object]` | - `__init__()`<br>- `read_block(handle, offset, size) -> bytes` |
| **`FileWriter`** | Service | - `_file_descriptors: dict[int, object]` | - `__init__()`<br>- `write_block(handle, offset, data) -> None` |
| **`FileSynchronizer`** | Service | None | - `allocate_on_disk(path: str) -> None`<br>- `delete_from_disk(path: str) -> None`<br>- `expand_file(handle, size_bytes) -> int`<br>- `fsync(handle) -> None`<br>- `flush_buffers(handle) -> None` |
