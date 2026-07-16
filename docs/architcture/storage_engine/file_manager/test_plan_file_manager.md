# Test Plan & TDD Design: File Manager

This document defines the automated testing architecture for the **File Manager** sub-module, bridging the technical concepts established in Layer 4 (Class Detail) and Sequence Diagrams seamlessly into actionable TDD (Test-Driven Development) execution.

---

## 1. Directory Structure (GitHub Repository)
To cleanly isolate domain boundaries, the testing suite separates logics dynamically simulating disk operations (Unit Tests using Mocking) versus implicitly executing live hardware OS drivers (Integration Tests).

```text
DBMS/
│
├── src/storage_engine/file_manager/          # Functional source code
│   ├── interfaces/
│   ├── enums/
│   ├── entities/
│   └── services/
│
└── tests/
    ├── unit_tests/file_manager/              # MOCKED OS - Extremely fast
    │   ├── test_file_lifecycle_manager.py
    │   ├── test_open_file_manager.py
    │   └── test_file_io.py
    │
    └── integration_tests/file_manager/       # REAL DISK OS I/O - Requires teardown
        └── test_physical_file_integration.py
```

---

## 2. Unit Test Scenarios (Mocked Dependencies)
*Strategy: Utilize Python's `unittest.mock` strictly isolating the focal class, verifying internal function matrix execution logic correctly without touching the actual hard drive.*

### Target: `test_file_lifecycle_manager.py` (Testing `FileLifecycleManager`)
| ID | Behavior Spec (TDD) | Given (Context / Setup) | When (Trigger) | Then (Assertion) |
|---|---|---|---|---|
| UT-FLM-01 | Happy Create | Mocked OS reports `OK` on allocation bounds | call `create_file(path)` | Returns valid `FileHandle`, calls `.register()` inside OpenFileMgr |
| UT-FLM-02 | Sad Create (Exists) | Mocked OS throws `FileAlreadyExists` | call `create_file(path)` | Throws Exception immediately, NEVER calls `.register()` down the line |
| UT-FLM-03 | Happy Delete | Mocked OpenFileMgr returns `false` (No users) | call `delete_file(path)` | Returns `True`, calls Mocked OS delete command successfully |
| UT-FLM-04 | Sad Delete (In Use) | Mocked OpenFileMgr returns `true` (In use) | call `delete_file(path)` | Throws `FileInUseException`, OS delete is NEVER called |

### Target: `test_open_file_manager.py` (Testing `OpenFileManager`)
| ID | Behavior Spec (TDD) | Given (Context / Setup) | When (Trigger) | Then (Assertion) |
|---|---|---|---|---|
| UT-OFM-01 | Fresh File Registration | `OpenFileTable` is entirely empty | call `register(dataFile)` | Creates `OpenFileEntry`, sets open_count = 1, returns new Handle |
| UT-OFM-02 | Handle Limit Breached | `OpenFileTable` holds Maximum active instances | call `register(dataFile)` | Throws `MaxOpenFilesExceededException` aggressively |
| UT-OFM-03 | Releasing Handle | `open_count` is initially 2 | call `release_handle(id)` | Drops count to 1, Table Entry is NOT purged functionally |
| UT-OFM-04 | Auto-Evict Handle | `open_count` is 1 | call `release_handle(id)` | Count drops 0, structurally REMOVES Entry bridging Memory clean-up |

---

## 3. Integration Test Scenarios (Real OS Interaction)
*Strategy: Executing actual physical Operating System file bindings bypassing mocking completely, simulating absolute true system limits.*

### Target: `test_physical_file_integration.py`
| ID | Behavior Spec | Execution Sequence Matrix | Target Assertion Limits |
|---|---|---|---|
| IT-FM-01 | End-to-End File Lifecycle | 1. `create_file("db.txt")` <br>2. `write_block("db.txt", data)` <br>3. `release_handle` <br>4. `open_file("db.txt")` <br>5. `read_block` <br>6. `release_handle` & `delete_file` | Read data successfully fetches matching physically appended characters verifying persistent ACID durability logic naturally. Delete ensures disk is wiped perfectly. |
| IT-FM-02 | Multi-Handle Concurrency | 1. Thread 1: `open_file("db.txt", EXCLUSIVE)` <br>2. Thread 2: `open_file("db.txt", READ_ONLY)` | Thread 2 request dynamically throws Exception asserting OS structural locks behave functionally correctly simulating database collision explicitly. |
