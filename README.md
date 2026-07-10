# Bản vẽ bản demo Layer 2 - DBMS Mindmap

File này trình bày hai cách vẽ sơ đồ Layer 1 và Layer 2 của hệ thống DBMS bằng công cụ **Mermaid**.

> [!WARNING]
> **Lưu ý về hiển thị trong VS Code Preview:**
> * **Cách 1 (cú pháp `mindmap`):** Có thể không hiển thị được (báo lỗi syntax hoặc trắng trơn) trên VS Code do trình dựng mặc định của VS Code chưa hỗ trợ layout này. Chỉ hiển thị khi bạn tải Extension `Markdown Preview Mermaid Support` của Matt Bierner hoặc khi push lên GitHub.
> * **Cách 2 (cú pháp `flowchart`):** Hiển thị hoàn hảo ngay lập tức trên VS Code và GitHub mà không cần cài thêm gì.

---

## Cách 1: Sử dụng cú pháp `mindmap` (Mermaid Mindmap)

Đây là cú pháp tối ưu và ngắn gọn nhất cho Sơ đồ tư duy dạng tỏa tròn.

```mermaid
mindmap
  root((DBMS))
    Storage Engine
      File Manager
      Page Manager
      Buffer Manager
      Record Manager
      Access Methods
      Storage Allocation
    Query Processing
      SQL Parser
      Query Validation
      Query Optimizer
      Query Executor
      Result Processing
    Transaction & Concurrency
      Transaction Manager
      Lock Manager
      Deadlock Handler
      Isolation Manager
      Concurrency Management
    Security
      Authentication
      Authorization
      User Management
      Role Management
      Permission Manager
      Encryption
      Auditing
      Security Policy
    Database Object & Metadata
      Database Manager
      Schema Manager
      Table Manager
      Column Manager
      Data Type Manager
      Index Manager
      Constraint Manager
      View Manager
      Procedure Manager
      Function Manager
      Trigger Manager
      Catalog Manager
    Administration
      Monitoring
      Configuration
      Utilities & tools
      Database Maintenance
      Import & Export
      Threads Manager
    Backup, Recovery & Logging
      Transaction Logging
      Checkpoint Manager
      High Availability Support
      Recovery Manager
      Backup & Restore Manager
    Communication & Connectivity
      Connection Manager
      Session Manager
      Protocol Handler
      Request Dispatcher
      Response Manager
```

---

## Cách 2: Sử dụng cú pháp `flowchart` (graph LR)

Giao diện dạng cây từ trái sang phải, cho phép tùy biến hình dạng node và phân màu bằng CSS.

```mermaid
graph LR
    %% Styles & Colors
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px;
    classDef root fill:#ff9999,stroke:#333,stroke-width:2px,font-weight:bold;
    classDef layer1 fill:#99ccff,stroke:#333,stroke-width:1.5px,font-weight:bold;
    classDef layer2 fill:#ccffcc,stroke:#333,stroke-width:1px;

    %% Root (Center Node)
    db((DBMS)):::root

    %% ==========================================
    %% NỬA BÊN TRÁI (Xếp về bên trái dùng liên kết B --- A)
    %% ==========================================

    %% Layer 1
    se[Storage Engine]:::layer1
    qp[Query Processing]:::layer1
    tc[Transaction & Concurrency]:::layer1
    sc[Security]:::layer1

    se --- db
    qp --- db
    tc --- db
    sc --- db

    %% Layer 2: Storage Engine
    se_fm[File Manager]:::layer2 --- se
    se_pm[Page Manager]:::layer2 --- se
    se_bm[Buffer Manager]:::layer2 --- se
    se_rm[Record Manager]:::layer2 --- se
    se_am[Access Methods]:::layer2 --- se
    se_sa[Storage Allocation]:::layer2 --- se

    %% Layer 2: Query Processing
    qp_sp[SQL Parser]:::layer2 --- qp
    qp_qv[Query Validation]:::layer2 --- qp
    qp_qo[Query Optimizer]:::layer2 --- qp
    qp_qe[Query Executor]:::layer2 --- qp
    qp_rp[Result Processing]:::layer2 --- qp

    %% Layer 2: Transaction & Concurrency
    tc_tm[Transaction Manager]:::layer2 --- tc
    tc_lm[Lock Manager]:::layer2 --- tc
    tc_dh[Deadlock Handler]:::layer2 --- tc
    tc_im[Isolation Manager]:::layer2 --- tc
    tc_cm[Concurrency Management]:::layer2 --- tc

    %% Layer 2: Security
    sc_at[Authentication]:::layer2 --- sc
    sc_az[Authorization]:::layer2 --- sc
    sc_um[User Management]:::layer2 --- sc
    sc_rm[Role Management]:::layer2 --- sc
    sc_pm[Permission Manager]:::layer2 --- sc
    sc_ec[Encryption]:::layer2 --- sc
    sc_ad[Auditing]:::layer2 --- sc
    sc_sp[Security Policy]:::layer2 --- sc

    %% ==========================================
    %% NỬA BÊN PHẢI (Xếp về bên phải dùng liên kết A --- B)
    %% ==========================================

    %% Layer 1
    dom[Database Object & Metadata]:::layer1
    adm[Administration]:::layer1
    brl[Backup, Recovery & Logging]:::layer1
    cc[Communication & Connectivity]:::layer1

    db --- dom
    db --- adm
    db --- brl
    db --- cc

    %% Layer 2: Database Object & Metadata
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

    %% Layer 2: Administration
    adm --- adm_mn[Monitoring]:::layer2
    adm --- adm_cf[Configuration]:::layer2
    adm --- adm_ut[Utilities & tools]:::layer2
    adm --- adm_dm[Database Maintenance]:::layer2
    adm --- adm_ie[Import & Export]:::layer2
    adm --- adm_tm[Threads Manager]:::layer2

    %% Layer 2: Backup, Recovery & Logging
    brl --- brl_tl[Transaction Logging]:::layer2
    brl --- brl_cm[Checkpoint Manager]:::layer2
    brl --- brl_ha[High Availability Support]:::layer2
    brl --- brl_rm[Recovery Manager]:::layer2
    brl --- brl_br[Backup & Restore Manager]:::layer2

    %% Layer 2: Communication & Connectivity
    cc --- cc_cm[Connection Manager]:::layer2
    cc --- cc_sm[Session Manager]:::layer2
    cc --- cc_ph[Protocol Handler]:::layer2
    cc --- cc_rd[Request Dispatcher]:::layer2
    cc --- cc_rm[Response Manager]:::layer2
```








```mermaid
graph LR
    classDef branch fill:#99ccff,stroke:#333;
    classDef sub fill:#ccffcc,stroke:#333;
    classDef classNode fill:#fff,stroke:#333,stroke-dasharray: 5 5;

    se[Storage Engine]:::branch
    
    %% Sub-components
    se --> am[Access Methods]:::sub
    se --> pm[Page Manager]:::sub
    
    %% Classes & Interfaces
    am --- IAccess[<< interface >> IAccessMethod]:::classNode
    am --- BTree[class BPlusTreeManager]:::classNode
    am --- Heap[class HeapScan]:::classNode
    
    pm --- BasePg[<< abstract >> BasePage]:::classNode
    pm --- DataPg[class DataPage]:::classNode
    pm --- Header[class PageHeader]:::classNode







# Class Diagram Level 1: Hệ thống DBMS (High-Level Architecture)

Tài liệu này cung cấp sơ đồ Class Diagram Level 1, thể hiện sự tương tác, phụ thuộc và thừa kế giữa các Class/Interface lớn nhất đại diện cho 8 nhánh của hệ thống DBMS.

---

## 1. Bản vẽ Class Diagram Level 1 (Mermaid)

Sơ đồ này mô tả cách các thành phần trong các tầng kiến trúc (Connectivity -> Query Parser -> Execution Operators -> Access Methods -> Buffer Pool -> OS Files/Logs) giao tiếp với nhau bằng cách sử dụng các Interfaces cột trụ để giảm sự phụ thuộc trực tiếp (coupling).

```mermaid
classDiagram
    %% ==========================================
    %% TẦNG 1: COMMUNICATION & CONNECTIVITY (Mạng & Phiên)
    %% ==========================================
    class NetworkListener {
        +startPortListener()
        +acceptClientSocket()
    }
    class SessionManager {
        +createSession() : SessionContext
        +closeSession(SessionID)
        +getActiveSession(SessionID) : SessionContext
    }
    class RequestDispatcher {
        -threadPool : WorkerThreadPool
        +dispatchQuery(queryString, SessionContext)
    }

    NetworkListener --> SessionManager : "authenticates & creates"
    NetworkListener --> RequestDispatcher : "dispatches socket stream to"

    %% ==========================================
    %% TẦNG 2: QUERY PROCESSING (Bộ xử lý truy vấn)
    %% ==========================================
    class SQLParser {
        -lexer : Lexer
        +parseToAST(queryString) : AST
    }
    class SemanticValidator {
        -catalog : CatalogManager
        +checkSemanticState(AST) : boolean
    }
    class QueryOptimizer {
        -costEstimator : CostEstimator
        +generateBestPlan(AST) : PhysicalPlan
    }
    class OperatorExecutor {
        <<abstract>>
        +open()
        +next() : Record
        +close()
    }

    RequestDispatcher --> SQLParser : "sends raw query to"
    SQLParser --> SemanticValidator : "sends AST to"
    SemanticValidator --> QueryOptimizer : "sends validated AST to"
    QueryOptimizer --> OperatorExecutor : "compiles plan to executor tree"

    %% ==========================================
    %% TẦNG 3: DATABASE OBJECT & METADATA (Cấu trúc & Catalog)
    %% ==========================================
    class CatalogManager {
        -metadataCache : MetadataCache
        +resolveObjectID(schemaName, tableName) : ObjectID
        +getTableMetadata(ObjectID) : TableMetadata
    }
    class IConstraintValidator {
        <<interface>>
        +validateConstraints(Record, TableMetadata) : boolean
    }

    SemanticValidator ..> CatalogManager : "lookups metadata"
    OperatorExecutor ..> IConstraintValidator : "evaluates validations on INSERT/UPDATE"

    %% ==========================================
    %% TẦNG 4: TRANSACTION & LOCKING (Concurrency)
    %% ==========================================
    class TransactionManager {
        -transactionTable : TransactionTable
        +beginTransaction() : Transaction
        +commit(Transaction)
        +abort(Transaction)
    }
    class LockManager {
        -lockTable : LockTable
        +acquireLock(TransactionID, ResourceID, LockMode) : boolean
        +releaseLock(TransactionID, ResourceID)
    }

    RequestDispatcher ..> TransactionManager : "manages tx block"
    OperatorExecutor ..> LockManager : "requests locks (Shared/Exclusive) during read/write"

    %% ==========================================
    %% TẦNG 5: ACCESS METHODS & BUFFER POOL (Storage Engine)
    %% ==========================================
    class IAccessMethod {
        <<interface>>
        +getNextRecordRID(ScanState) : RID
    }
    class BPlusTreeManager {
        +findKey(Key) : RID
        +insertKey(Key, RID)
        +removeKey(Key)
    }
    class HeapScan {
        +scanNextRow(TableID) : RID
    }
    class BufferPoolManager {
        -frameTable : BufferFrame[]
        +pinPage(PageID) : BasePage
        +unpinPage(PageID, isDirty)
        +flushAll()
    }

    IAccessMethod <|.. BPlusTreeManager : "implements"
    IAccessMethod <|.. HeapScan : "implements"

    OperatorExecutor --> IAccessMethod : "retrieves physical row IDs from"
    BPlusTreeManager --> BufferPoolManager : "requests data pages from"
    HeapScan --> BufferPoolManager : "requests data pages from"

    %% ==========================================
    %% TẦNG 6: FILE SYSTEM & LOGGING (OS & Bền vững)
    %% ==========================================
    class IFileManager {
        <<interface>>
        +readPageBlock(PageID, byteBuffer)
        +writePageBlock(PageID, byteBuffer)
    }
    class IWalWriter {
        <<interface>>
        +appendLogRecord(LSN, byteBuffer)
        +flushLogToDisk()
    }

    BufferPoolManager --> IFileManager : "swaps pages using"
    TransactionManager --> IWalWriter : "logs transaction state change"
    BPlusTreeManager --> IWalWriter : "logs structural page modifications (Split/Merge)"
```

---

## 2. Giải thích sự tương tác giữa các Class thông qua Interface

Sơ đồ Class Diagram Level 1 thể hiện rõ nét triết lý **Dependency Inversion** (các module cấp cao không phụ thuộc phụ thuộc trực tiếp vào module cấp thấp, cả hai đều phụ thuộc vào lớp trừu tượng - Interface):

1.  **Sự cô lập của Query Execution (`OperatorExecutor`):**
    *   `OperatorExecutor` là lớp trừu tượng đại diện cho các toán tử chạy lệnh (Volcano Iterator Model). Nó **không hề giao tiếp trực tiếp** với File cứng trên đĩa và cũng không biết cấu trúc cây B+Tree index chạy ra sao.
    *   Nó tương tác với bộ máy ổ cứng thông qua giao diện **`IAccessMethod`**.
2.  **Trừu tượng hóa cách lấy Row ID (`IAccessMethod`):**
    *   Tùy thuộc vào kế hoạch chạy (Physical Plan), `OperatorExecutor` sẽ gọi `IAccessMethod`. Nếu dùng index, hệ thống nạp engine **`BPlusTreeManager`**; nếu quét hết bảng, hệ thống nạp **`HeapScan`**. Cả hai đều implement `IAccessMethod` để trả về Số định danh bản ghi `RID` (Row ID).
3.  **Cách ly lưu trữ đĩa thông qua `IFileManager`:**
    *   Bộ điều phối RAM **`BufferPoolManager`** khi hết bộ đệm hoặc khi cần ghi tệp tin sẽ không gọi trực tiếp API của OS mà thông qua Interface **`IFileManager`** (Cửa ngõ quản lý file). Việc này cho phép chúng ta dễ dàng đổi cơ chế lưu trữ (lưu trên file NTFS cục bộ, lưu trên ổ SSD trực tiếp - Raw Device, hay lưu trên Cloud Storage) bằng cách viết các class triển khai mới kế thừa `IFileManager`.
4.  **Kiểm soát khóa bất đồng bộ qua `LockManager`:**
    *   Khi `OperatorExecutor` duyệt dữ liệu, nó sẽ liên lạc với `LockManager` để xin cấp khóa (ví dụ: xin khóa đọc Shared Lock cho Row ID tương ứng). Nếu thành công, nó mới tiếp tục gọi `IAccessMethod` nạp trang. Việc này tách biệt hoàn toàn logic kiểm soát đồng thời khỏi logic lưu trữ.
5.  **Bảo vệ toàn vẹn qua `IConstraintValidator`:**
    *   Khi Executor làm nhiệm vụ ghi (như INSERT), nó sẽ gọi giao diện `IConstraintValidator`. Tùy theo thiết lập bảng, `ForeignKeyValidator` hay `PrimaryKeyValidator` sẽ được nạp vào để kiểm duyệt điều kiện logic, bảm đảm tính Integrity.
