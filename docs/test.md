classDiagram
    direction TB

    DBMS *-- ClientInterface
    DBMS *-- QueryProcessing
    DBMS *-- DatabaseManagement
    DBMS *-- StorageEngine
    DBMS *-- TransactionConcurrency
    DBMS *-- SecurityManagement
    DBMS *-- Administration
    DBMS *-- BackupRecoveryLogging
    DBMS *-- PerformanceManagement
    DBMS *-- CommunicationConnectivity

    ClientInterface --> QueryProcessing
    QueryProcessing --> DatabaseManagement
    QueryProcessing --> StorageEngine
    QueryProcessing --> TransactionConcurrency
    QueryProcessing --> SecurityManagement

    DatabaseManagement --> SystemCatalog
    DatabaseManagement --> StorageEngine

    TransactionConcurrency --> StorageEngine
    TransactionConcurrency --> BackupRecoveryLogging

    BackupRecoveryLogging --> StorageEngine

    PerformanceManagement --> QueryProcessing
    PerformanceManagement --> StorageEngine
    PerformanceManagement --> TransactionConcurrency

    Administration --> SecurityManagement
    Administration --> BackupRecoveryLogging
    Administration --> PerformanceManagement
