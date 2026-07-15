# DBMS Layer 3: Component Deep-dive

This flowchart focuses on Layer-3 breakdown for the two main core systems: **Storage Engine** and **Query Processing**. It is visualized with a symmetrical topology mapping from root context out to specific granular components.

```mermaid
graph LR
    %% Styles & Colors
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px;
    classDef root fill:#ff9999,stroke:#333,stroke-width:2px,font-weight:bold;
    classDef layer1 fill:#99ccff,stroke:#333,stroke-width:1.5px,font-weight:bold;
    classDef layer2 fill:#ccffcc,stroke:#333,stroke-width:1px;
    classDef layer3 fill:#fff3cd,stroke:#aaa,stroke-width:1px;

    %% Root
    db((DBMS)):::root

    %% ==========================================
    %% LEFT SIDE
    %% ==========================================
    se[Storage Engine]:::layer1
    qp[Query Processing]:::layer1
    tc[Transaction & Concurrency]:::layer1
    sc[Security]:::layer1

    se --- db
    qp --- db
    tc --- db
    sc --- db

    %% Storage Engine → L2
    se_fm[File Manager]:::layer2 --- se
    se_pm[Page Manager]:::layer2 --- se
    se_bm[Buffer Manager]:::layer2 --- se
    se_rm[Record Manager]:::layer2 --- se
    se_am[Access Methods]:::layer2 --- se
    se_sa[Storage Allocation]:::layer2 --- se

    %% File Manager → L3
    se_fm_1[OS File Wrapper]:::layer3 --- se_fm
    se_fm_2[Data File Registry]:::layer3 --- se_fm
    se_fm_3[File Descriptor Manager]:::layer3 --- se_fm
    se_fm_4[File Growth Manager]:::layer3 --- se_fm

    %% Page Manager → L3
    se_pm_1[Page Formatter]:::layer3 --- se_pm
    se_pm_2[Page Header Manager]:::layer3 --- se_pm
    se_pm_3[Slot Directory Manager]:::layer3 --- se_pm
    se_pm_4[Free Space Manager]:::layer3 --- se_pm
    se_pm_5[Page I/O Interface]:::layer3 --- se_pm

    %% Buffer Manager → L3
    se_bm_1[Buffer Frame Manager]:::layer3 --- se_bm
    se_bm_2[Page Replacement Policy]:::layer3 --- se_bm
    se_bm_3[Dirty Page Writer]:::layer3 --- se_bm
    se_bm_4[Prefetch Manager]:::layer3 --- se_bm

    %% Record Manager → L3
    se_rm_1[Record Layout Manager]:::layer3 --- se_rm
    se_rm_2[RID Generator]:::layer3 --- se_rm
    se_rm_3[Variable-Length Data Manager]:::layer3 --- se_rm
    se_rm_4[Large Object Manager]:::layer3 --- se_rm

    %% Access Methods → L3
    se_am_1[B+Tree Manager]:::layer3 --- se_am
    se_am_2[Hash Index Manager]:::layer3 --- se_am
    se_am_3[Index State Manager]:::layer3 --- se_am
    se_am_4[Index Maintenance]:::layer3 --- se_am

    %% Storage Allocation → L3
    se_sa_1[Extent Manager]:::layer3 --- se_sa
    se_sa_2[Segment Manager]:::layer3 --- se_sa
    se_sa_3[Tablespace Manager]:::layer3 --- se_sa
    se_sa_4[Space Reclamation]:::layer3 --- se_sa

    %% Query Processing → L2
    qp_sp[SQL Parser]:::layer2 --- qp
    qp_qv[Query Validation]:::layer2 --- qp
    qp_qo[Query Optimizer]:::layer2 --- qp
    qp_qe[Query Executor]:::layer2 --- qp
    qp_rp[Result Processing]:::layer2 --- qp

    %% SQL Parser → L3
    qp_sp_1[Lexical Analyzer]:::layer3 --- qp_sp
    qp_sp_2[Syntax Analyzer]:::layer3 --- qp_sp
    qp_sp_3[AST Builder]:::layer3 --- qp_sp
    qp_sp_4[Error Reporter]:::layer3 --- qp_sp

    %% Query Validation → L3
    qp_qv_1[Semantic Validator]:::layer3 --- qp_qv
    qp_qv_2[Catalog & Metadata Lookup]:::layer3 --- qp_qv
    qp_qv_3[Privilege Checker]:::layer3 --- qp_qv
    qp_qv_4[Constraint Validator]:::layer3 --- qp_qv

    %% Query Optimizer → L3
    qp_qo_1[Logical Plan Generator]:::layer3 --- qp_qo
    qp_qo_2[Rule-Based Optimizer]:::layer3 --- qp_qo
    qp_qo_3[Cost-Based Optimizer]:::layer3 --- qp_qo
    qp_qo_4[Physical Plan Generator]:::layer3 --- qp_qo
    qp_qo_5[Plan Cache Manager]:::layer3 --- qp_qo

    %% Query Executor → L3
    qp_qe_1[Operator Engine]:::layer3 --- qp_qe
    qp_qe_2[Pipeline Manager]:::layer3 --- qp_qe
    qp_qe_3[Expression Evaluator]:::layer3 --- qp_qe
    qp_qe_4[Resource Manager]:::layer3 --- qp_qe

    %% Result Processing → L3
    qp_rp_1[Result Set Builder]:::layer3 --- qp_rp
    qp_rp_2[Data Converter]:::layer3 --- qp_rp
    qp_rp_3[Cursor Manager]:::layer3 --- qp_rp
    qp_rp_4[Pagination Manager]:::layer3 --- qp_rp
    qp_rp_5[Output Buffer]:::layer3 --- qp_rp

    %% Transaction & Concurrency → L2
    tc_tm[Transaction Manager]:::layer2 --- tc
    tc_lm[Lock Manager]:::layer2 --- tc
    tc_dh[Deadlock Handler]:::layer2 --- tc
    tc_im[Isolation Manager]:::layer2 --- tc
    tc_mv[MVCC Manager]:::layer2 --- tc

    %% Security → L2
    sc_at[Authentication]:::layer2 --- sc
    sc_az[Authorization]:::layer2 --- sc
    sc_um[User Management]:::layer2 --- sc
    sc_ec[Encryption]:::layer2 --- sc
    sc_ad[Auditing]:::layer2 --- sc

    %% ==========================================
    %% RIGHT SIDE
    %% ==========================================
    dom[Database Object & Metadata]:::layer1
    adm[Administration]:::layer1
    brl[Backup, Recovery & Logging]:::layer1
    cc[Communication & Connectivity]:::layer1

    db --- dom
    db --- adm
    db --- brl
    db --- cc

    %% Database Object & Metadata → L2
    dom --- dom_sc[Schema Manager]:::layer2
    dom --- dom_tb[Table Manager]:::layer2
    dom --- dom_id[Index Manager]:::layer2
    dom --- dom_cs[Constraint Manager]:::layer2
    dom --- dom_vw[View Manager]:::layer2
    dom --- dom_pr[Procedure Manager]:::layer2
    dom --- dom_ct[Catalog Manager]:::layer2

    %% Administration → L2
    adm --- adm_mn[Monitoring]:::layer2
    adm --- adm_cf[Configuration]:::layer2
    adm --- adm_ut[Utilities & Tools]:::layer2
    adm --- adm_dm[Database Maintenance]:::layer2
    adm --- adm_ie[Import & Export]:::layer2
    adm --- adm_tm[Threads Manager]:::layer2

    %% Backup, Recovery & Logging → L2
    brl --- brl_tl[Transaction Logging]:::layer2
    brl --- brl_cm[Checkpoint Manager]:::layer2
    brl --- brl_ha[High Availability]:::layer2
    brl --- brl_rm[Recovery Manager]:::layer2
    brl --- brl_br[Backup & Restore Manager]:::layer2

    %% Communication & Connectivity → L2
    cc --- cc_cm[Connection Manager]:::layer2
    cc --- cc_sm[Session Manager]:::layer2
    cc --- cc_ph[Protocol Handler]:::layer2
    cc --- cc_rd[Request Dispatcher]:::layer2
    cc --- cc_rm[Response Manager]:::layer2
```
