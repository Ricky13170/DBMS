# DBMS Layer 1: Architecture Overview

This document provides a high-level overview of the DBMS architecture. The system is decomposed into 8 core global domains.

## Mindmap Representation

The quickest way to grasp the scale of the system.

```mermaid
mindmap
  root((DBMS))
    Storage Engine
    Query Processing
    Transaction & Concurrency
    Security
    Database Object & Metadata
    Administration
    Backup, Recovery & Logging
    Communication & Connectivity
```

## Flowchart Representation

A top-down structure representing dependency resolution.

```mermaid
flowchart TD
    DBMS[DBMS Architecture]
    
    DBMS --> SE[Storage Engine]
    DBMS --> QP[Query Processing]
    DBMS --> TC[Transaction & Concurrency]
    DBMS --> SEC[Security]
    DBMS --> DOM[Database Object & Metadata]
    DBMS --> ADMIN[Administration]
    DBMS --> BRL[Backup, Recovery & Logging]
    DBMS --> NET[Communication & Connectivity]
    
    style DBMS fill:#2d3436,color:#ffffff,stroke:#0984e3,stroke-width:4px
```

---

## High-level Class Diagram (Layer 1)

Thể hiện 8 hệ thống con như các class (chưa có methods) và các mối quan hệ phụ thuộc giữa chúng ở cấp độ Layer 1.

```mermaid
classDiagram
    direction TB

    class DBMS

    class StorageEngine {
        <<subsystem>>
    }
    class QueryProcessing {
        <<subsystem>>
    }
    class TransactionConcurrency {
        <<subsystem>>
    }
    class Security {
        <<subsystem>>
    }
    class DatabaseObjectMetadata {
        <<subsystem>>
    }
    class Administration {
        <<subsystem>>
    }
    class BackupRecoveryLogging {
        <<subsystem>>
    }
    class CommunicationConnectivity {
        <<subsystem>>
    }

    %% DBMS owns all subsystems
    DBMS *-- StorageEngine
    DBMS *-- QueryProcessing
    DBMS *-- TransactionConcurrency
    DBMS *-- Security
    DBMS *-- DatabaseObjectMetadata
    DBMS *-- Administration
    DBMS *-- BackupRecoveryLogging
    DBMS *-- CommunicationConnectivity

    %% Cross-subsystem dependencies
    QueryProcessing --> StorageEngine
    QueryProcessing --> DatabaseObjectMetadata
    TransactionConcurrency --> StorageEngine
    BackupRecoveryLogging --> StorageEngine
    CommunicationConnectivity --> QueryProcessing
    CommunicationConnectivity --> Security
    Security --> DatabaseObjectMetadata
    Administration --> StorageEngine
```
