# Storage Engine — Layer 1 Class Diagram

Sơ đồ này thể hiện cấu trúc Layer 1 của riêng khối Storage Engine, nơi mà `StorageEngineFacade` đóng vai trò là container chứa (Composition) 6 thành phần con, hoàn toàn khớp với file source code `storage_core.py` mà bạn đang mở.

```mermaid
classDiagram
    direction TB
    
    class StorageEngineFacade {
        <<Facade / Orchestrator>>
    }

    class FileManager
    class PageManager
    class BufferManager
    class RecordManager
    class AccessMethods
    class StorageAllocation

    %% Thể hiện quan hệ Composition (StorageEngineFacade rỗng chứa các sub-class)
    StorageEngineFacade *-- FileManager
    StorageEngineFacade *-- PageManager
    StorageEngineFacade *-- BufferManager
    StorageEngineFacade *-- RecordManager
    StorageEngineFacade *-- AccessMethods
    StorageEngineFacade *-- StorageAllocation
```
