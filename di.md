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
