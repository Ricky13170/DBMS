# Test Plan & TDD Design: File Manager

This document defines the automated testing architecture for the **File Manager** sub-module, bridging the technical concepts established in Layer 4 (Class Detail) and Sequence Diagrams seamlessly into actionable TDD (Test-Driven Development) execution.

---

---

## 1. Unit Test Scenarios (Mocked Dependencies)
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

### Target: `test_file_io.py` (Testing `FileReader` & `FileWriter`)
| ID | Behavior Spec (TDD) | Given (Context / Setup) | When (Trigger) | Then (Assertion) |
|---|---|---|---|---|
| UT-IO-01 | Write Valid Block | Handle is valid and has WRITE Mode | call `write_block(handle, offset, data)` | OS write called exactly correlating offset and byte injection |
| UT-IO-02 | Write Invalid Handle | Handle is closed or READ_ONLY Mode | call `write_block(...)` | Throws `InvalidHandleException` preventing manipulation |
| UT-IO-03 | Read Valid Block | Handle is valid and has READ Mode | call `read_block(handle, offset, size)` | Returns correct byte array directly bridged from Mocked OS |
| UT-IO-04 | Read Out of Bounds | Request offset+size logically exceeds EOF | call `read_block(...)` | Triggers OS crash interception returning `EOFException` |

### Target: `test_file_synchronizer.py` (Testing `FileSynchronizer`)
| ID | Behavior Spec (TDD) | Given (Context / Setup) | When (Trigger) | Then (Assertion) |
|---|---|---|---|---|
| UT-SYNC-01 | Valid Expansion | OS has sufficient physical free space | call `expand_file(handle, size)` | Appends null padding bytes sequentially, returning new EOF offset boundary |
| UT-SYNC-02 | Expansion Fails | OS throws insufficient disk space alert | call `expand_file(handle, size)` | Intercepts OS code translating into logical `OutOfSpaceException` |
| UT-SYNC-03 | Flush Dirty Buffers | Handle has active memory unflushed blocks | call `fsync(handle)` | Explicitly fires `fsync()` kernel bypassing OS caching completely (ACID Durability) |

---

## 2. Integration Test Scenarios (Real OS Interaction)
*Strategy: Executing actual physical Operating System file bindings bypassing mocking completely, simulating absolute true system limits.*

### Target: `test_physical_file_integration.py`
| ID | Behavior Spec | Execution Sequence Matrix | Target Assertion Limits |
|---|---|---|---|
| IT-FM-01 | End-to-End File Lifecycle | 1. `create_file("db.txt")` <br>2. `write_block("db.txt", data)` <br>3. `release_handle` <br>4. `open_file("db.txt")` <br>5. `read_block` <br>6. `release_handle` & `delete_file` | Read data successfully fetches matching physically appended characters verifying persistent ACID durability logic naturally. Delete ensures disk is wiped perfectly. |
| IT-FM-02 | Multi-Handle Concurrency | 1. Thread 1: `open_file("db.txt", EXCLUSIVE)` <br>2. Thread 2: `open_file("db.txt", READ_ONLY)` | Thread 2 request dynamically throws Exception asserting OS structural locks behave functionally correctly simulating database collision explicitly. |
