# Storage Engine — Layer 2 Class Diagram (Interfaces & Dependencies)

This diagram is an expanded version of Layer 1, clearly illustrating the Methods, Properties, and Dependency Injection flows through Constructors between classes. This diagram accurately reflects the structure of the `Layer_2/storage_engine/storage_core.py` source file.

```mermaid
classDiagram
    direction TB
    
    class FileManager {
        -_open_files: dict[int, int]
        -_get_file_handle(file_id: int) int
        +create_file(file_path: str, file_id: int) bool
        +open_file(file_path: str, file_id: int) bool
        +close_file(file_id: int) bool
        +read_block(file_id: int, block_id: int) bytes
        +write_block(file_id: int, block_id: int, data: bytes) bool
    }

    class StorageAllocation {
        +file_manager: FileManager
    }
    
    class PageManager {
        +file_manager: FileManager
        +format_page(page_id: int) bool
    }

    class BufferManager {
        +page_manager: PageManager
        +buffer_pool: dict
        +pin_page(page_id: int) bool
        +unpin_page(page_id: int, is_dirty: bool) bool
        +flush_all() bool
    }

    class RecordManager {
        +buffer_manager: BufferManager
        +insert_record(page_id: int, data: bytes) int
        +read_record(page_id: int, slot_id: int) bytes
        +delete_record(page_id: int, slot_id: int) bool
    }

    class AccessMethods {
        +buffer_manager: BufferManager
        +record_manager: RecordManager
    }

    class StorageEngine {
        +file_manager: FileManager
        +storage_allocation: StorageAllocation
        +page_manager: PageManager
        +buffer_manager: BufferManager
        +record_manager: RecordManager
        +access_methods: AccessMethods
    }
    
    %% Facade acts as the central container (Composition)
    StorageEngine *-- FileManager
    StorageEngine *-- StorageAllocation
    StorageEngine *-- PageManager
    StorageEngine *-- BufferManager
    StorageEngine *-- RecordManager
    StorageEngine *-- AccessMethods
    
    %% Dependency Injection Relationships (Via Constructor)
    StorageAllocation --> FileManager : [Inject] Requests Disk File I/O
    PageManager --> FileManager : [Inject] Reads/Writes Page Data
    BufferManager --> PageManager : [Inject] Formats Page Structures
    RecordManager --> BufferManager : [Inject] Retrieves Page from RAM
    AccessMethods --> BufferManager : [Inject] Reads Index Pages
    AccessMethods --> RecordManager : [Inject] Handles Record Logic Constraints
```
