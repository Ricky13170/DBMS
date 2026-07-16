# DBMS Layer 3: Component Deep-dive

This document breaks the detailed Layer-3 operational architecture down for all 8 core subsystems of the DBMS into individual branch flowcharts, supplemented with **explanatory tables** defining the strict architectural responsibilities of each sub-component.

> **Note on Visualization:** Each of the 8 core systems is rendered as a standalone flow chart using a Left-to-Right (`graph LR`) layout. This orientation forces leaf nodes to stack **vertically**, forming a clean list-like cascade that perfectly solves horizontal overstretching and guarantees crisp readability on any screen size.

---

## 1. Storage Engine
```mermaid
graph LR
    classDef layer1 fill:#1f497d,color:#ffffff,stroke:#0b5394,stroke-width:2px,font-weight:bold,rx:8,ry:8;
    classDef layer2 fill:#38761d,color:#ffffff,stroke:#274e13,stroke-width:2px,rx:8,ry:8;
    classDef layer3 fill:#b45f06,color:#ffffff,stroke:#783f04,stroke-width:2px,font-style:italic,rx:8,ry:8;

    ROOT[Storage Engine]:::layer1

    FM[File Manager]:::layer2
    PM[Page Manager]:::layer2
    BM[Buffer Manager]:::layer2
    RM[Record Manager]:::layer2
    AM[Access Methods]:::layer2
    SA[Storage Allocation]:::layer2

    ROOT --- FM & PM & BM & RM & AM & SA

    FM --- FM1[OS File Wrapper]:::layer3 & FM2[Data File Registry]:::layer3 & FM3[File Descriptor Manager]:::layer3 & FM4[File Growth Manager]:::layer3
    PM --- PM1[Page Formatter]:::layer3 & PM2[Page Header Manager]:::layer3 & PM3[Slot Directory Manager]:::layer3 & PM4[Free Space Manager]:::layer3 & PM5[Page I/O Interface]:::layer3
    BM --- BM1[Buffer Frame Manager]:::layer3 & BM2[Page Replacement Policy]:::layer3 & BM3[Dirty Page Writer]:::layer3 & BM4[Prefetch Manager]:::layer3
    RM --- RM1[Record Layout Manager]:::layer3 & RM2[RID Generator]:::layer3 & RM3[Variable-Length Data Manager]:::layer3 & RM4[Large Object Manager]:::layer3
    AM --- AM1[B+Tree Manager]:::layer3 & AM2[Hash Index Manager]:::layer3 & AM3[Index State Manager]:::layer3 & AM4[Index Maintenance]:::layer3
    SA --- SA1[Extent Manager]:::layer3 & SA2[Segment Manager]:::layer3 & SA3[Tablespace Manager]:::layer3 & SA4[Space Reclamation]:::layer3
```

### Storage Engine Component Roles
| Layer 2 Subsystem | Layer 3 Component | Functionality / Role |
|---|---|---|
| **File Manager** | OS File Wrapper | Abstracts underlying OS file operations (open, read, write, close) providing cross-platform unity. |
| | Data File Registry | Tracks all active database files and their physical mapping directory strings. |
| | File Descriptor Manager | Manages open file handles and caches tracking to bypass OS limits. |
| | File Growth Manager | Handles automatic physical disk file expansion when capacity limits are hit. |
| **Page Manager** | Page Formatter | Initializes the physical layout mapping for empty unassigned RAM pages. |
| | Page Header Manager | Interacts with metadata embedded within a page's header (e.g., LSN, Page ID). |
| | Slot Directory Manager | Tracks memory offsets referencing records stored on a page (allowing dynamic sizing). |
| | Free Space Manager | Calculates and manages operational free bytes available within a single Page. |
| | Page I/O Interface | Connects Pages structures functionally against the raw physical bytes on Disk via File Manager. |
| **Buffer Manager** | Buffer Frame Manager | Maps dynamically translating physical memory pages onto logical cache buffer slots. |
| | Page Replacement Policy | Elects "victim" pages to evict (e.g. LRU, 2Q, Clock) when the cache pool is exhausted. |
| | Dirty Page Writer | Periodically flushes heavily modified non-persistent RAM pages securely down to the storage disk. |
| | Prefetch Manager | Proactively anticipates sequential disk read needs and caches pages before the executor asks. |
| **Record Manager** | Record Layout Manager | Handles semantic serializing (flattening tuples) into byte arrays and vice-versa. |
| | RID Generator | Generates globally unique Record Identifiers composed of Page ID and Slot ID. |
| | Variable-Length Data Manager | Stores strings (VARCHAR) structurally without wasting byte padding limits. |
| | Large Object Manager | Slices and manages storing enormous objects (LOBs) spanning across multiple pages sequentially. |
| **Access Methods** | B+Tree Manager | Orchestrates heavily balanced hierarchical tree lookups optimizing read/write access. |
| | Hash Index Manager | Manages linear hashing buckets for high-velocity O(1) equality predicate resolutions. |
| | Index State Manager | Monitors indexing structural integrity and validates rebuilding necessity (Fragmentation checks). |
| | Index Maintenance | Repairs tree node balance, executing complex splitting or node merging during heavily loaded DMLs. |
| **Storage Allocation** | Extent Manager | Allocates operational logic spaces in chunks of 8 to 64 consecutive pages (Extents) for locality. |
| | Segment Manager | Organizes allocated extents linking them logically to tables or indexes structures natively. |
| | Tablespace Manager | Binds schemas/Databases logic mapping to physically mounted hardware storage containers. |
| | Space Reclamation | Compacts and reclaims abandoned orphan disk locations previously soft-deleted natively. |

---

## 2. Query Processing
```mermaid
graph LR
    classDef layer1 fill:#1f497d,color:#ffffff,stroke:#0b5394,stroke-width:2px,font-weight:bold,rx:8,ry:8;
    classDef layer2 fill:#38761d,color:#ffffff,stroke:#274e13,stroke-width:2px,rx:8,ry:8;
    classDef layer3 fill:#b45f06,color:#ffffff,stroke:#783f04,stroke-width:2px,font-style:italic,rx:8,ry:8;

    ROOT[Query Processing]:::layer1

    SP[SQL Parser]:::layer2
    QV[Query Validation]:::layer2
    QO[Query Optimizer]:::layer2
    QE[Query Execution]:::layer2
    RP[Result Processing]:::layer2

    ROOT --- SP & QV & QO & QE & RP

    SP --- SP1[Lexical Analyzer]:::layer3 & SP2[Syntax Analyzer]:::layer3 & SP3[AST Builder]:::layer3 & SP4[Error Reporter]:::layer3
    QV --- QV1[Semantic Validator]:::layer3 & QV2[Catalog Lookup]:::layer3 & QV3[Privilege Checker]:::layer3 & QV4[Constraint Validator]:::layer3
    QO --- QO1[Logical Plan Generator]:::layer3 & QO2[Rule-Based Optimizer]:::layer3 & QO3[Cost-Based Optimizer]:::layer3 & QO4[Physical Plan Generator]:::layer3 & QO5[Plan Cache Manager]:::layer3
    QE --- QE1[Operator Engine]:::layer3 & QE2[Pipeline Manager]:::layer3 & QE3[Expression Evaluator]:::layer3 & QE4[Resource Manager]:::layer3
    RP --- RP1[Result Set Builder]:::layer3 & RP2[Data Converter]:::layer3 & RP3[Cursor Manager]:::layer3 & RP4[Output Buffer]:::layer3
```

### Query Processing Component Roles
| Layer 2 Subsystem | Layer 3 Component | Functionality / Role |
|---|---|---|
| **SQL Parser** | Lexical Analyzer | Tokenizes text-based SQL queries slicing them down into known dictionary literals and types. |
| | Syntax Analyzer | Enforces grammatical token structural matching against configured dialect guidelines. |
| | AST Builder | Represents the abstract syntax sequence strictly graphically using logic tree patterns. |
| | Error Reporter | Reconstructs semantic failure bounds indicating which string character caused the compilation failure. |
| **Query Validation** | Semantic Validator | Authenticates whether requested attributes and structures actively exist dynamically. |
| | Catalog Lookup | Leverages Metadata caches inspecting schema bounds defining tables boundaries dynamically. |
| | Privilege Checker | Determines whether the session explicitly executing has read/write RBAC clearance per column. |
| | Constraint Validator | Inspects potential query payloads guaranteeing referential bounds (e.g. FK matching). |
| **Query Optimizer** | Logical Plan Generator | Interprets the confirmed AST and translates components into Relational Algebra expressions. |
| | Rule-Based Optimizer | Executes predefined algorithm modifications structurally (e.g., Predicate filtering pushdowns). |
| | Cost-Based Optimizer | Selects the cheapest path iterating statistics mapping CPU vectors and I/O loading limits. |
| | Physical Plan Generator | Formats the theoretical logic into specific actionable engine commands mapping exact Storage rules. |
| | Plan Cache Manager | Caches heavily executed queries into memory intercepting identical text bypassing Parsing completely. |
| **Query Execution** | Operator Engine | Enacts physical core relational operations dynamically (Table Scans, Hash Joins, Loop Joins). |
| | Pipeline Manager | Steers continuous streamed tuples executing continuously without stalling memory footprints. |
| | Expression Evaluator | Calculates active mathematical evaluations embedded as logic predicates recursively mapping tuples. |
| | Resource Manager | Controls CPU threshold scheduling blocking individual heavy queries throttling out all threads heavily. |
| **Result Processing** | Result Set Builder | Rearranges internal bytes into structured tabular logic formatted exactly for the client mapping. |
| | Data Converter | Reconstructs native internal raw Byte arrays translating dynamically into readable text format output. |
| | Cursor Manager | Maintains logical fetch states preserving sequence iteration logic bypassing RAM limits structurally. |
| | Output Buffer | Holds outgoing parsed response payload staging strictly for network propagation cleanly offloading. |

---

## 3. Transaction & Concurrency
```mermaid
graph LR
    classDef layer1 fill:#1f497d,color:#ffffff,stroke:#0b5394,stroke-width:2px,font-weight:bold,rx:8,ry:8;
    classDef layer2 fill:#38761d,color:#ffffff,stroke:#274e13,stroke-width:2px,rx:8,ry:8;
    classDef layer3 fill:#b45f06,color:#ffffff,stroke:#783f04,stroke-width:2px,font-style:italic,rx:8,ry:8;

    ROOT[Transaction & Concurrency]:::layer1

    TM[Transaction Manager]:::layer2
    LM[Lock Manager]:::layer2
    DH[Deadlock Handler]:::layer2
    IM[Isolation Manager]:::layer2
    CM[Concurrency Management]:::layer2

    ROOT --- TM & LM & DH & IM & CM

    TM --- TM1[Transaction Lifecycle]:::layer3 & TM2[TX ID Generator]:::layer3 & TM3[Savepoint Manager]:::layer3 & TM4[Transaction Table]:::layer3
    LM --- LM1[Lock Table]:::layer3 & LM2[Lock Compatibility]:::layer3 & LM3[Escalation Manager]:::layer3 & LM4[Two-Phase Locking]:::layer3
    DH --- DH1[Deadlock Detector]:::layer3 & DH2[Victim Selector]:::layer3 & DH3[Deadlock Prevention]:::layer3
    IM --- IM1[Isolation Controller]:::layer3 & IM2[Snapshot Manager]:::layer3 & IM3[Phantom Protection]:::layer3
    CM --- CM1[MVCC Engine]:::layer3 & CM2[Version Store]:::layer3 & CM3[Version Chain Manager]:::layer3 & CM4[Visibility Checker]:::layer3 & CM5[Garbage Collector]:::layer3
```

### Transaction & Concurrency Component Roles
| Layer 2 Subsystem | Layer 3 Component | Functionality / Role |
|---|---|---|
| **Transaction Manager**| Transaction Lifecycle | Orchestrates transactional states (Active, Partially Committed, Failed, Aborted, or Committed). |
| | TX ID Generator | Mints monotonically increasing transaction integers dynamically binding sequence boundaries. |
| | Savepoint Manager | Implements logical rollback sub-checkpoints preventing entire transaction failures linearly. |
| | Transaction Table | Hosts in-memory hash mappings tracking all active sessions scaling dynamically. |
| **Lock Manager** | Lock Table | Tracks specific resources heavily bound globally dictating active locking states memory boundaries. |
| | Lock Compatibility | Decides matrices conflict boundaries mapping Shared vs Exclusive scaling dynamically preventing data racing. |
| | Escalation Manager | Mutates massive granular Row locks collapsing explicitly into Table bounds bypassing memory threshold limits. |
| | Two-Phase Locking | Forces strict serializable limits preventing releasing locks early until phase shrinking commences explicitly. |
| **Deadlock Handler** | Deadlock Detector | Iterates cyclical wait-for graphs natively mapping transactions mutually preventing infinite hanging. |
| | Victim Selector | Targets specifically executing processes terminating linearly based crucially on lowest-cost boundaries logically. |
| | Deadlock Prevention | Proactively manages limits aggressively failing transactions preventing cycles entirely using heuristic timeout algorithms. |
| **Isolation Manager** | Isolation Controller | Polices explicit ANSI anomalies managing boundaries strictly matching RC, RR, configuring consistency mapping. |
| | Snapshot Manager | Locks read-bounds freezing state dynamically ensuring read-write collisions resolve mapping historically natively. |
| | Phantom Protection | Deploys Gap locking boundaries isolating insertions blocking phantom row emergence predictably natively. |
| **Concurrency (MVCC)**| MVCC Engine | Modulates reading limits mapping reads independently without blocking modifying writes globally. |
| | Version Store | Maintains exact historic clones mapped logically resolving modifications safely preserving snapshot limits. |
| | Version Chain Manager | Configures backwards-linked maps iterating previous record states natively spanning globally safely. |
| | Visibility Checker | Correlates whether specific historical versions validate viewing permissions dynamically per executing Transaction IDs. |
| | Garbage Collector | Executes purging bounds physically cleaning version chains terminating expired ghost tuples aggressively natively. |

---

## 4. Database Object & Metadata
```mermaid
graph LR
    classDef layer1 fill:#1f497d,color:#ffffff,stroke:#0b5394,stroke-width:2px,font-weight:bold,rx:8,ry:8;
    classDef layer2 fill:#38761d,color:#ffffff,stroke:#274e13,stroke-width:2px,rx:8,ry:8;
    classDef layer3 fill:#b45f06,color:#ffffff,stroke:#783f04,stroke-width:2px,font-style:italic,rx:8,ry:8;

    ROOT[Database Object & Metadata]:::layer1

    DB[Database Mgr]:::layer2
    SC[Schema Mgr]:::layer2
    TB[Table Mgr]:::layer2
    CL[Column Mgr]:::layer2
    DT[Data Type Mgr]:::layer2
    ID[Index Mgr]:::layer2
    CS[Constraint Mgr]:::layer2
    VW[View Mgr]:::layer2
    PR[Programmable Objects]:::layer2
    CT[Catalog Mgr]:::layer2

    ROOT --- DB & SC & TB & CL & DT & ID & CS & VW & PR & CT

    DB --- DB1[DB Lifecycle]:::layer3 & DB2[DB State]:::layer3 & DB3[DB Config]:::layer3 & DB4[DB Validator]:::layer3
    SC --- SC1[Schema Lifecycle]:::layer3 & SC2[Ownership]:::layer3 & SC3[Namespace]:::layer3
    TB --- TB1[Table Lifecycle]:::layer3 & TB2[Definition]:::layer3 & TB3[Partition Mgr]:::layer3
    CL --- CL1[Column Lifecycle]:::layer3 & CL2[Default Value]:::layer3 & CL3[Identity]:::layer3 & CL4[Computed Col]:::layer3 & CL5[Nullability]:::layer3
    DT --- DT1[Built-in Types]:::layer3 & DT2[UDT Manager]:::layer3 & DT3[Type Conversion]:::layer3 & DT4[Type Validator]:::layer3 & DT5[Collation Management]:::layer3
    ID --- ID1[Index Lifecycle]:::layer3 & ID2[Index Def]:::layer3 & ID3[Index Type Manager]:::layer3 & ID4[Dependency Tracker]:::layer3
    CS --- CS1[PK Manager]:::layer3 & CS2[FK Manager]:::layer3 & CS3[Unique Const]:::layer3 & CS4[Check Const]:::layer3 & CS5[Constraint Validator]:::layer3
    VW --- VW1[View Lifecycle]:::layer3 & VW2[View Def Storage]:::layer3 & VW3[View Resolver]:::layer3 & VW4[Updatable View Manager]:::layer3 & VW5[Indexed View]:::layer3
    PR --- PR1[Stored Procs]:::layer3 & PR2[Functions]:::layer3 & PR3[Triggers]:::layer3 & PR4[Parameters]:::layer3 & PR5[Routine Catalog]:::layer3
    CT --- CT1[System Tables]:::layer3 & CT2[Meta Reader]:::layer3 & CT3[Meta Writer]:::layer3 & CT4[Dependency Tracker]:::layer3 & CT5[Metadata Cache]:::layer3 & CT6[Object Identifier]:::layer3 & CT7[Catalog Versioning]:::layer3
```

### DB Object & Metadata Component Roles
*(Because Metadata contains 40+ objects, key definitions are grouped generally for documentation compactness)*
| Layer 2 Subsystem | Functionality / Role of Inner Components |
|---|---|
| **Database & Schema Mgr** | Resolves creation logically encapsulating table bindings. Sets operational states configuring read-only scaling and ownership boundaries structurally bypassing collision natively. |
| **Table & Column Mgr** | Architecturally maps definitions strictly bounding variables logic configuring defaults, primary incremental vectors, nullability, partitioning mappings natively. |
| **Data Type Mgr** | Controls native memory mappings assigning semantic structures globally resolving implicit Casting matrices seamlessly tracking strings character limits predictably. |
| **Index & Constraint Mgr** | Dictates structural enforcement binding keys verifying domains dynamically handling relationships universally preventing corrupt relationships organically. |
| **View & Programmable Mgr**| Materializes logic sequences converting stored queries into transparently fetched dynamic subsets heavily executing grouped behavioral batches cleanly. |
| **Catalog Mgr** | Hosts the Universal Truth tables configuring caching logic managing identifiers globally ensuring referencing dependencies dynamically resolving correctly. |

---

## 5. Security
```mermaid
graph LR
    classDef layer1 fill:#1f497d,color:#ffffff,stroke:#0b5394,stroke-width:2px,font-weight:bold,rx:8,ry:8;
    classDef layer2 fill:#38761d,color:#ffffff,stroke:#274e13,stroke-width:2px,rx:8,ry:8;
    classDef layer3 fill:#b45f06,color:#ffffff,stroke:#783f04,stroke-width:2px,font-style:italic,rx:8,ry:8;

    ROOT[Security]:::layer1

    AT[Authentication]:::layer2
    AZ[Authorization]:::layer2
    AC[Access Control]:::layer2
    UM[User Management]:::layer2
    EC[Encryption]:::layer2
    AD[Auditing]:::layer2

    ROOT --- AT & AZ & AC & UM & EC & AD

    AT --- AT1[Credential Validator]:::layer3 & AT2[Auth Protocol]:::layer3 & AT3[Login Manager]:::layer3 & AT4[Password Policy]:::layer3
    AZ --- AZ1[Permission Resolver]:::layer3 & AZ2[Privilege Eval]:::layer3 & AZ3[Grant/Revoke Manager]:::layer3 & AZ4[Policy Decision Engine]:::layer3
    AC --- AC1[RBAC Evaluator]:::layer3 & AC2[Row-level Filter]:::layer3 & AC3[Col-level Masker]:::layer3 & AC4[Object Perms]:::layer3
    UM --- UM1[User Catalog]:::layer3 & UM2[Role Catalog]:::layer3 & UM3[Role Hierarchy]:::layer3 & UM4[Account Lifecycle]:::layer3
    EC --- EC1[TDE]:::layer3 & EC2[Transport Encrypt]:::layer3 & EC3[Key Management]:::layer3 & EC4[Col-level Encrypt]:::layer3
    AD --- AD1[Audit Log Writer]:::layer3 & AD2[Audit Rule Engine]:::layer3 & AD3[Audit Trail Mgr]:::layer3
```

### Security Component Roles
| Layer 2 Subsystem | Layer 3 Component | Functionality / Role |
|---|---|---|
| **Authentication** | Credential Validator | Checks explicitly hashed incoming tokens verifying encrypted user credentials securely predictably. |
| | Auth Protocol | Orchestrates standardized handshake logic resolving token structures reliably. |
| | Login Manager | Sets contextual properties logging access bounds isolating sessions globally reliably. |
| | Password Policy | Polices formatting bounds restricting weakly structured strings configuring cycling timers securely. |
| **Authorization/RBAC** | Permission Eval/Resolver | Matches mapping trees linking users towards granular granted vectors aggressively. |
| | Access Filters (Row/Col) | Dynamically edits logical queries blocking restricted tuple subsets masking unprivileged column data completely natively. |
| **Encryption & Audit** | TDE / Key Management | Transparently encrypts storage files dynamically rendering drives unreadable bypassing valid key boundaries tracking logging actions structurally. |

---

## 6. Administration
```mermaid
graph LR
    classDef layer1 fill:#1f497d,color:#ffffff,stroke:#0b5394,stroke-width:2px,font-weight:bold,rx:8,ry:8;
    classDef layer2 fill:#38761d,color:#ffffff,stroke:#274e13,stroke-width:2px,rx:8,ry:8;
    classDef layer3 fill:#b45f06,color:#ffffff,stroke:#783f04,stroke-width:2px,font-style:italic,rx:8,ry:8;

    ROOT[Administration]:::layer1

    MN[Monitoring]:::layer2
    CF[Configuration]:::layer2
    UT[Utilities & Tools]:::layer2
    DM[Database Maintenance]:::layer2
    IE[Import & Export]:::layer2
    TM[Thread Pool Mgr]:::layer2

    ROOT --- MN & CF & UT & DM & IE & TM

    MN --- MN1[Metrics Collector]:::layer3 & MN2[Slow Query Profiler]:::layer3 & MN3[Event Logger]:::layer3 & MN4[Active Sessions]:::layer3
    CF --- CF1[Config Registry]:::layer3 & CF2[Dynamic Reloader]:::layer3 & CF3[Engine Options]:::layer3
    UT --- UT1[DBCC Engine]:::layer3 & UT2[Resource Governor]:::layer3 & UT3[Database CLI]:::layer3
    DM --- DM1[Stats Collector]:::layer3 & DM2[Page Verifier]:::layer3 & DM3[Index Maint Agent]:::layer3 & DM4[Auto Vacuum]:::layer3
    IE --- IE1[Bulk COPY]:::layer3 & IE2[CSV/JSON Importer]:::layer3 & IE3[Binary Importer]:::layer3 & IE4[Logical Dump Util]:::layer3 & IE5[Data Export]:::layer3
    TM --- TM1[Pool Controller]:::layer3 & TM2[Task Scheduler]:::layer3 & TM3[Worker Pool]:::layer3
```

### Administration Component Roles
| Layer 2 Subsystem | Functionality / Role of Inner Components |
|---|---|
| **Monitoring & Config** | Exposes metrics capturing CPU/I/O limits analyzing heavily executing delays tracking runtime tuning reloading parameters globally safely. |
| **Maintenance & Utils** | Fixes orphaned clusters reorganizing structures checking logical consistencies managing scheduled pruning (Vacuuming). |
| **Import/Export & Threads**| Multiplexes structural vectors processing massive payloads assigning multi-threaded logic explicitly resolving workloads concurrently effortlessly. |

---

## 7. Backup, Recovery & Logging
```mermaid
graph LR
    classDef layer1 fill:#1f497d,color:#ffffff,stroke:#0b5394,stroke-width:2px,font-weight:bold,rx:8,ry:8;
    classDef layer2 fill:#38761d,color:#ffffff,stroke:#274e13,stroke-width:2px,rx:8,ry:8;
    classDef layer3 fill:#b45f06,color:#ffffff,stroke:#783f04,stroke-width:2px,font-style:italic,rx:8,ry:8;

    ROOT[Backup, Recovery & Logging]:::layer1

    TL[Transaction Logging]:::layer2
    CM[Checkpoint Manager]:::layer2
    HA[High Availability]:::layer2
    RM[Recovery Manager]:::layer2
    BR[Backup & Restore]:::layer2

    ROOT --- TL & CM & HA & RM & BR

    TL --- TL1[WAL Manager]:::layer3 & TL2[WAL Writer/Buffer]:::layer3 & TL3[LSN Generator]:::layer3 & TL4[Log Segment Mgr]:::layer3 & TL5[Log Archive Mgr]:::layer3
    CM --- CM1[Checkpointer Daemon]:::layer3 & CM2[Fuzzy Checkpoint]:::layer3 & CM3[Dirty Page Flush]:::layer3 & CM4[Checkpoint Metadata Mgr]:::layer3
    HA --- HA1[Log Sender]:::layer3 & HA2[Log Receiver]:::layer3 & HA3[Log Applier]:::layer3 & HA4[Replication Coordinator]:::layer3 & HA5[Sync Manager]:::layer3
    RM --- RM1[Crash Recovery]:::layer3 & RM2[REDO/UNDO Applier]:::layer3 & RM3[PITR Engine]:::layer3 & RM4[Recovery Coordinator]:::layer3
    BR --- BR1[Full Backup]:::layer3 & BR2[Incremental Backup]:::layer3 & BR3[Physical Hot Backup]:::layer3 & BR4[Backup Metadata Catalog]:::layer3 & BR5[Restore Planner]:::layer3 & BR6[File Restorer]:::layer3 & BR7[Restore Validator]:::layer3
```

### Backup, Recovery Component Roles
| Layer 2 Subsystem | Functionality / Role of Inner Components |
|---|---|
| **Logging (WAL)** | Queues active delta changes mapping linear sequences appending explicitly ensuring persistency before actual commits. |
| **Checkpoint & HA** | Pauses logical flushing limits establishing recovery lines. Replicates logs streaming logic maintaining secondary cluster synchronization gracefully. |
| **Recovery & Backup** | Traverses boundaries backwards/forwards orchestrating complete rebuilds resolving crash scenarios creating persistent disk snapshots explicitly securely. |

---

## 8. Communication & Connectivity
```mermaid
graph LR
    classDef layer1 fill:#1f497d,color:#ffffff,stroke:#0b5394,stroke-width:2px,font-weight:bold,rx:8,ry:8;
    classDef layer2 fill:#38761d,color:#ffffff,stroke:#274e13,stroke-width:2px,rx:8,ry:8;
    classDef layer3 fill:#b45f06,color:#ffffff,stroke:#783f04,stroke-width:2px,font-style:italic,rx:8,ry:8;

    ROOT[Communication & Connectivity]:::layer1

    CN[Connection Manager]:::layer2
    SM[Session Manager]:::layer2
    PH[Protocol Handler]:::layer2
    RD[Request Dispatcher]:::layer2
    RS[Response Manager]:::layer2

    ROOT --- CN & SM & PH & RD & RS

    CN --- CN1[Connection Listener]:::layer3 & CN2[Connection Pooler]:::layer3 & CN3[Connection Limiter]:::layer3
    SM --- SM1[Session Lifecycle]:::layer3 & SM2[Context Store]:::layer3 & SM3[Timeout Manager]:::layer3
    PH --- PH1[Stream Packet Parser]:::layer3 & PH2[Data Packet Serializer]:::layer3 & PH3[SSL/TLS Handshake]:::layer3
    RD --- RD1[Request Queue Manager]:::layer3 & RD2[Command Router]:::layer3 & RD3[Thread Assigner]:::layer3
    RS --- RS1[Response Formatter]:::layer3 & RS2[Network Buffer Writer]:::layer3 & RS3[Response Stream Writer]:::layer3
```

### Communication Component Roles
| Layer 2 Subsystem | Functionality / Role of Inner Components |
|---|---|
| **Connection & Session** | Listens tracking active TCP sockets multiplexing heavily routing tracking session contexts globally bypassing disconnection limits cleanly. |
| **Protocol & Request** | Deserializes wire payloads explicitly routing logical boundaries allocating executing thread parameters explicitly isolating execution dynamically. |
| **Response** | Rearranges output streams chunking buffering boundaries efficiently terminating payload transfers across network limits smoothly. |
