# File Management — Sequence Diagrams

> **Methodology:** Bottom-up approach — handle small operations first, then aggregate them up to the Feature-level.
>
> **Participants extracted from Layer 4 File Manager:**
> - `FileLifecycleManager` (Facade — F1)
> - `OpenFileManager` (F2)
> - `OpenFileTable` / `OpenFileEntry` / `FileHandle` (F2 Entities)
> - `DataFile` (F1 Entity)
> - `FileSynchronizer` (F4)
> - `FileReader` / `FileWriter` (F3)

---

## Operation 1: createFile()

**Scenario:** The DBMS needs to create a new physical data file (e.g., when creating a new Table).

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

**Sad Path — File already exists:**
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

**Inferred Method Signatures:**
| Class | Method |
|---|---|
| `FileLifecycleManager` | `createFile(path: String, type: FileType): FileHandle` |
| `FileSynchronizer` | `allocateOnDisk(path: String): void` |
| `OpenFileManager` | `register(file: DataFile, mode: FileAccessMode): FileHandle` |
| `OpenFileTable` | `addEntry(file: DataFile): OpenFileEntry` |

---

## Operation 2: openFile()

**Scenario:** The DBMS reopens an existing physical file to prepare for read/write operations.

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
    OFT-->>OFM: null (not opened yet)
    OFM-->>FLM: false

    FLM->>DF: load(path)
    note over DF: Reads the file metadata header<br/>from the operating system
    DF-->>FLM: dataFile (state=OPEN)

    FLM->>OFM: register(dataFile, accessMode, lockMode)
    OFM->>OFT: addEntry(dataFile, accessMode, lockMode)
    OFT->>OFE: new OpenFileEntry(dataFile, accessMode, lockMode)
    OFT-->>OFM: fileHandle
    OFM-->>FLM: fileHandle

    FLM-->>Caller: fileHandle
```

**Happy Path — File was already opened (Reuse Handle):**
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
    OFT-->>OFM: existingEntry (already exists)
    OFM-->>FLM: true

    FLM->>OFM: getHandle(path)
    OFM->>OFT: findEntry(path)
    OFT-->>OFM: fileHandle
    OFM-->>FLM: fileHandle

    FLM-->>Caller: fileHandle (reused)
    note over Caller,FLM: Does not create a new OS file handle<br/>to avoid resource waste
```

**Sad Path — File does not exist:**
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

**Inferred Method Signatures:**
| Class | Method |
|---|---|
| `FileLifecycleManager` | `openFile(path: String, mode: FileAccessMode, lock: FileLockMode): FileHandle` |
| `OpenFileManager` | `isAlreadyOpen(path: String): boolean` |
| `OpenFileManager` | `getHandle(path: String): FileHandle` |
| `OpenFileTable` | `findEntry(path: String): OpenFileEntry?` |
| `DataFile` | `load(path: String): DataFile` |

---

## Operation 3: deleteFile()

**Scenario:** The DBMS deletes a data file (e.g., DROP TABLE). It must ensure no one is currently opening the file before physical disk deletion.

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

**Sad Path — File is currently in use:**
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

**Inferred Method Signatures:**
| Class | Method |
|---|---|
| `FileLifecycleManager` | `deleteFile(path: String): boolean` |
| `FileSynchronizer` | `deleteFromDisk(path: String): void` |

---

## Operation 4: allocateSpace()

**Scenario:** A data page is full, the Page Manager calls down to request additional capacity (allocating a new byte array) at the end of the physical file.

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

**Sad Path — Out of Disk Space:**
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

**Inferred Method Signatures:**
| Class | Method |
|---|---|
| `FileLifecycleManager` | `allocateSpace(handle: FileHandle, size: Long): Long` |
| `OpenFileTable` | `validateHandle(handle: FileHandle): boolean` |
| `FileSynchronizer` | `expandFile(handle: FileHandle, size: Long): Long` |
