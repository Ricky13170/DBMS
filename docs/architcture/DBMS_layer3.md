# DBMS Layer 3: Component Deep-dive

This document breaks the detailed Layer-3 operational architecture down for all 8 core subsystems of the DBMS into individual branch flowcharts.

> **Note on Visualization:** Each of the 8 core systems is rendered as a standalone flow chart using a Left-to-Right (`graph LR`) layout. This orientation forces leaf nodes to stack **vertically**, forming a clean list-like cascade that perfectly solves horizontal overstretching and guarantees crisp readability on any screen size.

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

    ROOT --- FM
    ROOT --- PM
    ROOT --- BM
    ROOT --- RM
    ROOT --- AM
    ROOT --- SA

    FM --- FM1[OS File Wrapper]:::layer3
    FM --- FM2[Data File Registry]:::layer3
    FM --- FM3[File Descriptor Manager]:::layer3
    FM --- FM4[File Growth Manager]:::layer3

    PM --- PM1[Page Formatter]:::layer3
    PM --- PM2[Page Header Manager]:::layer3
    PM --- PM3[Slot Directory Manager]:::layer3
    PM --- PM4[Free Space Manager]:::layer3
    PM --- PM5[Page I/O Interface]:::layer3

    BM --- BM1[Buffer Frame Manager]:::layer3
    BM --- BM2[Page Replacement Policy]:::layer3
    BM --- BM3[Dirty Page Writer]:::layer3
    BM --- BM4[Prefetch Manager]:::layer3

    RM --- RM1[Record Layout Manager]:::layer3
    RM --- RM2[RID Generator]:::layer3
    RM --- RM3[Variable-Length Data Manager]:::layer3
    RM --- RM4[Large Object Manager]:::layer3

    AM --- AM1[B+Tree Manager]:::layer3
    AM --- AM2[Hash Index Manager]:::layer3
    AM --- AM3[Index State Manager]:::layer3
    AM --- AM4[Index Maintenance]:::layer3

    SA --- SA1[Extent Manager]:::layer3
    SA --- SA2[Segment Manager]:::layer3
    SA --- SA3[Tablespace Manager]:::layer3
    SA --- SA4[Space Reclamation]:::layer3
```

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

    ROOT --- SP
    ROOT --- QV
    ROOT --- QO
    ROOT --- QE
    ROOT --- RP

    SP --- SP1[Lexical Analyzer]:::layer3
    SP --- SP2[Syntax Analyzer]:::layer3
    SP --- SP3[AST Builder]:::layer3
    SP --- SP4[Error Reporter]:::layer3

    QV --- QV1[Semantic Validator]:::layer3
    QV --- QV2[Catalog Lookup]:::layer3
    QV --- QV3[Privilege Checker]:::layer3
    QV --- QV4[Constraint Validator]:::layer3

    QO --- QO1[Logical Plan Generator]:::layer3
    QO --- QO2[Rule-Based Optimizer]:::layer3
    QO --- QO3[Cost-Based Optimizer]:::layer3
    QO --- QO4[Physical Plan Generator]:::layer3
    QO --- QO5[Plan Cache Manager]:::layer3

    QE --- QE1[Operator Engine]:::layer3
    QE --- QE2[Pipeline Manager]:::layer3
    QE --- QE3[Expression Evaluator]:::layer3
    QE --- QE4[Resource Manager]:::layer3

    RP --- RP1[Result Set Builder]:::layer3
    RP --- RP2[Data Converter]:::layer3
    RP --- RP3[Cursor Manager]:::layer3
    RP --- RP4[Output Buffer]:::layer3
```

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

    ROOT --- TM
    ROOT --- LM
    ROOT --- DH
    ROOT --- IM
    ROOT --- CM

    TM --- TM1[Transaction Lifecycle]:::layer3
    TM --- TM2[TX ID Generator]:::layer3
    TM --- TM3[Savepoint Manager]:::layer3
    TM --- TM4[Transaction Table]:::layer3

    LM --- LM1[Lock Table]:::layer3
    LM --- LM2[Lock Compatibility]:::layer3
    LM --- LM3[Escalation Manager]:::layer3
    LM --- LM4[Two-Phase Locking]:::layer3

    DH --- DH1[Deadlock Detector]:::layer3
    DH --- DH2[Victim Selector]:::layer3
    DH --- DH3[Deadlock Prevention]:::layer3

    IM --- IM1[Isolation Controller]:::layer3
    IM --- IM2[Snapshot Manager]:::layer3
    IM --- IM3[Phantom Protection]:::layer3

    CM --- CM1[MVCC Engine]:::layer3
    CM --- CM2[Version Store]:::layer3
    CM --- CM3[Version Chain Manager]:::layer3
    CM --- CM4[Visibility Checker]:::layer3
    CM --- CM5[Garbage Collector]:::layer3
```

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

    ROOT --- DB
    ROOT --- SC
    ROOT --- TB
    ROOT --- CL
    ROOT --- DT
    ROOT --- ID
    ROOT --- CS
    ROOT --- VW
    ROOT --- PR
    ROOT --- CT

    DB --- DB1[DB Lifecycle]:::layer3
    DB --- DB2[DB State]:::layer3
    DB --- DB3[DB Config]:::layer3
    DB --- DB4[DB Validator]:::layer3

    SC --- SC1[Schema Lifecycle]:::layer3
    SC --- SC2[Ownership]:::layer3
    SC --- SC3[Namespace]:::layer3

    TB --- TB1[Table Lifecycle]:::layer3
    TB --- TB2[Definition]:::layer3
    TB --- TB3[Partition Mgr]:::layer3

    CL --- CL1[Column Lifecycle]:::layer3
    CL --- CL2[Default Value]:::layer3
    CL --- CL3[Identity]:::layer3
    CL --- CL4[Computed Col]:::layer3
    CL --- CL5[Nullability]:::layer3

    DT --- DT1[Built-in Types]:::layer3
    DT --- DT2[UDT Manager]:::layer3
    DT --- DT3[Type Conversion]:::layer3
    DT --- DT4[Type Validator]:::layer3
    DT --- DT5[Collation Management]:::layer3

    ID --- ID1[Index Lifecycle]:::layer3
    ID --- ID2[Index Def]:::layer3
    ID --- ID3[Index Type Manager]:::layer3
    ID --- ID4[Dependency Tracker]:::layer3

    CS --- CS1[PK Manager]:::layer3
    CS --- CS2[FK Manager]:::layer3
    CS --- CS3[Unique Const]:::layer3
    CS --- CS4[Check Const]:::layer3
    CS --- CS5[Constraint Validator]:::layer3

    VW --- VW1[View Lifecycle]:::layer3
    VW --- VW2[View Def Storage]:::layer3
    VW --- VW3[View Resolver]:::layer3
    VW --- VW4[Updatable View Manager]:::layer3
    VW --- VW5[Indexed View]:::layer3

    PR --- PR1[Stored Procs]:::layer3
    PR --- PR2[Functions]:::layer3
    PR --- PR3[Triggers]:::layer3
    PR --- PR4[Parameters]:::layer3
    PR --- PR5[Routine Catalog]:::layer3

    CT --- CT1[System Tables]:::layer3
    CT --- CT2[Meta Reader]:::layer3
    CT --- CT3[Meta Writer]:::layer3
    CT --- CT4[Dependency Tracker]:::layer3
    CT --- CT5[Metadata Cache]:::layer3
    CT --- CT6[Object Identifier]:::layer3
    CT --- CT7[Catalog Versioning]:::layer3
```

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

    ROOT --- AT
    ROOT --- AZ
    ROOT --- AC
    ROOT --- UM
    ROOT --- EC
    ROOT --- AD

    AT --- AT1[Credential Validator]:::layer3
    AT --- AT2[Auth Protocol]:::layer3
    AT --- AT3[Login Manager]:::layer3
    AT --- AT4[Password Policy]:::layer3

    AZ --- AZ1[Permission Resolver]:::layer3
    AZ --- AZ2[Privilege Eval]:::layer3
    AZ --- AZ3[Grant/Revoke Manager]:::layer3
    AZ --- AZ4[Policy Decision Engine]:::layer3

    AC --- AC1[RBAC Evaluator]:::layer3
    AC --- AC2[Row-level Filter]:::layer3
    AC --- AC3[Col-level Masker]:::layer3
    AC --- AC4[Object Perms]:::layer3

    UM --- UM1[User Catalog]:::layer3
    UM --- UM2[Role Catalog]:::layer3
    UM --- UM3[Role Hierarchy]:::layer3
    UM --- UM4[Account Lifecycle]:::layer3

    EC --- EC1[TDE]:::layer3
    EC --- EC2[Transport Encrypt]:::layer3
    EC --- EC3[Key Management]:::layer3
    EC --- EC4[Col-level Encrypt]:::layer3

    AD --- AD1[Audit Log Writer]:::layer3
    AD --- AD2[Audit Rule Engine]:::layer3
    AD --- AD3[Audit Trail Mgr]:::layer3
```

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

    ROOT --- MN
    ROOT --- CF
    ROOT --- UT
    ROOT --- DM
    ROOT --- IE
    ROOT --- TM

    MN --- MN1[Metrics Collector]:::layer3
    MN --- MN2[Slow Query Profiler]:::layer3
    MN --- MN3[Event Logger]:::layer3
    MN --- MN4[Active Sessions]:::layer3

    CF --- CF1[Config Registry]:::layer3
    CF --- CF2[Dynamic Reloader]:::layer3
    CF --- CF3[Engine Options]:::layer3

    UT --- UT1[DBCC Engine]:::layer3
    UT --- UT2[Resource Governor]:::layer3
    UT --- UT3[Database CLI]:::layer3

    DM --- DM1[Stats Collector]:::layer3
    DM --- DM2[Page Verifier]:::layer3
    DM --- DM3[Index Maint Agent]:::layer3
    DM --- DM4[Auto Vacuum]:::layer3

    IE --- IE1[Bulk COPY]:::layer3
    IE --- IE2[CSV/JSON Importer]:::layer3
    IE --- IE3[Binary Importer]:::layer3
    IE --- IE4[Logical Dump Util]:::layer3
    IE --- IE5[Data Export]:::layer3

    TM --- TM1[Pool Controller]:::layer3
    TM --- TM2[Task Scheduler]:::layer3
    TM --- TM3[Worker Pool]:::layer3
```

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

    ROOT --- TL
    ROOT --- CM
    ROOT --- HA
    ROOT --- RM
    ROOT --- BR

    TL --- TL1[WAL Manager]:::layer3
    TL --- TL2[WAL Writer/Buffer]:::layer3
    TL --- TL3[LSN Generator]:::layer3
    TL --- TL4[Log Segment Mgr]:::layer3
    TL --- TL5[Log Archive Mgr]:::layer3

    CM --- CM1[Checkpointer Daemon]:::layer3
    CM --- CM2[Fuzzy Checkpoint]:::layer3
    CM --- CM3[Dirty Page Flush]:::layer3
    CM --- CM4[Checkpoint Metadata Mgr]:::layer3

    HA --- HA1[Log Sender]:::layer3
    HA --- HA2[Log Receiver]:::layer3
    HA --- HA3[Log Applier]:::layer3
    HA --- HA4[Replication Coordinator]:::layer3
    HA --- HA5[Sync Manager]:::layer3

    RM --- RM1[Crash Recovery]:::layer3
    RM --- RM2[REDO/UNDO Applier]:::layer3
    RM --- RM3[PITR Engine]:::layer3
    RM --- RM4[Recovery Coordinator]:::layer3

    BR --- BR1[Full Backup]:::layer3
    BR --- BR2[Incremental Backup]:::layer3
    BR --- BR3[Physical Hot Backup]:::layer3
    BR --- BR4[Backup Metadata Catalog]:::layer3
    BR --- BR5[Restore Planner]:::layer3
    BR --- BR6[File Restorer]:::layer3
    BR --- BR7[Restore Validator]:::layer3
```

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

    ROOT --- CN
    ROOT --- SM
    ROOT --- PH
    ROOT --- RD
    ROOT --- RS

    CN --- CN1[Connection Listener]:::layer3
    CN --- CN2[Connection Pooler]:::layer3
    CN --- CN3[Connection Limiter]:::layer3

    SM --- SM1[Session Lifecycle]:::layer3
    SM --- SM2[Context Store]:::layer3
    SM --- SM3[Timeout Manager]:::layer3

    PH --- PH1[Stream Packet Parser]:::layer3
    PH --- PH2[Data Packet Serializer]:::layer3
    PH --- PH3[SSL/TLS Handshake]:::layer3

    RD --- RD1[Request Queue Manager]:::layer3
    RD --- RD2[Command Router]:::layer3
    RD --- RD3[Thread Assigner]:::layer3

    RS --- RS1[Response Formatter]:::layer3
    RS --- RS2[Network Buffer Writer]:::layer3
    RS --- RS3[Response Stream Writer]:::layer3
```
