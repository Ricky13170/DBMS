# Tham số Thiết kế: DBMS Class Breakdown (Layer 4 - Không Methods)
Tài liệu này định nghĩa các Object tham gia vào hệ thống, được phân loại nghiêm ngặt theo các chuẩn:
- **Enums**: File cấu hình hằng số
- **Entities**: Lớp dữ liệu thuần túy không chứa logic (DTO, POJO, Data structures)
- **Interfaces**: Hợp đồng giao tiếp (Tuân thủ ISP)
- **Abstract Classes**: Lớp cơ sở chứa logic dùng chung (Tuân thủ Template Method)
- **Classes**: Các lớp thực thi nghiệp vụ (Tuân thủ SRP)

---

## 1. STORAGE ENGINE

### 1.1 File Management
```text
File Management
├── Enums
│   ├── FileType (DATA, LOG, TEMP)
│   ├── FileState (OPEN, CLOSED, CORRUPTED)
│   ├── FileAccessMode (READ, WRITE, APPEND)
│   ├── FileLockMode (SHARED, EXCLUSIVE)
│   └── AllocationStatus (ALLOCATED, FREE)
├── Entities
│   ├── DataFile
│   ├── OpenFileTable
│   ├── OpenFileEntry
│   └── FileHandle
├── Interfaces
│   ├── IFileLifecycleManager  -- create/delete/rename
│   ├── IFileReader            -- read block
│   ├── IFileWriter            -- write block
│   ├── IFileSynchronizer      -- fsync/flush
│   ├── IExtentManager         -- manage extents
│   └── IOpenFileManager       -- manage file handles
├── Abstract Classes
│   └── (None)
└── Classes
    ├── FileLifecycleManager
    ├── FileReader
    ├── FileWriter
    ├── FileSynchronizer
    ├── ExtentManager
    └── OpenFileManager
```

### 1.2 Page Management
```text
Page Management
├── Enums
│   ├── PageType (DATA, DIRECTORY, BLOB)
│   └── PageStatus (CLEAN, DIRTY, PINNED)
├── Entities
│   ├── GenericPage
│   ├── DataPage
│   ├── DirectoryPage
│   ├── PageHeader
│   └── PageSlot
├── Interfaces
│   ├── IPageFormatter         -- format new page
│   ├── IPageReader            -- read slots
│   ├── IPageWriter            -- write/update slots
│   └── IPageDefragmenter      -- compact space
├── Abstract Classes
│   └── AbstractPageFormatter
└── Classes
    ├── DataPageFormatter
    ├── DirectoryPageFormatter
    ├── PageReader
    ├── PageWriter
    └── PageDefragmenter
```

### 1.3 Buffer Management
```text
Buffer Management
├── Enums
│   └── ReplacementPolicyType (LRU, CLOCK, MRU)
├── Entities
│   ├── BufferFrame
│   ├── BufferPool
│   └── FrameStatistics
├── Interfaces
│   ├── IBufferPoolManager     -- get/pin/unpin pages
│   ├── IReplacementPolicy     -- choose victim
│   ├── IFlushController       -- background flush
│   └── IFrameAllocator        -- manage memory frames
├── Abstract Classes
│   └── AbstractReplacementPolicy
└── Classes
    ├── LRUReplacementPolicy
    ├── ClockReplacementPolicy
    ├── BufferPoolManager
    ├── FlushController
    └── FrameAllocator
```

### 1.4 Record Management
```text
Record Management
├── Enums
│   ├── RecordFormat (FIXED, VARIABLE)
│   └── SchemaType (INT, VARCHAR, DATE)
├── Entities
│   ├── RID (Record ID)
│   ├── Tuple
│   ├── Field
│   └── RecordSchema
├── Interfaces
│   ├── IRecordSerializer      -- Tuple <-> Bytes
│   ├── IRecordCRUD            -- insert/delete/update tuple
│   ├── ISchemaValidator       -- validate field types
│   └── IRecordLocator         -- find exact byte offset
├── Abstract Classes
│   └── AbstractRecordSerializer
└── Classes
    ├── FixedLengthSerializer
    ├── VariableLengthSerializer
    ├── RecordCRUDManager
    ├── SchemaValidator
    └── RecordLocator
```

### 1.5 Access Methods (Indexes)
```text
Access Methods
├── Enums
│   ├── IndexType (B_PLUS_TREE, HASH)
│   └── ScanDirection (FORWARD, BACKWARD)
├── Entities
│   ├── IndexKey
│   ├── BTreeNode
│   ├── HashBucket
│   └── ScanContext
├── Interfaces
│   ├── IAccessMethod          -- insert/delete/search index
│   ├── IIndexScanner          -- range scan
│   └── IIndexNodeSplitter     -- handle node overflow
├── Abstract Classes
│   └── AbstractTreeScanner
└── Classes
    ├── BPlusTreeIndex
    ├── HashIndex
    ├── BTreeScanner
    └── NodeSplitter
```

### 1.6 Space Allocation
```text
Space Allocation
├── Enums
│   └── SpaceSearchStrategy (FIRST_FIT, BEST_FIT)
├── Entities
│   ├── FreeSpaceMap (FSM)
│   ├── AllocationBitmap
│   └── ExtentTracker
├── Interfaces
│   ├── ISpaceAllocator        -- allocate pages
│   ├── ISpaceDeallocator      -- free pages
│   └── ISpaceSearcher         -- find free slots/pages
├── Abstract Classes
│   └── (None)
└── Classes
    ├── PageAllocator
    ├── FSMManager
    ├── BitmapManager
    └── BestFitSearcher
```

---

## 2. QUERY PROCESSING

### 2.1 SQL Parser & Semantic Analysis
```text
SQL Parser
├── Enums
│   ├── TokenType (KEYWORD, IDENTIFIER, LITERAL)
│   └── ASTNodeType (SELECT, INSERT, JOIN)
├── Entities
│   ├── Token
│   ├── AbstractSyntaxTree (AST)
│   ├── QueryContext
│   └── SemanticError
├── Interfaces
│   ├── ILexer                 -- string -> tokens
│   ├── IParser                -- tokens -> AST
│   ├── ISemanticValidator     -- AST -> Validated AST
│   └── ICatalogLookup         -- resolve tables/columns
├── Abstract Classes
│   └── AbstractSyntaxNode
└── Classes
    ├── SQLLexer
    ├── SQLParser
    ├── SemanticValidator
    └── CatalogLookupService
```

### 2.2 Query Optimizer
```text
Query Optimizer
├── Enums
│   ├── JoinStrategy (NESTED_LOOP, HASH, MERGE)
│   └── OptimizationGoal (COST, LATENCY)
├── Entities
│   ├── LogicalPlan
│   ├── PhysicalPlan
│   ├── CostMetrics
│   └── TableStatistics
├── Interfaces
│   ├── IPlanGenerator         -- AST -> Logical
│   ├── IRuleApplier           -- Relational algebra rules
│   ├── ICostEstimator         -- heuristic cost
│   └── IPhysicalPlanner       -- Logical -> Physical
├── Abstract Classes
│   ├── AbstractOptimizationRule
│   └── AbstractPhysicalOperator
└── Classes
    ├── HeuristicOptimizer
    ├── CostBasedOptimizer
    ├── FilterPushdownRule
    ├── JoinReorderRule
    └── PlanGenerator
```

### 2.3 Query Execution Engine
```text
Query Execution
├── Enums
│   └── ExecutionState (INIT, RUNNING, DONE, ERROR)
├── Entities
│   ├── ExecutionContext
│   └── OperatorState
├── Interfaces
│   ├── IExecutionEngine       -- execute PhysicalPlan
│   ├── IRelationalOperator    -- open/next/close (Volcano paradigm)
│   └── IPipelineManager       -- orchestrate operators
├── Abstract Classes
│   └── AbstractRelationalOperator
└── Classes
    ├── VolcanoExecutionEngine
    ├── NestedLoopJoinOp
    ├── HashJoinOp
    ├── SeqScanOp
    ├── IndexScanOp
    └── PipelineManager
```

---

## 3. TRANSACTION & CONCURRENCY

### 3.1 Transaction Manager
```text
Transaction Management
├── Enums
│   ├── TxStatus (ACTIVE, COMMITTED, ABORTED)
│   └── IsolationLevel (READ_COMMITTED, SERIALIZABLE)
├── Entities
│   ├── TransactionContext
│   ├── Savepoint
│   └── TxTableEntry
├── Interfaces
│   ├── ITxLifecycleManager    -- begin/commit/rollback
│   ├── ISavepointManager      -- set/release savepoints
│   └── ITxStateTracker        -- monitor states
├── Abstract Classes
│   └── (None)
└── Classes
    ├── TransactionManager
    ├── SavepointController
    └── TransactionTable
```

### 3.2 Lock Manager
```text
Lock Management
├── Enums
│   ├── LockMode (SHARED, EXCLUSIVE, INTENT)
│   └── DeadlockResolution (WAIT_DIE, WOUND_WAIT)
├── Entities
│   ├── LockRequest
│   ├── LockQueue
│   └── WaitGraph
├── Interfaces
│   ├── ILockingProtocol       -- acquire/release
│   ├── IDeadlockDetector      -- detect cycles
│   └── IVictimSelector        -- choose tx to abort
├── Abstract Classes
│   └── AbstractDeadlockPrevention
└── Classes
    ├── TwoPhaseLockingProtocol
    ├── LockTable
    ├── DeadlockDetector
    └── WoundWaitPolicy
```

### 3.3 MVCC Engine
```text
MVCC & Versioning
├── Enums
│   └── VersionStatus (VISIBLE, INVISIBLE, STALE)
├── Entities
│   ├── VersionRecord
│   ├── Snapshot
│   └── VersionChain
├── Interfaces
│   ├── IMVCCEngine            -- create versions
│   ├── IVisibilityChecker     -- check snapshot visibility
│   └── IGarbageCollector      -- clean stale versions
├── Abstract Classes
│   └── (None)
└── Classes
    ├── VersionManager
    ├── VisibilityChecker
    ├── SnapshotManager
    └── MVCCGarbageCollector
```

---

## 4. DATABASE OBJECT & METADATA

### 4.1 Catalog & Schema Management
```text
Catalog Manager
├── Enums
│   ├── ObjectType (TABLE, VIEW, INDEX, FUNC)
│   └── ColumnType (INT, VARCHAR, BOOLEAN)
├── Entities
│   ├── SchemaDef
│   ├── TableDef
│   ├── ColumnDef
│   └── ObjectMetadata
├── Interfaces
│   ├── ICatalogReader         -- Read metadata
│   ├── ICatalogWriter         -- Write/Update metadata
│   ├── IObjectLifecycle       -- create/drop operations
│   └── IConstraintValidator   -- PK/FK checking
├── Abstract Classes
│   └── (None)
└── Classes
    ├── SystemCatalog
    ├── ObjectLifecycleManager
    ├── ConstraintValidator
    └── TypeRegistry
```

---

## 5. SECURITY

### 5.1 Authentication & Authorization
```text
Security
├── Enums
│   ├── AuthMethod (PASSWORD, TOKEN)
│   ├── PrivilegeType (SELECT, INSERT, UPDATE)
│   └── RoleLevel (ADMIN, USER)
├── Entities
│   ├── UserAccount
│   ├── RoleDef
│   ├── SessionContext
│   └── AuditEvent
├── Interfaces
│   ├── IAuthenticator         -- verify credentials
│   ├── IAuthorizer            -- check permissions
│   ├── IPrivilegeGrantor      -- grant/revoke
│   └── IAuditLogger           -- write logs
├── Abstract Classes
│   ├── AbstractAuthMethod
│   └── AbstractSecurityPolicy
└── Classes
    ├── PasswordAuthenticator
    ├── RBACAuthorizer
    ├── PrivilegeManager
    └── AuditManager
```

---

## 6. ADMINISTRATION

### 6.1 Monitoring & Config
```text
Administration
├── Enums
│   ├── MetricType (CPU, MEMORY, IO)
│   └── AlertSeverity (INFO, WARNING, CRITICAL)
├── Entities
│   ├── SystemMetric
│   ├── AlertNotification
│   └── DBConfigMap
├── Interfaces
│   ├── IMetricsCollector      -- gather system stats
│   ├── IAlertNotifier         -- send warnings
│   ├── IConfigManager         -- hot reload parameters
│   └── ITaskScheduler         -- cron jobs
├── Abstract Classes
│   └── (None)
└── Classes
    ├── PerformanceCollector
    ├── AlertSystem
    ├── DynamicConfigManager
    └── BackgroundTaskScheduler
```

---

## 7. BACKUP & RECOVERY (LOGGING)

### 7.1 WAL & Recovery Manager
```text
Logging & Recovery
├── Enums
│   ├── BackupType (FULL, INCREMENTAL)
│   ├── LogOperation (INSERT, UPDATE, DELETE)
│   └── RecoveryMode (CRASH, PITR)
├── Entities
│   ├── LogSequenceNumber (LSN)
│   ├── LogRecord
│   ├── CheckpointRecord
│   └── BackupManifest
├── Interfaces
│   ├── IWALWriter             -- append log
│   ├── IWALReader             -- scan log
│   ├── IRecoveryEngine        -- redo/undo
│   ├── IBackupStrategy        -- export data
│   └── IRestoreStrategy       -- import data
├── Abstract Classes
│   └── AbstractBackupEngine
└── Classes
    ├── WALManager
    ├── CrashRecoveryEngine
    ├── PointInTimeRecovery
    ├── CheckpointCoordinator
    └── FullBackupEngine
```

---

## 8. COMMUNICATION & CONNECTIVITY

### 8.1 Network & Session
```text
Communication
├── Enums
│   ├── ProtocolType (TCP, UNIX_SOCKET)
│   └── ConnectionState (IDLE, ACTIVE, CLOSING)
├── Entities
│   ├── NetworkPacket
│   ├── ClientRequest
│   ├── ServerResponse
│   └── ConnectionStats
├── Interfaces
│   ├── INetworkListener       -- accept connections
│   ├── IPacketSerializer      -- string <-> bytes
│   ├── IPacketParser          -- bytes -> req
│   └── IConnectionPooler      -- manage active connections
├── Abstract Classes
│   ├── AbstractListener
│   └── AbstractProtocolHandler
└── Classes
    ├── TCPListener
    ├── PacketHandler
    ├── ConnectionPoolManager
    └── RequestDispatcher
```
