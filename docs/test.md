# DBMS — Database Management System

A modular, SOLID-compliant Database Management System designed with a top-down architecture approach.
The system is decomposed into 10 core subsystems, each designed with clear interfaces, entities, and service classes following OOP best practices.

---

## Architecture Overview
```mermaid
mindmap
  root((DBMS Core))
    ClientInterface
    QueryProcessing
    DatabaseManagement
    StorageEngine
    TransactionConcurrency
    SecurityManagement
    BackupRecoveryLogging
    Administration
    PerformanceManagement
    CommunicationConnectivity
```

### Layer 1 — System Domains

```mermaid
classDiagram
    direction TB
    
    class DBMS {
    }

    DBMS *-- ClientInterface
    DBMS *-- QueryProcessing
    DBMS *-- DatabaseManagement
    DBMS *-- StorageEngine
    DBMS *-- TransactionConcurrency
    DBMS *-- SecurityManagement
    DBMS *-- Administration
    DBMS *-- BackupRecoveryLogging
    DBMS *-- PerformanceManagement
    DBMS *-- CommunicationConnectivity
    
    ClientInterface --> QueryProcessing
    QueryProcessing --> DatabaseManagement
    QueryProcessing --> StorageEngine
    QueryProcessing --> TransactionConcurrency
    QueryProcessing --> SecurityManagement
    DatabaseManagement --> SystemCatalog
    DatabaseManagement --> StorageEngine
    TransactionConcurrency --> StorageEngine
    TransactionConcurrency --> BackupRecoveryLogging
    BackupRecoveryLogging --> StorageEngine
    PerformanceManagement --> QueryProcessing
    PerformanceManagement --> StorageEngine
    PerformanceManagement --> TransactionConcurrency
    Administration --> SecurityManagement
    Administration --> BackupRecoveryLogging
    Administration --> PerformanceManagement

```

---

## Design Principles

| Principle | Application |
|---|---|
| **SOLID** | Each class has a single responsibility; interfaces are segregated by functionality |
| **ISP** | Fat interfaces split into focused interfaces (e.g., `IFileReader`, `IFileWriter`, `IFileSynchronizer`) |
| **DIP** | High-level modules depend on abstractions, not concrete implementations |
| **Design Patterns** | Facade, Template Method, Strategy, Composite, Iterator used per module |

---
