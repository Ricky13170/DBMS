# DBMS Layer 2: Functional Breakdown

This document illustrates the Layer-2 subsystem breakdown for each of the core 8 systems in the DBMS, structured in a symmetrical topology.

```mermaid
graph LR
    %% Styles & Colors
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px;
    classDef root fill:#7f0000,color:#ffffff,stroke:#4c0000,stroke-width:2px,font-weight:bold,rx:8,ry:8;
    classDef layer1 fill:#1f497d,color:#ffffff,stroke:#0b5394,stroke-width:2px,font-weight:bold,rx:8,ry:8;
    classDef layer2 fill:#38761d,color:#ffffff,stroke:#274e13,stroke-width:2px,rx:8,ry:8;

    %% Root
    db((DBMS)):::root

    %% LEFT SIDE
    se[Storage Engine]:::layer1
    qp[Query Processing]:::layer1
    tc[Transaction & Concurrency]:::layer1
    sc[Security]:::layer1

    se --- db
    qp --- db
    tc --- db
    sc --- db

    se_fm[File Manager]:::layer2 --- se
    se_pm[Page Manager]:::layer2 --- se
    se_bm[Buffer Manager]:::layer2 --- se
    se_rm[Record Manager]:::layer2 --- se
    se_am[Access Methods]:::layer2 --- se
    se_sa[Storage Allocation]:::layer2 --- se

    qp_sp[SQL Parser]:::layer2 --- qp
    qp_qv[Query Validation]:::layer2 --- qp
    qp_qo[Query Optimizer]:::layer2 --- qp
    qp_qe[Query Executor]:::layer2 --- qp
    qp_rp[Result Processing]:::layer2 --- qp

    tc_tm[Transaction Manager]:::layer2 --- tc
    tc_lm[Lock Manager]:::layer2 --- tc
    tc_dh[Deadlock Handler]:::layer2 --- tc
    tc_im[Isolation Manager]:::layer2 --- tc
    tc_cm[Concurrency Management]:::layer2 --- tc

    sc_at[Authentication]:::layer2 --- sc
    sc_az[Authorization]:::layer2 --- sc
    sc_um[User Management]:::layer2 --- sc
    sc_rm[Role Management]:::layer2 --- sc
    sc_pm[Permission Manager]:::layer2 --- sc
    sc_ec[Encryption]:::layer2 --- sc
    sc_ad[Auditing]:::layer2 --- sc
    sc_sp[Security Policy]:::layer2 --- sc

    %% RIGHT SIDE
    dom[Database Object & Metadata]:::layer1
    adm[Administration]:::layer1
    brl[Backup, Recovery & Logging]:::layer1
    cc[Communication & Connectivity]:::layer1

    db --- dom
    db --- adm
    db --- brl
    db --- cc

    dom --- dom_db[Database Manager]:::layer2
    dom --- dom_sc[Schema Manager]:::layer2
    dom --- dom_tb[Table Manager]:::layer2
    dom --- dom_cl[Column Manager]:::layer2
    dom --- dom_dt[Data Type Manager]:::layer2
    dom --- dom_id[Index Manager]:::layer2
    dom --- dom_cs[Constraint Manager]:::layer2
    dom --- dom_vw[View Manager]:::layer2
    dom --- dom_pr[Procedure Manager]:::layer2
    dom --- dom_fn[Function Manager]:::layer2
    dom --- dom_tr[Trigger Manager]:::layer2
    dom --- dom_ct[Catalog Manager]:::layer2

    adm --- adm_mn[Monitoring]:::layer2
    adm --- adm_cf[Configuration]:::layer2
    adm --- adm_ut[Utilities & tools]:::layer2
    adm --- adm_dm[Database Maintenance]:::layer2
    adm --- adm_ie[Import & Export]:::layer2
    adm --- adm_tm[Threads Manager]:::layer2

    brl --- brl_tl[Transaction Logging]:::layer2
    brl --- brl_cm[Checkpoint Manager]:::layer2
    brl --- brl_ha[High Availability Support]:::layer2
    brl --- brl_rm[Recovery Manager]:::layer2
    brl --- brl_br[Backup & Restore Manager]:::layer2

    cc --- cc_cm[Connection Manager]:::layer2
    cc --- cc_sm[Session Manager]:::layer2
    cc --- cc_ph[Protocol Handler]:::layer2
    cc --- cc_rd[Request Dispatcher]:::layer2
    cc --- cc_rm[Response Manager]:::layer2
```

## Layer 2 Modules Explanatory Table

Layer 2 represents the first functional decomposition level branching from the core domains (Layer 1). Each Layer 1 branch is split into smaller component modules (Layer 2) to strictly establish functional and domain boundaries:

| Category | Subsystem (Layer 1) | Functionality (Layer 2 Modules) |
|---|---|---|
| **Core Engine** | **Storage Engine** | Decomposed into 6 specialized modules responsible for: disk interaction, buffer pool management, physical file & page structure formatting, space optimization, and access path allocation (records, index modeling). |
| | **Query Processing** | Decomposed horizontally following the SQL Pipeline lifecycle: raw syntax parsing (Parser), semantics validation (Validation), physical disk-read planning (Optimizer), query physical execution (Executor), and response payload packaging (Result Processing). |
| | **Transaction & Concurrency** | Fully manages the ACID infrastructure: sustaining active transaction states (Transaction Manager), handling conflict-resolution locks (Lock Manager), monitoring cyclic deadlocks (Deadlock Handler), and managing concurrent multi-version histories (MVCC/Isolation). |
| | **Security** | Focuses entirely on security mechanisms: identity verification (Authentication), resource-level rules access (Authorization), permanent disk encryption (Encryption), and historical behavior tracking (Auditing). |
| **Management** | **Database Object & Metadata** | Manages the systemic lifecycle of all logical structures created by end-users (Schema, Table, Column, Index, View, etc.). Acts as the centralized Data Dictionary. |
| | **Administration** | Provides essential utilities for privileged operators (DBAs): monitoring system health and states, flexibly adjusting configuration parameters at runtime, and executing import/export operations. |
| | **Backup, Recovery & Logging** | Distributes and isolates recovery workflows: writing immediate execution data to log files (Transaction WAL) for software crash recovery, and creating storage snapshots (Backup Manager) to safeguard against hardware storage failures. |
| | **Communication & Connectivity** | Acts as the external interface adapter: routing inbound TCP ports (Connection), managing live connections (Session Manager), and decoding stream packets (Protocol Handler) before forwarding the structural payloads directly into the Core Engine. |
