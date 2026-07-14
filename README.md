# DBMS — Database Management System

A modular, SOLID-compliant Database Management System designed with a top-down architecture approach.
The system is decomposed into 8 core subsystems, each designed with clear interfaces, entities, and service classes following OOP best practices.

---

## Architecture Overview

### Layer 1 — System Domains

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

---

## Design Principles

| Principle | Application |
|---|---|
| **SOLID** | Each class has a single responsibility; interfaces are segregated by functionality |
| **ISP** | Fat interfaces split into focused interfaces (e.g., `IFileReader`, `IFileWriter`, `IFileSynchronizer`) |
| **DIP** | High-level modules depend on abstractions, not concrete implementations |
| **Design Patterns** | Facade, Template Method, Strategy, Composite, Iterator used per module |

---

## Project Structure

```text
DBMS/
├── docs/
│   ├── architecture/       ← Layer 1-4 design diagrams
│   └── sequence_diagrams/  ← Key operation sequence diagrams
├── src/                    ← Implementation source code
└── tests/
    ├── unit/
    └── integration/
```

---

## Documentation

- [Layer 3 Component Breakdown](docs/architecture/layer3_components.md)
- [Storage Engine — File Manager (Detailed)](docs/04_class_detail_file_management.md)
