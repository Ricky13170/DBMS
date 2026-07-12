# Class Diagram Level 1 — DBMS High-Level Architecture

Sơ đồ thể hiện **8 module chính** và mối quan hệ giữa chúng ở mức tổng quan.  
Không đi vào chi tiết method/property — đó là phần của Class Diagram Level 2 (chi tiết từng nhánh).

> **Relationship legend:**
> - `<|--` Inheritance
> - `<|..` Realization (implement interface)
> - `*--` Composition
> - `o--` Aggregation
> - `-->` Association / uses
> - `..>` Dependency

---

## Mermaid Class Diagram

```mermaid
classDiagram

    %% ─────────────────────────────────────────
    %% 8 MODULE CHÍNH
    %% ─────────────────────────────────────────

    class CommunicationConnectivity {
        <<module>>
    }

    class QueryProcessing {
        <<module>>
    }

    class TransactionConcurrency {
        <<module>>
    }

    class Security {
        <<module>>
    }

    class DatabaseObjectMetadata {
        <<module>>
    }

    class StorageEngine {
        <<module>>
    }

    class BackupRecoveryLogging {
        <<module>>
    }

    class Administration {
        <<module>>
    }

    %% ─────────────────────────────────────────
    %% INTERFACES TRUNG TÂM
    %% ─────────────────────────────────────────

    class IAccessMethod {
        <<interface>>
    }

    class IWALManager {
        <<interface>>
    }

    class IFileManager {
        <<interface>>
    }

    %% ─────────────────────────────────────────
    %% RELATIONSHIPS
    %% ─────────────────────────────────────────

    %% Entry point: mọi request đi qua Communication
    CommunicationConnectivity --> QueryProcessing : "dispatches request"
    CommunicationConnectivity ..> Security : "authenticates on connect"

    %% Query pipeline
    QueryProcessing ..> DatabaseObjectMetadata : "resolves names, reads catalog & stats"
    QueryProcessing ..> Security : "checks object privileges & RLS"
    QueryProcessing --> StorageEngine : "reads/writes records"
    QueryProcessing ..> TransactionConcurrency : "acquires locks, reads MVCC snapshot"

    %% Storage Engine dùng interfaces
    StorageEngine --> IAccessMethod : "delegates index/heap scan"
    StorageEngine --> IFileManager : "swaps pages to disk"
    StorageEngine --> IWALManager : "WAL before dirty write"

    %% Transaction phối hợp với WAL
    TransactionConcurrency --> IWALManager : "logs every state change"

    %% Backup dùng WAL và checkpoint
    BackupRecoveryLogging o-- IWALManager : "replays log for recovery"
    BackupRecoveryLogging o-- StorageEngine : "snapshots data files"

    %% Administration hỗ trợ ngang
    Administration o-- StorageEngine : "vacuum, index rebuild, statistics"
    Administration o-- QueryProcessing : "supplies updated statistics to optimizer"

    %% Metadata là nền tảng chung
    DatabaseObjectMetadata o-- StorageEngine : "provides schema to layout records"
```

---

## Mối quan hệ chính giải thích

| Relationship | Loại | Ý nghĩa |
|---|---|---|
| `CommunicationConnectivity → QueryProcessing` | Association | Mọi request đều đi qua đây trước |
| `QueryProcessing ..> DatabaseObjectMetadata` | Dependency | Tra cứu catalog khi validate & optimize |
| `QueryProcessing → StorageEngine` | Association | Query thực sự đọc/ghi data ở đây |
| `QueryProcessing ..> TransactionConcurrency` | Dependency | Xin lock, đọc MVCC version trong lúc execute |
| `StorageEngine → IAccessMethod` | Association | Strategy pattern — B+Tree hay HeapScan |
| `StorageEngine → IWALManager` | Association | WAL rule: log trước, ghi sau |
| `TransactionConcurrency → IWALManager` | Association | Mọi BEGIN/COMMIT/ROLLBACK phải log |
| `BackupRecoveryLogging o-- IWALManager` | Aggregation | Recovery đọc lại log, không sở hữu |
| `Administration o-- StorageEngine` | Aggregation | DBA tools: vacuum, rebuild, stats |
| `DatabaseObjectMetadata o-- StorageEngine` | Aggregation | Schema metadata cho record layout |
