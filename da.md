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









@startuml
title DBMS High-Level Architecture

skinparam shadowing false
skinparam linetype ortho
skinparam packageStyle rectangle
skinparam defaultTextAlignment center
skinparam ArrowThickness 1.2

top to bottom direction

rectangle "DBMS" as DBMS

'==========================
' Layer 1
'==========================

together {
rectangle "Communication\n&\nConnectivity" as CC
rectangle "Security" as SEC
rectangle "Administration" as ADM
}

'==========================
' Layer 2
'==========================

rectangle "Query\nProcessing" as QP

'==========================
' Layer 3
'==========================

together {
rectangle "Transaction\n&\nConcurrency" as TX
rectangle "Backup,\nRecovery\n& Logging" as BR
}

'==========================
' Layer 4
'==========================

together {
rectangle "Storage\nEngine" as SE
rectangle "Database Objects\n& Metadata" as META
}

'------------------------------------
' Hidden links (force layout)
'------------------------------------

CC -[hidden]- SEC
SEC -[hidden]- ADM

TX -[hidden]- BR

SE -[hidden]- META

CC -[hidden]down- QP
QP -[hidden]down- TX
QP -[hidden]down- SE

'------------------------------------
' Composition
'------------------------------------

DBMS *-down- CC
DBMS *-down- SEC
DBMS *-down- ADM

DBMS *-down- QP

DBMS *-down- TX
DBMS *-down- BR

DBMS *-down- SE
DBMS *-down- META

'------------------------------------
' Main pipeline
'------------------------------------

CC --> QP : dispatch request

QP --> SE : read/write

TX --> BR : WAL

'------------------------------------
' Dependency
'------------------------------------

CC ..> SEC : authenticate

QP ..> SEC : check privilege

QP ..> TX : begin transaction

QP ..> META : catalog lookup

ADM ..> QP : optimizer statistics

ADM ..> SE : vacuum / rebuild index

META ..> SE : schema layout

META ..> BR : restore dependency

@enduml
