# DBMS High-Level Architecture (Flowchart)

> **Relationship legend**
>
> - **──▶** Main Association (gọi thường xuyên)
> - **-.-▶** Dependency (sử dụng tạm thời)
> - **DBMS → Module** : Ownership / Composition (ở mức kiến trúc)

```mermaid
flowchart TB

%%========================
%% Root
%%========================

DBMS["DBMS"]

%%========================
%% Layer 1
%%========================

CC["Communication &<br/>Connectivity"]
SEC["Security"]
ADM["Administration"]

%%========================
%% Layer 2
%%========================

QP["Query Processing"]

%%========================
%% Layer 3
%%========================

TX["Transaction &<br/>Concurrency"]

BR["Backup, Recovery<br/>& Logging"]

%%========================
%% Layer 4
%%========================

SE["Storage Engine"]

META["Database Objects<br/>& Metadata"]

%%=================================================
%% Ownership
%%=================================================

DBMS --> CC
DBMS --> SEC
DBMS --> ADM
DBMS --> QP
DBMS --> TX
DBMS --> BR
DBMS --> SE
DBMS --> META

%%=================================================
%% Main Request Pipeline
%%=================================================

CC -->|dispatch request| QP

QP -->|read / write| SE

TX -->|WAL| BR

%%=================================================
%% Dependencies
%%=================================================

CC -.->|authenticate| SEC

QP -.->|check privilege| SEC

QP -.->|begin transaction| TX

QP -.->|catalog lookup| META

ADM -.->|optimizer statistics| QP

ADM -.->|vacuum / rebuild index| SE

META -.->|schema layout| SE

META -.->|restore dependency| BR
```
