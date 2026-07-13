# Detailed Class Diagram — File Manager (Storage Engine)

Tài liệu này đặc tả chi tiết Layer 4 cho sub-module **File Manager**, bao gồm đầy đủ thuộc tính (properties), phương thức (methods), kiểu dữ liệu (Python type hint), và quan hệ giữa các lớp.

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
    }
    class IFileLifecycleManager {
        <<interface>>
        +create_file(path: str, file_type: FileType) DataFile
        +open_file(file_id: int, mode: FileAccessMode) FileHandle
        +close_file(handle: FileHandle) None
        +delete_file(file_id: int) None
        +rename_file(file_id: int, new_path: str) None
    }
    class FileLifecycleManager {
        -_open_file_mgr: IOpenFileManager
        -_reader: IFileReader
        -_writer: IFileWriter
        -_synchronizer: IFileSynchronizer
        +__init__(open_file_mgr: IOpenFileManager, reader: IFileReader, writer: IFileWriter, synchronizer: IFileSynchronizer)
        +create_file(path: str, file_type: FileType) DataFile
        +open_file(file_id: int, mode: FileAccessMode) FileHandle
        +close_file(handle: FileHandle) None
        +delete_file(file_id: int) None
        +rename_file(file_id: int, new_path: str) None
        -_lookup_data_file(file_id: int) DataFile
    }

    IFileLifecycleManager <|.. FileLifecycleManager
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
        +has_entry(file_id: int) bool
        +add_entry(entry: OpenFileEntry) None
        +get_entry(file_id: int) OpenFileEntry
        +remove_entry(file_id: int) None
    }
    class IOpenFileManager {
        <<interface>>
        +get_handle(file_id: int) FileHandle
        +is_open(file_id: int) bool
        +register_handle(handle: FileHandle) None
        +increment_open_count(file_id: int) FileHandle
        +release_handle(handle: FileHandle) bool
        +get_open_count() int
        +force_close_all() None
    }
    class OpenFileManager {
        -_table: OpenFileTable
        -_max_open: int
        -_next_handle_id: int
        +__init__(max_open: int)
        +get_handle(file_id: int) FileHandle
        +is_open(file_id: int) bool
        +register_handle(handle: FileHandle) None
        +increment_open_count(file_id: int) FileHandle
        +release_handle(handle: FileHandle) bool
        +get_open_count() int
        +force_close_all() None
        -_register_handle(handle: FileHandle) None
        -_unregister_handle(handle: FileHandle) None
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
Đảm bảo cơ chế đồng bộ hóa dữ liệu từ bộ nhớ đệm (OS cache) xuống thiết bị lưu trữ vật lý nhằm đáp ứng tiêu chí ACID (phần Durability).

```mermaid
classDiagram
    class IFileSynchronizer {
        <<interface>>
        +fsync(handle: FileHandle) None
        +flush_buffers(handle: FileHandle) None
    }
    class FileSynchronizer {
        +__init__()
        +fsync(handle: FileHandle) None
        +flush_buffers(handle: FileHandle) None
    }

    IFileSynchronizer <|.. FileSynchronizer
```

---

## 2. Toàn Bộ Detailed Class Diagram (Gộp & Quan Hệ Hoàn Chỉnh)

Sơ đồ quan hệ phụ thuộc giữa các lớp thực thi và interface trong cấu trúc File Manager:

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
    }
    class FileLifecycleManager {
        -_open_file_mgr: IOpenFileManager
        -_reader: IFileReader
        -_writer: IFileWriter
        -_synchronizer: IFileSynchronizer
        +create_file(path: str, file_type: FileType) DataFile
        +open_file(file_id: int, mode: FileAccessMode) FileHandle
        +close_file(handle: FileHandle) None
        +delete_file(file_id: int) None
        +rename_file(file_id: int, new_path: str) None
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
    }
    class OpenFileManager {
        -_table: OpenFileTable
        -_max_open: int
        -_next_handle_id: int
    }

    %% Read/Write
    class FileReader {
        -_file_descriptors: dict~int, object~
    }
    class FileWriter {
        -_file_descriptors: dict~int, object~
    }

    %% Synchronizer
    class FileSynchronizer {
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
```

---

## 3. Bản Đồ Properties & Methods Chi Tiết

Dưới đây là thống kê toàn bộ thuộc tính và phương thức với kiểu dữ liệu của File Manager:

| Class / Entity | Type | Properties | Methods & Signatures |
| :--- | :--- | :--- | :--- |
| **`DataFile`** | Entity | - `file_id: int`<br>- `path: str`<br>- `file_type: FileType`<br>- `state: FileState`<br>- `size_bytes: int` | - `__init__(file_id, path, file_type, state, size_bytes)` |
| **`FileHandle`** | Entity | - `handle_id: int`<br>- `file_id: int`<br>- `access_mode: FileAccessMode`<br>- `lock_mode: FileLockMode`<br>- `is_valid: bool` | - `__init__(handle_id, file_id, access_mode, lock_mode)`<br>- `invalidate() -> None` |
| **`OpenFileEntry`** | Entity | - `file_id: int`<br>- `handle: FileHandle`<br>- `open_count: int`<br>- `last_accessed: int` | - `__init__(file_id, handle)`<br>- `increment_open_count() -> None`<br>- `decrement_open_count() -> int` |
| **`OpenFileTable`** | Entity | - `_entries: dict[int, OpenFileEntry]` | - `__init__()`<br>- `has_entry(file_id) -> bool`<br>- `add_entry(entry)`<br>- `get_entry(file_id) -> OpenFileEntry`<br>- `remove_entry(file_id)` |
| **`FileLifecycleManager`** | Service | - `_open_file_mgr: IOpenFileManager`<br>- `_reader: IFileReader`<br>- `_writer: IFileWriter`<br>- `_synchronizer: IFileSynchronizer` | - `__init__(open_file_mgr, reader, writer, synchronizer)`<br>- `create_file(path, file_type) -> DataFile`<br>- `open_file(file_id, mode) -> FileHandle`<br>- `close_file(handle) -> None`<br>- `delete_file(file_id) -> None`<br>- `rename_file(file_id, new_path) -> None`<br>- `_lookup_data_file(file_id) -> DataFile` |
| **`OpenFileManager`** | Service | - `_table: OpenFileTable`<br>- `_max_open: int`<br>- `_next_handle_id: int` | - `__init__(max_open)`<br>- `get_handle(file_id) -> FileHandle`<br>- `is_open(file_id) -> bool`<br>- `register_handle(handle) -> None`<br>- `increment_open_count(file_id) -> FileHandle`<br>- `release_handle(handle) -> bool`<br>- `get_open_count() -> int`<br>- `force_close_all() -> None`<br>- `_register_handle(handle) -> None`<br>- `_unregister_handle(handle) -> None` |
| **`FileReader`** | Service | - `_file_descriptors: dict[int, object]` | - `__init__()`<br>- `read_block(handle, offset, size) -> bytes` |
| **`FileWriter`** | Service | - `_file_descriptors: dict[int, object]` | - `__init__()`<br>- `write_block(handle, offset, data) -> None` |
| **`FileSynchronizer`** | Service | None | - `__init__()`<br>- `fsync(handle) -> None`<br>- `flush_buffers(handle) -> None` |
