# High-Level Class Diagram: File Manager

This diagram illustrates the macro-architectural view specifically isolated for the **File Manager** subsystem.
*Note: Properties and Methods are intentionally hidden to explicitly feature dependencies, composition, and inheritance structures prior to establishing Sequence boundaries.*

```mermaid
classDiagram
    direction TB
    
    %% -------------------------------------
    %% INTERFACES (CONTRACTS)
    %% -------------------------------------
    class IFileLifecycleManager {
        <<interface>>
    }
    class IPageIOInterface {
        <<interface>>
    }
    class IFileDescriptorManager {
        <<interface>>
    }
    class IOSFileWrapper {
        <<interface>>
    }

    %% -------------------------------------
    %% ENUMERATIONS
    %% -------------------------------------
    class FileAccessMode {
        <<enumeration>>
    }
    class GrowthStrategy {
        <<enumeration>>
    }

    %% -------------------------------------
    %% DOMAIN ENTITIES
    %% -------------------------------------
    class DataFile {
        <<entity>>
    }
    class PagePointer {
        <<entity>>
    }
    
    %% -------------------------------------
    %% IMPLEMENTATIONS (MANAGERS & WRAPPERS)
    %% -------------------------------------
    class FileLifecycleManager {
        <<service>>
    }
    class PageIOManager {
        <<service>>
    }
    class FileDescriptorManager {
        <<service>>
    }
    class FileGrowthManager {
        <<service>>
    }
    class OSFileWrapper {
        <<utility>>
    }
    
    %% -------------------------------------
    %% STRUCTURAL RELATIONSHIPS
    %% -------------------------------------
    
    %% Interface Realization
    FileLifecycleManager ..|> IFileLifecycleManager
    PageIOManager ..|> IPageIOInterface
    FileDescriptorManager ..|> IFileDescriptorManager
    OSFileWrapper ..|> IOSFileWrapper
    
    %% Service Dependencies (Delegations)
    FileLifecycleManager --> FileDescriptorManager : registers/closes handles
    FileLifecycleManager --> FileGrowthManager : delegates expansion config
    FileLifecycleManager --> OSFileWrapper : physical OS calls

    PageIOManager --> FileDescriptorManager : fetches open handles
    PageIOManager --> OSFileWrapper : raw byte I/O
    
    %% Entity Composition & Usage
    DataFile *-- PagePointer : Maps logic bounds
    DataFile --> FileAccessMode : Has rules
    DataFile --> GrowthStrategy : Defines expansion limit

    FileLifecycleManager ..> DataFile : Orchestrates logic state
```
