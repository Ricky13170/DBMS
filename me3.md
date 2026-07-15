# File Management — Sequence Diagrams

> **Phương pháp:** Bottom-up — từng operation nhỏ trước, gộp dần lên Feature-level.
>
> **Participants lấy từ Layer 4 File Manager:**
> - `FileLifecycleManager` (Facade — F1)
> - `OpenFileManager` (F2)
> - `OpenFileTable` / `OpenFileEntry` / `FileHandle` (F2 Entities)
> - `DataFile` (F1 Entity)
> - `FileSynchronizer` (F4)
> - `FileReader` / `FileWriter` (F3)

---

## Operation 1: createFile()

**Kịch bản:** DBMS cần tạo một file dữ liệu vật lý mới (ví dụ khi tạo Table mới).

**Happy Path:**
```mermaid
sequenceDiagram
    autonumber
    actor Caller as Caller (TableManager)
    participant FLM as FileLifecycleManager
    participant DF as DataFile
    participant OFM as OpenFileManager
    participant OFT as OpenFileTable
    participant FS as FileSynchronizer

    Caller->>FLM: createFile(path, fileType)

    FLM->>DF: new DataFile(path, fileType, state=CREATING)
    FLM->>FS: allocateOnDisk(path)
    FS-->>FLM: ok

    FLM->>DF: setState(OPEN)

    FLM->>OFM: register(dataFile, accessMode=READ_WRITE)
    OFM->>OFT: addEntry(dataFile)
    OFT->>OFT: new OpenFileEntry(dataFile, accessMode)
    OFT-->>OFM: fileHandle (FileHandle)
    OFM-->>FLM: fileHandle

    FLM-->>Caller: fileHandle
```

**Sad Path — File đã tồn tại:**
```mermaid
sequenceDiagram
    autonumber
    actor Caller as Caller (TableManager)
    participant FLM as FileLifecycleManager
    participant FS as FileSynchronizer

    Caller->>FLM: createFile(path, fileType)
    FLM->>FS: allocateOnDisk(path)
    FS-->>FLM: ❌ FileAlreadyExistsException

    FLM-->>Caller: ❌ throw FileAlreadyExistsException
```

**Method signatures suy ra từ sequence:**
| Class | Method |
|---|---|
| `FileLifecycleManager` | `createFile(path: String, type: FileType): FileHandle` |
| `FileSynchronizer` | `allocateOnDisk(path: String): void` |
| `OpenFileManager` | `register(file: DataFile, mode: FileAccessMode): FileHandle` |
| `OpenFileTable` | `addEntry(file: DataFile): OpenFileEntry` |

---

## Operation 2: openFile()

**Kịch bản:** DBMS mở lại một file vật lý đã tồn tại để chuẩn bị đọc/ghi dữ liệu.

**Happy Path:**
```mermaid
sequenceDiagram
    autonumber
    actor Caller as Caller (BufferManager)
    participant FLM as FileLifecycleManager
    participant OFM as OpenFileManager
    participant OFT as OpenFileTable
    participant OFE as OpenFileEntry
    participant DF as DataFile

    Caller->>FLM: openFile(path, accessMode, lockMode)

    FLM->>OFM: isAlreadyOpen(path)
    OFM->>OFT: findEntry(path)
    OFT-->>OFM: null (chưa mở)
    OFM-->>FLM: false

    FLM->>DF: load(path)
    note over DF: Đọc metadata header của file<br/>từ hệ điều hành
    DF-->>FLM: dataFile (state=OPEN)

    FLM->>OFM: register(dataFile, accessMode, lockMode)
    OFM->>OFT: addEntry(dataFile, accessMode, lockMode)
    OFT->>OFE: new OpenFileEntry(dataFile, accessMode, lockMode)
    OFT-->>OFM: fileHandle
    OFM-->>FLM: fileHandle

    FLM-->>Caller: fileHandle
```

**Happy Path — File đã được mở trước đó (Reuse Handle):**
```mermaid
sequenceDiagram
    autonumber
    actor Caller as Caller (BufferManager)
    participant FLM as FileLifecycleManager
    participant OFM as OpenFileManager
    participant OFT as OpenFileTable

    Caller->>FLM: openFile(path, accessMode, lockMode)

    FLM->>OFM: isAlreadyOpen(path)
    OFM->>OFT: findEntry(path)
    OFT-->>OFM: existingEntry (đã có)
    OFM-->>FLM: true

    FLM->>OFM: getHandle(path)
    OFM->>OFT: findEntry(path)
    OFT-->>OFM: fileHandle
    OFM-->>FLM: fileHandle

    FLM-->>Caller: fileHandle (tái sử dụng)
    note over Caller,FLM: Không tạo OS file handle mới<br/>tránh lãng phí tài nguyên
```

**Sad Path — File không tồn tại:**
```mermaid
sequenceDiagram
    autonumber
    actor Caller as Caller (BufferManager)
    participant FLM as FileLifecycleManager
    participant DF as DataFile

    Caller->>FLM: openFile(path, accessMode, lockMode)
    FLM->>DF: load(path)
    DF-->>FLM: ❌ FileNotFoundException

    FLM-->>Caller: ❌ throw FileNotFoundException
```

**Method signatures suy ra từ sequence:**
| Class | Method |
|---|---|
| `FileLifecycleManager` | `openFile(path: String, mode: FileAccessMode, lock: FileLockMode): FileHandle` |
| `OpenFileManager` | `isAlreadyOpen(path: String): boolean` |
| `OpenFileManager` | `getHandle(path: String): FileHandle` |
| `OpenFileTable` | `findEntry(path: String): OpenFileEntry?` |
| `DataFile` | `load(path: String): DataFile` |

---

## Operation 3: deleteFile()

**Kịch bản:** DBMS xóa một file dữ liệu (ví dụ DROP TABLE). Cần đảm bảo file không còn ai đang mở trước khi xóa khỏi đĩa.

**Happy Path:**
```mermaid
sequenceDiagram
    autonumber
    actor Caller as Caller (TableManager)
    participant FLM as FileLifecycleManager
    participant OFM as OpenFileManager
    participant FS as FileSynchronizer

    Caller->>FLM: deleteFile(path)

    FLM->>OFM: isAlreadyOpen(path)
    OFM-->>FLM: false

    FLM->>FS: deleteFromDisk(path)
    FS-->>FLM: ok

    FLM-->>Caller: true (Success)
```

**Sad Path — Đang có người dùng:**
```mermaid
sequenceDiagram
    autonumber
    actor Caller as Caller (TableManager)
    participant FLM as FileLifecycleManager
    participant OFM as OpenFileManager

    Caller->>FLM: deleteFile(path)

    FLM->>OFM: isAlreadyOpen(path)
    OFM-->>FLM: true

    FLM-->>Caller: ❌ throw FileInUseException
```

**Method signatures suy ra từ sequence:**
| Class | Method |
|---|---|
| `FileLifecycleManager` | `deleteFile(path: String): boolean` |
| `FileSynchronizer` | `deleteFromDisk(path: String): void` |

---

## Operation 4: allocateSpace()

**Kịch bản:** Trang dữ liệu đã đầy, Page Manager gọi xuống xin thêm dung lượng (cấp phát mảng bytes mới) vào cuối file vật lý.

**Happy Path:**
```mermaid
sequenceDiagram
    autonumber
    actor Caller as Caller (PageManager)
    participant FLM as FileLifecycleManager
    participant OFT as OpenFileTable
    participant FS as FileSynchronizer

    Caller->>FLM: allocateSpace(fileHandle, sizeInBytes)

    FLM->>OFT: validateHandle(fileHandle)
    OFT-->>FLM: ok

    FLM->>FS: expandFile(fileHandle, sizeInBytes)
    FS-->>FLM: newOffset (Long)

    FLM-->>Caller: newOffset
```

**Sad Path — Hết dung lượng đĩa:**
```mermaid
sequenceDiagram
    autonumber
    actor Caller as Caller (PageManager)
    participant FLM as FileLifecycleManager
    participant FS as FileSynchronizer

    Caller->>FLM: allocateSpace(fileHandle, sizeInBytes)
    FLM->>FS: expandFile(fileHandle, sizeInBytes)
    FS-->>FLM: ❌ OutOfSpaceException

    FLM-->>Caller: ❌ throw OutOfSpaceException
```

**Method signatures suy ra từ sequence:**
| Class | Method |
|---|---|
| `FileLifecycleManager` | `allocateSpace(handle: FileHandle, size: Long): Long` |
| `OpenFileTable` | `validateHandle(handle: FileHandle): boolean` |
| `FileSynchronizer` | `expandFile(handle: FileHandle, size: Long): Long` |
