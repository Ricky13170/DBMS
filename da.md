# Class Diagram Level 1 — DBMS High-Level Architecture

Sơ đồ thể hiện **8 module chính** và mối quan hệ giữa chúng ở mức tổng quan.

> **Relationship legend:**
> - `*--` Composition (DBMS sở hữu module)
> - `-->` Association (phụ thuộc thường xuyên)
> - `..>` Dependency (dùng tạm thời)

---

```mermaid
classDiagram
    direction LR

    class DBMS {
    }

    class CommunicationConnectivity {
        Communication and Connectivity
    }

    class Security {
    }

    class Administration {
    }

    class QueryProcessing {
        Query Processing
    }

    class TransactionConcurrency {
        Transaction and Concurrency
    }

    class BackupRecoveryLogging {
        Backup, Recovery and Logging
    }

    class StorageEngine {
        Storage Engine
    }

    class DatabaseObjectsMetadata {
        Database Objects and Metadata
    }

    %% --- DBMS Composition (explicit diamonds) ---
    DBMS *-- CommunicationConnectivity
    DBMS *-- Security
    DBMS *-- Administration
    DBMS *-- QueryProcessing
    DBMS *-- TransactionConcurrency
    DBMS *-- BackupRecoveryLogging
    DBMS *-- StorageEngine
    DBMS *-- DatabaseObjectsMetadata

    %% --- Main request pipeline ---
    CommunicationConnectivity --> QueryProcessing : dispatches request

    %% --- Security cross-cutting ---
    CommunicationConnectivity ..> Security : authenticates
    QueryProcessing ..> Security : checks privilege

    %% --- Query to lower layers ---
    QueryProcessing ..> TransactionConcurrency : acquires lock
    QueryProcessing --> StorageEngine : reads/writes data
    QueryProcessing ..> DatabaseObjectsMetadata : catalog lookup

    %% --- Transaction to WAL ---
    TransactionConcurrency --> BackupRecoveryLogging : WAL log

    %% --- Administration support ---
    Administration ..> QueryProcessing : supplies statistics
    Administration ..> StorageEngine : vacuum, rebuild index

    %% --- Metadata support ---
    DatabaseObjectsMetadata ..> StorageEngine : schema for record layout
    DatabaseObjectsMetadata ..> BackupRecoveryLogging : object dependency on restore
```

---

## Tổng hợp Relationships

| Từ | Đến | Loại | Ý nghĩa |
|---|---|---|---|
| `DBMS` | `Communication & Connectivity` | Composition | DBMS sở hữu |
| `DBMS` | `Security` | Composition | DBMS sở hữu |
| `DBMS` | `Administration` | Composition | DBMS sở hữu |
| `Communication & Connectivity` | `Query Processing` | Association | Entry point của mọi request |
| `Communication & Connectivity` | `Security` | Dependency | Xác thực khi connect |
| `Query Processing` | `Security` | Dependency | Kiểm tra quyền truy cập object |
| `Query Processing` | `Transaction & Concurrency` | Dependency | Xin lock, đọc MVCC snapshot |
| `Query Processing` | `Storage Engine` | Association | Đọc/ghi dữ liệu thực sự |
| `Query Processing` | `Database Objects & Metadata` | Dependency | Tra cứu catalog, statistics |
| `Transaction & Concurrency` | `Backup, Recovery & Logging` | Association | WAL trước mỗi thay đổi |
| `Administration` | `Query Processing` | Dependency | Cung cấp statistics cho optimizer |
| `Administration` | `Storage Engine` | Dependency | Vacuum, rebuild index, collect stats |
| `Database Objects & Metadata` | `Storage Engine` | Dependency | Schema để layout record |
| `Database Objects & Metadata` | `Backup, Recovery & Logging` | Dependency | Object dependency khi restore |
