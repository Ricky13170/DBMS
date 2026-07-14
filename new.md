# Kế Hoạch 5 Ngày - DBMS Design (Top-Down + Feature-First)

## Approach được chọn

Kết hợp **Top-down (quản lý)** + **Feature-first bottom-up (người bạn)**:
- Mindmap + Class Diagram: top-down toàn hệ thống trước
- Sequence Diagram: bottom-up từng operation nhỏ → gộp dần theo feature
- Ưu tiên **Storage Engine** → sau đó mở rộng ra 7 nhánh còn lại

---

## Deliverables Tổng Quan

| # | Deliverable | File |
|---|-------------|------|
| D1 | Mindmap 3 Layers | `docs/01_mindmap_3layers.md` |
| D2 | Mindmap Classes + Methods (L4) | [docs/02_mindmap_classes.md](file:///d:/Th%E1%BB%B1c%20T%E1%BA%ADp/bbv/DBMS/docs/02_mindmap_classes.md) |
| D3 | Class Diagram Level 1 (toàn hệ thống) | [docs/03_class_diagram_level1.md](file:///d:/Th%E1%BB%B1c%20T%E1%BA%ADp/bbv/DBMS/docs/03_class_diagram_level1.md) |
| D4 | Class Diagram chi tiết (8 nhánh) | `docs/04_class_detail_*.md` |
| D5 | Sequence Diagram Level 1 | `docs/05_sequence_level1.md` |
| D6 | Sequence chi tiết per feature | `docs/06_seq_*.md` |
| D7 | TDD Design | `tests/07_tdd_design.md` |
| D8 | Unit + Integration Tests | `tests/unit/` + `tests/integration/` |

---

## Ngày 1 — Mindmap (D1 + D2)

**Mục tiêu:** Có mindmap đầy đủ 3 layer + mindmap classes với tên class/method

| Task | Output |
|------|--------|
| Mindmap Layer 1→2→3 toàn bộ DBMS (Mermaid) | `01_mindmap_3layers.md` |
| Mindmap Classes: thêm class name, abstract, interface, method tại L4 | `02_mindmap_classes.md` |
| Đối chiếu L3 checklist: đủ 8 nhánh, 50+ sub-components | Checklist nội tuyến |

> **Ưu tiên đi sâu:** Storage Engine → Query Processing → Transaction → Security → ...

---

## Ngày 2 — Class Diagram (D3 + D4)

**Mục tiêu:** Class Diagram formal — Level 1 tổng quan và chi tiết từng nhánh

| Task | Output |
|------|--------|
| Class Diagram Level 1: 8 module, relationships | `03_class_diagram_level1.md` |
| Class Detail — Storage Engine (6 sub-modules) | `04_class_detail_storage_engine.md` |
| Class Detail — Query Processing | `04_class_detail_query_processing.md` |
| Class Detail — Transaction & Concurrency | `04_class_detail_transaction.md` |
| Class Detail — Security | `04_class_detail_security.md` |
| Class Detail — DB Object & Metadata | `04_class_detail_db_object.md` |
| Class Detail — Administration | `04_class_detail_administration.md` |
| Class Detail — Backup, Recovery & Logging | `04_class_detail_backup_recovery.md` |
| Class Detail — Communication & Connectivity | `04_class_detail_communication.md` |
| Đối chiếu: mỗi node D2 có class tương ứng D4 | Cross-check |

> **Trong mỗi class detail:** properties, methods, tên hàm đầy đủ  
> **Relationships:** inheritance (`<|--`), composition (`*--`), dependency (`..>`)

---

## Ngày 3 — Sequence Diagram (D5 + D6)

**Mục tiêu:** Vẽ sequence từ bottom-up, gộp dần theo feature

### Level 1 (D5) — High-level flows
| Flow | Output |
|------|--------|
| SELECT Query end-to-end | `05_sequence_level1.md` |
| INSERT/UPDATE/DELETE | (cùng file) |
| Transaction commit/rollback | (cùng file) |
| Auth + Connection lifecycle | (cùng file) |

### Chi tiết (D6) — Per feature, Storage Engine trước
| Flow | Output |
|------|--------|
| File Management: createFile → deleteFile → openFile → allocateSpace | `06a_seq_file_management.md` |
| Page Management: formatPage → readPage → writePage | `06b_seq_page_management.md` |
| Buffer Management: pinPage → dirtyWrite → flush | `06c_seq_buffer_management.md` |
| DML Operations | `06d_seq_dml_operations.md` |
| Transaction: BEGIN → COMMIT → ROLLBACK | `06e_seq_transaction.md` |
| Auth & Authorization | `06f_seq_auth.md` |
| Backup & Recovery | `06g_seq_backup_recovery.md` |

> **Cách vẽ sequence** theo người bạn: viết sequence nhỏ (createFile) → gộp lên (File Allocator) → gộp lên (File Management)

---

## Ngày 4 — TDD Design + Unit Tests (D7 + D8 phần 1)

**Mục tiêu:** Test-driven plan và unit test cases cho 8 nhánh

| Task | Output |
|------|--------|
| TDD Strategy tổng quan | `tests/07_tdd_design.md` |
| Unit Tests — Storage Engine | `tests/unit/storage_engine_tests.md` |
| Unit Tests — Query Processing | `tests/unit/query_processing_tests.md` |
| Unit Tests — Transaction | `tests/unit/transaction_tests.md` |
| Unit Tests — Security | `tests/unit/security_tests.md` |
| Unit Tests — DB Object & Metadata | `tests/unit/db_object_tests.md` |
| Unit Tests — Administration | `tests/unit/administration_tests.md` |
| Unit Tests — Backup & Recovery | `tests/unit/backup_recovery_tests.md` |
| Unit Tests — Communication | `tests/unit/communication_tests.md` |

> **Mỗi test case gồm:** Given / When / Then + tên method được test + class liên quan

---

## Ngày 5 — Integration Tests + Review Tổng Thể (D8 phần 2)

**Mục tiêu:** Integration tests + đối chiếu toàn bộ với mindmap D1

| Task | Output |
|------|--------|
| Integration Tests — E2E Query Flow | `tests/integration/e2e_query_tests.md` |
| Integration Tests — Transaction + Concurrency | `tests/integration/transaction_tests.md` |
| Integration Tests — Security + Connection | `tests/integration/security_connection_tests.md` |
| Integration Tests — Backup & Recovery | `tests/integration/backup_recovery_tests.md` |
| Cross-reference Checklist: Mindmap ↔ Class ↔ Sequence ↔ Tests | `docs/08_cross_reference_checklist.md` |
| README tổng hợp project | `README.md` |

---

## Cấu Trúc Thư Mục

```
DBMS/
├── README.md
├── DBMS_layer1.txt       (đã có)
├── DBMS_layer2.txt       (đã có)
├── DBMS_layer3.txt       (đã có)
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
│   ├── 05_sequence_level1.md
│   ├── 06a_seq_file_management.md
│   ├── 06b_seq_page_management.md
│   ├── 06c_seq_buffer_management.md
│   ├── 06d_seq_dml_operations.md
│   ├── 06e_seq_transaction.md
│   ├── 06f_seq_auth.md
│   ├── 06g_seq_backup_recovery.md
│   └── 08_cross_reference_checklist.md
└── tests/
    ├── 07_tdd_design.md
    ├── unit/
    │   ├── storage_engine_tests.md
    │   ├── query_processing_tests.md
    │   ├── transaction_tests.md
    │   ├── security_tests.md
    │   ├── db_object_tests.md
    │   ├── administration_tests.md
    │   ├── backup_recovery_tests.md
    │   └── communication_tests.md
    └── integration/
        ├── e2e_query_tests.md
        ├── transaction_tests.md
        ├── security_connection_tests.md
        └── backup_recovery_tests.md
```

---

## Format

- **Mindmaps**: Mermaid `mindmap` syntax
- **Class Diagrams**: Mermaid `classDiagram` syntax
- **Sequence Diagrams**: Mermaid `sequenceDiagram` syntax
- **Tất cả**: file [.md](file:///d:/Th%E1%BB%B1c%20T%E1%BA%ADp/bbv/DBMS/implementation_plan.md) render được trên GitHub
