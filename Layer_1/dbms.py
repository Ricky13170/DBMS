class StorageEngine:
    pass


class QueryProcessing:
    pass


class TransactionConcurrency:
    pass


class Security:
    pass


class DatabaseObjectMetadata:
    pass


class Administration:
    pass


class BackupRecoveryLogging:
    pass


class CommunicationConnectivity:
    pass


class DBMS:
    """Core System chứa (Composition) 8 Sub-systems gốc"""
    def __init__(self):
        self.storage_engine = StorageEngine()
        self.query_processing = QueryProcessing()
        self.transaction_concurrency = TransactionConcurrency()
        self.security = Security()
        self.database_metadata = DatabaseObjectMetadata()
        self.administration = Administration()
        self.backup_recovery = BackupRecoveryLogging()
        self.communication = CommunicationConnectivity()
