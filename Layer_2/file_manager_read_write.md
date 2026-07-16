# Sequence Diagram: File Manager (Read / Write Blocks)

This diagram details the interactions of the `FileManager` when receiving Read/Write Data requests from higher layers (typically `PageManager` or `BufferManager`) down to the Operating System (OS). By analyzing this diagram, we can easily identify IO/File lock risks to design appropriate Test Cases.

```mermaid
sequenceDiagram
    participant PM as Target Caller (e.g., PageManager)
    participant FM as FileManager
    participant OS as Operating System / HDD

    %% --------- READ FILE SCENARIO ---------
    rect rgb(235, 245, 255)
    Note over PM,OS: Scenario 1: Read a Block (Page) from Disk
    PM->>FM: read_block(file_id, block_id)
    
    %% Check handle
    FM->>FM: Resolve file_descriptor = get_file_handle(file_id)
    alt If Handle Does Not Exist (File not opened)
        FM->>OS: open(file_path, mode='rb')
        OS-->>FM: file_descriptor
        FM->>FM: Cache file_descriptor in Open Files Map
    end
    
    %% Seek pointer and Read
    FM->>OS: os.lseek(file_descriptor, block_id * PAGE_SIZE)
    FM->>OS: os.read(file_descriptor, PAGE_SIZE)
    
    alt Read Data Lost or Error (EOF, Bad Sector)
        OS-->>FM: Error or missing bytes
        FM-->>PM: throw IOError (Corrupted File)
    else Read Successful
        OS-->>FM: raw_bytes
        FM-->>PM: return raw_bytes
    end
    end

    %% --------- WRITE FILE SCENARIO ---------
    rect rgb(255, 245, 235)
    Note over PM,OS: Scenario 2: Write a Block (Page) to Disk
    PM->>FM: write_block(file_id, block_id, data_bytes)
    
    %% Check data and handle
    FM->>FM: Assert(len(data_bytes) == PAGE_SIZE)
    FM->>FM: Resolve file_descriptor = get_file_handle(file_id)
    
    alt Handle Does Not Exist
        FM->>OS: open(file_path, mode='r+b') (Read/Write)
        OS-->>FM: file_descriptor
    end
    
    %% Write
    FM->>OS: os.lseek(file_descriptor, block_id * PAGE_SIZE)
    FM->>OS: os.write(file_descriptor, data_bytes)
    OS-->>FM: bytes_written
    
    %% Ensure disk sync (Optional fsync config)
    opt fsync() forced configuration
        FM->>OS: os.fsync(file_descriptor)
        OS-->>FM: Flush confirmation
    end
    
    FM-->>PM: return True (Success)
    end
```
