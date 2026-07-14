# DBMS Layer 2: Functional Breakdown

This document illustrates the Layer-2 subsystem breakdown for each of the core 8 systems in the DBMS, structured in a symmetrical topology.

```mermaid
graph LR
    %% Styles & Colors
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px;
    classDef root fill:#ff9999,stroke:#333,stroke-width:2px,font-weight:bold;
    classDef layer1 fill:#99ccff,stroke:#333,stroke-width:1.5px,font-weight:bold;
    classDef layer2 fill:#ccffcc,stroke:#333,stroke-width:1px;

    %% Root
    db((DBMS)):::root

    %% BÊN TRÁI
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

    %% BÊN PHẢI
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

## Giải Nghĩa Các Phân Hệ Layer 2

Layer 2 là bước phân rã thứ nhất từ các Domain cốt lõi (Layer 1). Mỗi nhánh của Layer 1 được tách ra thành các Module (phân hệ) độc lập (Layer 2) nhằm phân định rõ ranh giới nghiệp vụ (bounded context):

### Nửa Bên Trái (Core Engine Group)
* **Storage Engine:** Phân rã thành 6 Module trị trách nhiệm chuyên biệt: tương tác đĩa, quản lý bộ đệm, định dạng cấu trúc file & trang vật lý, tối ưu không gian và tạo phương thức truy xuất (bản ghi, mô hình chỉ mục).
* **Query Processing:** Phân rã dọc theo vòng đời trôi chảy của một câu truy vấn SQL (Pipeline): từ phân tích cú pháp thô (Parser), tra cứu xác thực với metadata (Validation), lên kế hoạch đọc đĩa (Optimizer), tới thực thi vật lý (Executor) và cuối cùng đóng gói format dữ liệu gửi phản hồi (Result Processing).
* **Transaction & Concurrency:** Đảm nhiệm trọn gói yếu tố ACID. Tách biệt hoàn toàn việc lưu giữ trạng thái giao dịch (Transaction Manager), quản lý khóa chống xung đột (Lock Manager), theo dõi chu trình bế tắc (Deadlock Handler) và quản lý phiên bản dữ liệu song song (MVCC/Isolation).
* **Security:** Tập trung vào kiểm soát bảo mật hệ thống: từ lớp định danh user đầu vào (Authentication), ủy quyền cấp độ tài nguyên (Authorization), mã hóa ổ đĩa (Encryption) đến lưu vết hành vi (Auditing).

### Nửa Bên Phải (Management & Utility Group)
* **Database Object & Metadata:** Quản lý vòng đời (lifecycle) của mọi cấu trúc logic mà end-user khai báo trên hệ thống (Schema, Table, Column, Index, View...). Đây đóng vai trò như từ điển Data Dictionary của toàn bộ DBMS.
* **Administration:** Trợ lý đặc quyền dành cho DBA: cung cấp module giám sát tình trạng hệ thống, cấu hình tham số database memory lúc runtime và cơ chế import/export hiệu suất cao.
* **Backup, Recovery & Logging:** Phân tách rõ quy trình phục hồi khẩn cấp: Ghi dữ liệu tức thời qua nhật ký biến thiên (Transaction WAL) để cứu vãn hệ thống ngay khi cúp điện, và tạo bản snapshot bảo vệ định kỳ (Backup Manager) chống rủi ro hỏng đĩa vật lý.
* **Communication & Connectivity:** Lớp Adapter nằm sát ngoài ranh giới internet. Điều hướng và quản lý cấu hình các cổng kết nối TCP (Connection), phiên hoạt động cục bộ (Session), phân giải gói tin theo chuẩn giao thức (Protocol Handler) trước khi đưa payload vào Core Engine.
