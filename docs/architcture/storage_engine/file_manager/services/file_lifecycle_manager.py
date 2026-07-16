class FileLifecycleManager:
    def __init__(self, open_file_mgr, reader, writer, synchronizer):
        self._open_file_mgr = open_file_mgr
        self._reader = reader
        self._writer = writer
        self._synchronizer = synchronizer

    def create_file(self, path: str, file_type):
        """
        Operation 1: Create a new physical data file.
        """
        try:
            self._synchronizer.allocate_on_disk(path)
        except Exception as e:
            if "FileAlreadyExists" in str(e):
                raise Exception("FileAlreadyExists")
            raise e
            
        from storage_engine.file_manager.entities.data_file import DataFile
        
        # Sinh trạng thái CREATING -> OPEN như Sequence Diagram
        new_data_file = DataFile(file_id=0, path=path, file_type=file_type)
        
        from storage_engine.file_manager.enums.file_access_mode import FileAccessMode
        from storage_engine.file_manager.enums.file_lock_mode import FileLockMode
        
        file_handle = self._open_file_mgr.register(
            file=new_data_file, 
            mode=FileAccessMode.READ_WRITE, 
            lock=FileLockMode.EXCLUSIVE
        )
        
        return file_handle

    def delete_file(self, path: str) -> bool:
        if self._open_file_mgr.is_already_open(path):
            raise Exception("FileInUseException")
        
        self._synchronizer.delete_from_disk(path)
        return True
