# Danh sách các Lớp (Classes), Interfaces, và Abstract Classes hệ thống DBMS

Tài liệu này xác định chi tiết cấu trúc hướng đối tượng các Classes, Abstract Classes, và Interfaces cho toàn bộ 8 nhánh chính và các sub-components tương ứng. Đây là cơ sở dữ liệu thiết kế quan trọng cho việc vẽ Class Diagram Level 1 và chi tiết.

---

## 1. Storage Engine
Tầng quản lý đĩa vật lý, lưu trữ record, trang dữ liệu (Page), bộ nhớ đệm (Buffer Pool) và chỉ mục.

### 1.1 Data File Manager
*   `interface IFileManager`: Giao diện tương tác hệ điều hành để đọc/ghi thô file.
*   `class OSFileManager : IFileManager`: Triển khai đọc/ghi tệp tin thông qua HĐH Windows/Linux API.
*   `class DataFileRegistry`: Quản lý danh sách, đường dẫn và metadata của các file dữ liệu (`.mdf`, `.ndf`).
*   `class FileDescriptor`: Đại diện cho một file handle đang mở và vị trí con trỏ đĩa.
*   `class FileGrowthManager`: Quản lý logic tự động tăng dung lượng file (Auto-growth) khi hết chỗ trống.

### 1.2 Page Manager
*   `abstract class BasePage`: Lớp cơ sở trừu tượng cho tất cả các loại Page trong DBMS.
*   `class DataPage : BasePage`: Định dạng trang chứa dữ liệu Record thực tế.
*   `class IndexPage : BasePage`: Định dạng trang chứa các Node của cây chỉ mục B+Tree.
*   `class PageHeader`: Lưu siêu thông tin của trang (như PageID, LSN, PageType, FreeSpaceOffset).
*   `class SlotDirectory`: Quản lý vị trí (offset) của các record có độ dài biến đổi ở cuối trang.
*   `class FreeSpaceManager (FSM)`: Quản lý và tính toán dung lượng trống để chèn record mới.

### 1.3 Buffer Pool Manager
*   `class BufferFrame`: Đại diện cho một khung chứa trang (Page) đang nằm trên bộ nhớ RAM.
*   `interface IReplacementPolicy`: Giao diện cho thuật toán tráo trang khi đầy pool.
*   `class LRUReplacementPolicy : IReplacementPolicy`: Triển khai hoán đổi page theo Least Recently Used.
*   `class ClockReplacementPolicy : IReplacementPolicy`: Triển khai hoán đổi page theo thuật toán Clock.
*   `class BufferPoolManager`: Điều phối luân chuyển Pages giữa RAM và Đĩa đệm.
*   `class DirtyPageWriter`: Một Background Thread định kỳ ghi các Dirty Pages (trang bị sửa đổi) xuống đĩa.

### 1.4 Record Manager
*   `class Record`: Đại diện cho một hàng dữ liệu vật lý (Row data under byte array support).
*   `class RecordLayout`: Định nghĩa schema byte của record (độ dài cột, null bitmap, variable-length offset).
*   `class RecordID (RID)`: Cấu trúc xác định vị trí thực tế của Record (gồm `PageID` + `SlotNumber`).
*   `class VariableLengthManager`: Xử lý lưu trữ các trường dữ liệu động vượt kích thước chuẩn (`varchar(max)`, `text`).

### 1.5 Access Methods (Nhánh ưu tiên)
*   `interface IAccessMethod`: Giao diện duyệt và truy xuất dữ liệu chung.
*   `class BPlusTreeManager : IAccessMethod`: Quản lý thuật toán chèn, xóa, tách trang (`splitLeafNode()`), gộp trang (`mergeNodes()`) trên cây B+Tree.
*   `class HeapScan : IAccessMethod`: Thực thi quét tuần tự toàn bộ các Pages của một bảng không có index.
*   `class IndexIterator`: Bộ iterator để quét tuần tự các Leaf Nodes liên tiếp trên cây B+Tree phục vụ range scan.

### 1.6 Storage Allocation
*   `class ExtentManager`: Quản lý việc cấp phát và thu hồi Extent (nhóm 8 pages liên tiếp).
*   `class SegmentManager`: Quản lý các extents cấp riêng cho một đối tượng cụ thể (Table Segment hoặc Index Segment).
*   `class SpaceReclaimManager`: Thu gom rác vật lý và giải phóng dung lượng đĩa khi drop tablespace hoặc tables.

---

## 2. Query Processing
Tầng dịch trực tiếp các câu lệnh SQL từ client thành kế hoạch thực thi tối ưu và trả về kết quả.

### 2.1 SQL Parser
*   `class SQLParser`: Giao diện điều phối phân tích cú pháp SQL.
*   `class Lexer`: Bộ phân tích từ vựng (phân rã chuỗi SQL thành Tokens).
*   `class Parser`: Bộ phân tích ngữ pháp để dựng cây AST.
*   `abstract class AstNode`: Lớp đại diện cho một nút trong cây cú pháp trừu tượng (AST).
*   `class QueryAst : AstNode`: Nút gốc thể hiện toàn bộ câu lệnh SQL đã parse.

### 2.2 Query Validation
*   `class SemanticValidator`: Kiểm tra xem các bảng, cột có tồn tại thực tế và đúng kiểu dữ liệu không.
*   `interface IMetadataCatalogLookup`: Giao diện tra cứu siêu dữ liệu từ catalog.
*   `class PrivilegeChecker`: Xác thực user biên dịch query có quyền thao tác trên bảng/cột đó không.
*   `class IntegrityConstraintLookup`: Tra cứu các ràng buộc khóa ngoại/check ngay lúc biên dịch để hỗ trợ tối ưu logic.

### 2.3 Query Optimizer (Nhánh ưu tiên)
*   `class QueryOptimizer`: Quản lý chu trình tối ưu hóa.
*   `abstract class LogicalOperator`: Các toán tử logic (như `LogicalScan`, `LogicalJoin`, `LogicalFilter`).
*   `abstract class PhysicalOperator`: Các toán tử vật lý (như `IndexScan`, `HashJoin`, `NestedLoopJoin`, `Filter`).
*   `class PlanCache`: Bộ nhớ đệm lưu trữ các cấu trúc `PhysicalPlan` đã tối ưu để tái sử dụng.
*   `interface IOptimizerEngine`: Giao diện bộ tối ưu.
*   `class RuleBasedOptimizer : IOptimizerEngine`: Tối ưu hóa dựa trên quy tắc biến đổi logic (áp dụng đại số quan hệ).
*   `class CostBasedOptimizer : IOptimizerEngine`: Tối ưu hóa dựa trên chi phí tài nguyên (áp dụng mô hình ước lượng CPU, I/O cost).
*   `class CostEstimator`: Lớp tính toán chi phí (I/O, CPU) dựa trên thống kê cơ sở dữ liệu (`Statistics`).

### 2.4 Query Execution (Nhánh ưu tiên)
*   `interface IExecutionPipeline`: Điều hành tiến trình chạy luồng dữ liệu song song (parallel execution execution pipelines).
*   `abstract class OperatorExecutor (Volcano Iterator)`: Kế thừa mẫu thiết kế Volcano, cung cấp 3 methods cơ bản: `open()`, `next()`, `close()`.
*   `class ScanExecutor : OperatorExecutor`: Toán tử quét Heap / Index.
*   `class ProjectExecutor : OperatorExecutor`: Toán tử lọc cột được chọn.
*   `class FilterExecutor : OperatorExecutor`: Toán tử lọc dòng thỏa mãn WHERE clause.
*   `class HashJoinExecutor : OperatorExecutor`: Toán tử thực hiện Hash Join.
*   `class NestedLoopJoinExecutor : OperatorExecutor`: Toán tử thực hiện Nested Loop Join.

### 2.5 Result Processing
*   `class ResultSet`: Lưu cấu trúc bảng dữ liệu kết quả tạm thời được sinh ra bởi toán tử gốc (Root Executor).
*   `class ResultCursor`: Bộ con trỏ hỗ trợ duyệt dữ liệu kết quả định hướng (Next, Fetch, Seek) cho Client.
*   `class OutputBuffer`: Quản lý bộ đệm truyền tin để gửi kết quả từng phần (pagination/chunk) về Network Protocol layer.

---

## 3. Transaction & Concurrency
Tầng quản lý sự song song và duy trì tính cô lập (Isolation) của các giao dịch.

### 3.1 Transaction Manager
*   `interface ITransaction`: Interface đại diện cho một phiên giao dịch đang chạy.
*   `class Transaction : ITransaction`: Chứa trạng thái của Transaction (Active, Committed, Aborted, ...).
*   `class TransactionManager`: Quản lý vòng đời transaction (`beginTransaction()`, `commit()`, `abort()`).
*   `class TransactionTable`: Quản lý danh sách tất cả các transactions đang hoạt động trong hệ thống.
*   `class Savepoint`: Điểm đánh dấu rollback cục bộ trong transaction.

### 3.2 Lock Manager (Nhánh ưu tiên)
*   `class LockRequest`: Lưu trữ thông tin một yêu cầu khóa (gồm TransactionID, LockMode, ResourceID).
*   `class LockTable`: Cấu trúc Hash Table quản lý tất cả các LockRequest trên tài nguyên.
*   `class LockManager`: Cấp phát (`acquireLock()`) và giải phóng khóa (`releaseLock()`).
*   `class LockEscalationManager`: Quản lý nâng cấp khóa (ví dụ: gộp 5000 khóa Row thành 1 khóa Table).

### 3.3 Deadlock Handler
*   `interface IDeadlockDetector`: Giao diện bộ phát hiện deadlock.
*   `class DeadlockDetectionThread : IDeadlockDetector`: Chạy định kỳ, dựng đồ thị phụ thuộc (Wait-For Graph) và phát hiện chu trình.
*   `class VictimSelector`: Giải thuật chọn Transaction làm vật thế mạng để rollback dựa trên cost.

### 3.4 Isolation Manager
*   `class IsolationLevelController`: Triển khai luật hành vi ứng với 4 cấp độ cách ly (Read Uncommitted, Read Committed, Repeatable Read, Serializable).
*   `class PhantomProtection`: Logic bảo vệ chống lỗi đọc bóng ma (sử dụng Range Lock / Key-Range lock).

### 3.5 Concurrency Management (MVCC Engine - Nhánh ưu tiên)
*   `class MvccEngine`: Quản lý cơ chế đa phiên bản.
*   `class VersionStore`: Không gian lưu trữ các phiên bản cũ của record (TempDB hoặc Undo Tablespace).
*   `class VersionChainManager`: Quản lý liên kết (chỉ mục con trỏ rollback) giữa dòng hiện tại và các phiên bản cũ.
*   `class VisibilityChecker`: Xác định transaction có được nhìn thấy phiên bản record cụ thể nào đó không dựa trên Transaction Snapshot.
*   `class VersionGarbageCollector`: Background Thread thu hồi các phiên bản phiên cũ không còn transaction nào tham chiếu.

---

## 4. Database Object & Metadata
Quản lý định nghĩa cấu trúc bảng, catalog, kiểu dữ liệu, các ràng buộc và view.

### 4.1 Database Manager
*   `interface IDatabase`: Giao diện của một thực thể Database.
*   `class Database : IDatabase`: Đại diện cho cơ sở dữ liệu cụ thể (chứa các file cấu hình, meta files).
*   `class DatabaseStateController`: Điều khiển trạng thái Online, Offline, Restoring, Suspect của DB.

### 4.2 Schema Manager
*   `class Schema`: Quản lý namespace (lớp bọc ngoài tables, views để tránh đụng độ tên, ví dụ: `dbo`).
*   `class SchemaResolver`: Giải quyết tên đầy đủ của table (như `dbo.Customer` thành Object ID tương ứng).

### 4.3 Table Manager (Nhánh ưu tiên)
*   `interface ITable`: Đại diện cho một Table logic.
*   `class Table : ITable`: Triển khai Table logic (gồm Schema, Columns, Constraints metadata).
*   `class PartitionManager`: Chia bảng thành các Partition dựa trên cột phân vùng (Partition Key).

### 4.4 Column Manager
*   `class Column`: Lưu metadata của một cột (Name, Ordinal Position, DefaultValue, IsNullable).
*   `class IdentityGenerator`: Tự động điền số tăng dần cho cột Identity.

### 4.5 Data Type Manager
*   `abstract class DataType`: Lớp cơ sở cho các kiểu dữ liệu trong SQL.
*   `class Integertype : DataType`, `class Varchartype : DataType`, `class DatetimeType : DataType`: Các class cụ thể kế thừa kiểu dữ liệu.
*   `class TypeConverter`: Quản lý việc ép kiểu tự động (implicit cast) hoặc cưỡng ép (explicit cast).

### 4.6 Index Manager
*   `class IndexDefinition`: Chứa Meta thông tin index (cột tham gia, Index Type: Clustered/Non-Clustered).
*   `class IndexRegister`: Quản lý việc đăng ký, drop index.

### 4.7 Constraint Manager (Nhánh ưu tiên)
*   `interface IConstraintValidator`: Giao diện Validate dữ liệu.
*   `class PrimaryKeyValidator : IConstraintValidator`: Kiểm tra tính duy nhất và không Null của khóa chính.
*   `class ForeignKeyValidator : IConstraintValidator`: Kiểm tra tính toàn vẹn tham chiếu.
*   `class CheckConstraintEvaluator : IConstraintValidator`: Tính toán biểu thức logic của CHECK constraint.
*   `class CascadeActionManager`: Kích hoạt hành động xóa/sửa dây chuyền (Cascade).

### 4.8 View Manager
*   `class ViewDefinition`: Lưu câu lệnh SELECT gốc làm định nghĩa cho View.
*   `class ViewResolver`: Thay thế tên View thành câu SELECT lồng vào trong cây AST của Parser lúc biên dịch.

### 4.9 Programmable Objects
*   `class StoredProcedure`: Quản lý định nghĩa Code khối và các lệnh thực thi tuần tự.
*   `class UserDefinedFunction`: Quản lý hàm tự định nghĩa, trả về Scalar hoặc Table.
*   `class Trigger`: Quản lý logic chạy tự động ứng với các sự kiện DML (INSERT/UPDATE/DELETE).
*   `class ParameterManager`: Quản lý danh sách, kiểu, hướng (IN/OUT) của các tham số đầu vào.

### 4.10 Catalog Manager (Nhánh ưu tiên)
*   `class SystemCatalogTable`: Biểu diễn các bảng metadata hệ thống (như `sys.tables`, `sys.columns`).
*   `class MetadataWriter`: Ghi đè cấu trúc data DDL xuống System Catalog Tables.
*   `class MetadataCache`: Lưu đệm thông tin catalog trên RAM.
*   `class DependencyTracker`: Quản lý đồ thị phụ thuộc của toàn bộ cấu trúc DB.
*   `class ObjectIdentifier`: Cấp phát ID duy nhất cho tất cả các đối tượng được đăng ký vào Catalog.

---

## 5. Security
Tầng quản lý danh tính, phân quyền, mã hóa và ghi vết.

### 5.1 Authentication
*   `interface ICredentialValidator`: Giao diện xác thực kiểm tra mật khẩu.
*   `class SqlAuthValidator : ICredentialValidator`: Xác thực bằng tài khoản đăng ký trong database.
*   `class LoginManager`: Quản lý các phiên đăng nhập (Login Sessions).

### 5.2 Authorization & Access Control
*   `interface IPrivilegeEvaluator`: Giao diện kiểm tra quyền.
*   `class PermissionResolver`: Phân tích và tổng hợp toàn bộ quyền từ Group/Role gán cho User.
*   `class RowLevelSecurityFilter`: Tự động nạp thêm mệnh đề filter vào WHERE của Query dựa trên Security Policy của user.
*   `class ColumnLevelSecurityMasker`: Che giấu dữ liệu nhạy cảm ở cột đối với các user không đủ thẩm quyền.

### 5.3 User & Role Management
*   `class UserCatalog`: Registry cơ sở dữ liệu lưu thông tin danh sách Users.
*   `class RoleCatalog`: Registry cơ sở dữ liệu lưu thông tin danh sách Roles.
*   `class AccountLifecycleManager`: Quản lý việc tạo, khóa, mở khóa, khóa thời gian (lockout) tài khoản.

### 5.4 Encryption
*   `class TransparentDataEncryption (TDE)`: Mã hóa mức block đĩa khi ghi xuống (data-at-rest).
*   `interface ITransportEncryptor`: Giao diện mã hóa TLS/SSL lớp truyền gói tin (data-in-transit).

### 5.5 Auditing
*   `class AuditLogWriter`: Ghi vết các sự kiện bảo mật (nhập sai pass, truy cập bảng nhạy cảm) vào file audit độc lập.

---

## 6. Administration
Tầng giám sát hiệu năng, cấu hình hệ thống, bảo trì và quản lý tiến trình.

### 6.1 Monitoring
*   `class PerformanceCollector`: Thu thập thông số IO, RAM, CPU, Lock Wait.
*   `class SlowQueryProfiler`: Ghi nhận và phân tích các câu truy vấn chạy vượt ngưỡng thời gian quy định.

### 6.2 Configuration
*   `class ConfigRegistry`: Lưu trữ cấu hình key-value của Engine (như Max Memory, Max Degree of Parallelism).
*   `class DynamicParameterReloader`: Nạp lại cấu hình nóng mà không cần khởi động lại DBMS.

### 6.3 Utilities & tools
*   `class DbcEngine`: Bộ thực thi các lệnh bảo trì mức sâu (như DBCC CHECKDB trong SQL Server).
*   `class ResourceGovernor`: Giới hạn mức trần tài nguyên RAM/CPU cho mỗi Resource Pool.

### 6.4 Database Maintenance
*   `class StatisticsCollector`: Thu thập tần suất phân bố dữ liệu trên cột để giúp CBO tính toán chi phí chính xác.
*   `class PageVerifier`: Chạy kiểm tra Checksum trên các trang đĩa để phát hiện sớm các hỏng hóc phần cứng (bit rot).
*   `class IndexMaintenanceAgent`: Thực thi lệnh rebuild/reorganize chỉ mục định kỳ ngăn phân mảnh B+Tree.

### 6.5 Import & Export
*   `class BulkCopyLoader`: Thực thi nạp dữ liệu tốc độ cực cao ghi trực tiếp xuống File Manager bỏ qua Transaction Log.
*   `interface IDataImporter`: Giao diện nạp dữ liệu định dạng ngoài (CSV, JSON).

### 6.6 Threads Manager
*   `class WorkerThreadPool`: Quản lý pool các worker thread thực thi nhiệm vụ song song.
*   `class TaskScheduler`: Lập lịch chạy các tác vụ định kỳ của hệ thống (Maintenance, Backup).

---

## 7. Backup, Recovery & Logging
Duy trì tính bền vững (Durability) và hỗ trợ phục hồi dữ liệu khi gặp sự cố phần cứng/phần mềm.

### 7.1 Transaction Logging
*   `class Lsn`: Số nhật ký tuần tự (Log Sequence Number) đại diện cho vị trí bản ghi log.
*   `interface IWalWriter`: Interface ghi log xuống đĩa.
*   `class WalManager`: Điều phối cơ chế Write-Ahead Logging (luật WAL: phải ghi log trước khi ghi dirty page).
*   `class LogBuffer`: Bộ nhớ đệm log trước khi flush xuống đĩa.

### 7.2 Checkpoint Manager
*   `class Checkpointer`: Điều phối hoạt động ghi chốt Checkpoint để giảm thiểu thời gian Recovery khi gặp crash.
*   `class DirtyPageFlushCoordinator`: Tìm và đẩy các dirty page xuống đĩa hiệu quả mà không nghẽn mạng I/O.

### 7.3 High Availability Support
*   `class ReplicationSender`: Luồng gửi log cho các Node Secondary.
*   `class ReplicationReceiver`: Nhận log từ Node Primary và nạp vào hàng đợi.

### 7.4 Recovery Manager
*   `interface ILogApplier`: Giao diện apply nhật ký Log.
*   `class RedoLogApplier : ILogApplier`: Quét dữ liệu log từ checkpoint trước và replay các transaction đã commit (REDO).
*   `class UndoLogApplier : ILogApplier`: Quét dữ liệu log và hoàn tác các transaction chưa commit tại thời điểm crash (UNDO).
*   `class RecoveryManager`: Điều khiển quá trình ARIES Recovery (Analysis, Redo, Undo) khi khởi động lại hệ thống sau crash.

### 7.5 Backup & Restore Manager
*   `class BackupEngine`: Trích xuất snapshot vật lý hoặc logical của DB.
*   `class RestorePlanner`: Phân tích và sinh kế hoạch khôi phục (ví dụ: Full Backup + Differential Backup + Log Backup).

---

## 8. Communication & Connectivity
Tầng tiếp xúc đầu tiên với Client, xử lý kết nối, giao thức truyền tin và phân phối request.

### 8.1 Connection Manager
*   `class NetworkListener`: Lắng nghe các Socket kết nối TCP/IP từ Client.
*   `interface IConnectionPoolManager`: Giao diện quản lý/pool kết nối.
*   `class ConnectionLimiter`: Đảm bảo từ chối các kết nối vượt ngưỡng tài nguyên hệ thống chịu tải.

### 8.2 Session Manager
*   `class SessionContext`: Lưu trữ thông tin trạng thái của phiên làm việc (User đăng nhập, Database đang chọn, Temp Tables).
*   `class SessionManager`: Quản lý vòng đời mở, đóng, kiểm tra timeout các session.

### 8.3 Protocol Handler
*   `class StreamPacketParser`: Phân tích lớp gói tin giao thức mạng (như bóc tách cấu trúc TDS).
*   `interface ISessionSerializer`: Giao diện đóng gói dữ liệu phản hồi theo format của driver (JDBC/ODBC).

### 8.4 Request Dispatcher
*   `class RequestDispatcher`: Nhận câu truy vấn đã parse thô từ Protocol, định tuyến gửi đến Parser/DDL Manager.
*   `class ThreadAssigner`: Cấp phát Worker Thread từ Threads Manager để xử lý request đó.

### 8.5 Response Manager
*   `class ResponseFormatter`: Định dạng kết quả (JSON, Binary Grid) trả về cho Driver của client.
*   `class NetworkBuffer`: Quản lý buffer Socket ghi dữ liệu phản hồi xuống card mạng.
