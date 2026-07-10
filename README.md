# Kế hoạch 6 ngày - Thiết kế DBMS (Top-Down Approach)

## Phân tích hiện trạng

Đã review Layer 1 và Layer 2:

| Layer | Nội dung | Trạng thái |
|-------|----------|------------|
| Layer 1 | 8 nhánh chính (Storage Engine, Query Processing, Transaction & Concurrency, Security, Database Object & Metadata, Administration, Backup/Recovery/Logging, Communication & Connectivity) | ✅ Hoàn thành |
| Layer 2 | ~50 sub-modules chi tiết cho 8 nhánh | ✅ Hoàn thành |

### Nhận xét Layer 1 & 2

**Điểm mạnh:**
- Phân chia 8 nhánh hợp lý, bao phủ đầy đủ các thành phần cốt lõi của một DBMS
- Layer 2 chi tiết hóa mỗi nhánh với 5-12 sub-components, tương đương SQL Server architecture

**Góp ý nhỏ:**
- Nhánh `Administration > Threads Manager` nên xem xét đổi tên thành `Thread Pool Manager` cho rõ ràng hơn
- Có thể bổ sung `Statistics Manager` vào nhánh `Query Processing` (quan trọng cho Query Optimizer)
- `Communication & Connectivity` có thể thêm `Connection Pooling` như một sub-component riêng

---

## Deliverables tổng quan

| # | Deliverable | Mô tả |
|---|-------------|-------|
| D1 | Mindmap 3 Layers | Mindmap chính với Layer 1, 2, 3 (Mermaid format) |
| D2 | Mindmap Classes | Mindmap có class, abstract, interface, feature cho từng nhánh |
| D3 | Class Diagram Level 1 | Tổng quan toàn hệ thống, mối quan hệ giữa các module chính |
| D4 | Class Diagram chi tiết | Từng nhánh feature riêng biệt (8 diagrams) |
| D5 | Sequence Diagram Level 1 | Các flow chính (SELECT, INSERT, Transaction, Auth...) |
| D6 | Sequence Diagram chi tiết | Đầy đủ thành phần cho mỗi flow |
| D7 | TDD Design | Test-Driven Development plan cho toàn hệ thống |
| D8 | Unit & Integration Tests | Tất cả test cases |

---

## Kế hoạch 6 ngày chi tiết

### 📅 Ngày 1: Layer 3 + Mindmap 3 Layers (D1)

**Mục tiêu:** Hoàn thành Layer 3 (chi tiết nhất) và Mindmap tổng thể

| Task | Output |
|------|--------|
| Thiết kế Layer 3 cho tất cả 8 nhánh | `DBMS_layer3.txt` |
| Mindmap Layer 1-2-3 bằng Mermaid | `01_mindmap_3layers.md` |
| Review & chỉnh sửa | Đảm bảo tính nhất quán |

**File output:** `docs/01_mindmap_3layers.md`

---

### 📅 Ngày 2: Mindmap Classes + Class Diagram Level 1 (D2, D3)

**Mục tiêu:** Xác định classes/interfaces/abstracts cho mỗi nhánh, vẽ Class Diagram tổng quan

| Task | Output |
|------|--------|
| Xác định class, abstract class, interface cho mỗi sub-component | `02_mindmap_classes.md` |
| Vẽ Class Diagram Level 1 (tổng quan) bằng Mermaid | `03_class_diagram_level1.md` |
| Đối chiếu mindmap ↔ class diagram đủ chưa | Checklist đối chiếu |

**File output:** `docs/02_mindmap_classes.md`, `docs/03_class_diagram_level1.md`

---

### 📅 Ngày 3: Class Diagram chi tiết từng nhánh (D4)

**Mục tiêu:** 8 Class Diagrams chi tiết, mỗi diagram cho 1 nhánh feature

| Task | Output |
|------|--------|
| Class Diagram - Storage Engine | `04_class_detail_storage_engine.md` |
| Class Diagram - Query Processing | `04_class_detail_query_processing.md` |
| Class Diagram - Transaction & Concurrency | `04_class_detail_transaction.md` |
| Class Diagram - Security | `04_class_detail_security.md` |
| Class Diagram - Database Object & Metadata | `04_class_detail_db_object.md` |
| Class Diagram - Administration | `04_class_detail_administration.md` |
| Class Diagram - Backup, Recovery & Logging | `04_class_detail_backup_recovery.md` |
| Class Diagram - Communication & Connectivity | `04_class_detail_communication.md` |

**File output:** 8 files trong `docs/`

---

### 📅 Ngày 4: Sequence Diagrams (D5, D6)

**Mục tiêu:** Thiết kế Sequence Diagrams cho các flow chính

| Task | Output |
|------|--------|
| Sequence Diagram Level 1 (overview flows) | `05_sequence_diagram_level1.md` |
| Sequence chi tiết: SELECT Query Flow | `06_seq_select_query.md` |
| Sequence chi tiết: INSERT/UPDATE/DELETE Flow | `06_seq_dml_operations.md` |
| Sequence chi tiết: Transaction Flow | `06_seq_transaction.md` |
| Sequence chi tiết: Authentication & Authorization | `06_seq_auth.md` |
| Sequence chi tiết: Connection & Session | `06_seq_connection.md` |
| Sequence chi tiết: Backup & Recovery | `06_seq_backup_recovery.md` |

**File output:** 7 files trong `docs/`

---

### 📅 Ngày 5: TDD Design + Unit Test Cases (D7, D8 phần 1)

**Mục tiêu:** Thiết kế TDD, viết unit test cases cho 8 nhánh

| Task | Output |
|------|--------|
| TDD Strategy & Test Plan tổng quan | `07_tdd_design.md` |
| Unit Tests - Storage Engine | `tests/unit/storage_engine_tests.md` |
| Unit Tests - Query Processing | `tests/unit/query_processing_tests.md` |
| Unit Tests - Transaction & Concurrency | `tests/unit/transaction_tests.md` |
| Unit Tests - Security | `tests/unit/security_tests.md` |
| Unit Tests - Database Object & Metadata | `tests/unit/db_object_tests.md` |
| Unit Tests - Administration | `tests/unit/administration_tests.md` |
| Unit Tests - Backup, Recovery & Logging | `tests/unit/backup_recovery_tests.md` |
| Unit Tests - Communication & Connectivity | `tests/unit/communication_tests.md` |

**File output:** 9 files

---

### 📅 Ngày 6: Integration Test Cases + Review tổng thể (D8 phần 2)

**Mục tiêu:** Integration tests, đối chiếu tổng thể, hoàn thiện documentation

| Task | Output |
|------|--------|
| Integration Tests - End-to-End Query Flow | `tests/integration/e2e_query_tests.md` |
| Integration Tests - Transaction + Concurrency | `tests/integration/transaction_tests.md` |
| Integration Tests - Security + Connection | `tests/integration/security_connection_tests.md` |
| Integration Tests - Backup & Recovery | `tests/integration/backup_recovery_tests.md` |
| Đối chiếu Mindmap ↔ Class Diagram ↔ Tests | `08_cross_reference_checklist.md` |
| README tổng hợp project | `README.md` |

**File output:** 6 files

---

## Cấu trúc thư mục output

```
DBMS/
├── README.md
├── DBMS_layer1.txt                    (đã có)
├── DBMS_layer2.txt                    (đã có)
├── DBMS_layer3.txt                    (mới)
├── docs/
│   ├── 01_mindmap_3layers.md
│   ├── 02_mindmap_classes.md
│   ├── 03_class_diagram_level1.md
│   ├── 04_class_detail_storage_engine.md
│   ├── 04_class_detail_query_processing.md
│   ├── 04_class_detail_transaction.md
│   ├── 04_class_detail_security.md
│   ├── 04_class_detail_db_object.md
│   ├── 04_class_detail_administration.md
│   ├── 04_class_detail_backup_recovery.md
│   ├── 04_class_detail_communication.md
│   ├── 05_sequence_diagram_level1.md
│   ├── 06_seq_select_query.md
│   ├── 06_seq_dml_operations.md
│   ├── 06_seq_transaction.md
│   ├── 06_seq_auth.md
│   ├── 06_seq_connection.md
│   ├── 06_seq_backup_recovery.md
│   └── 08_cross_reference_checklist.md
├── tests/
│   ├── 07_tdd_design.md
│   ├── unit/
│   │   ├── storage_engine_tests.md
│   │   ├── query_processing_tests.md
│   │   ├── transaction_tests.md
│   │   ├── security_tests.md
│   │   ├── db_object_tests.md
│   │   ├── administration_tests.md
│   │   ├── backup_recovery_tests.md
│   │   └── communication_tests.md
│   └── integration/
│       ├── e2e_query_tests.md
│       ├── transaction_tests.md
│       ├── security_connection_tests.md
│       └── backup_recovery_tests.md
```

## Format sử dụng

- **Mindmaps**: Mermaid `mindmap` syntax
- **Class Diagrams**: Mermaid `classDiagram` syntax
- **Sequence Diagrams**: Mermaid `sequenceDiagram` syntax
- **Tất cả output**: file `.md` để push lên GitHub

## Verification Plan

### Automated Verification
- Validate tất cả Mermaid syntax bằng Mermaid Live Editor hoặc markdown preview
- Đối chiếu checklist: mỗi component trong mindmap phải có class tương ứng trong class diagram
- Mỗi class trong class diagram phải có ít nhất 1 unit test

### Manual Verification
- Review từng deliverable theo checklist đối chiếu
- Đảm bảo tất cả file render đúng trên GitHub
