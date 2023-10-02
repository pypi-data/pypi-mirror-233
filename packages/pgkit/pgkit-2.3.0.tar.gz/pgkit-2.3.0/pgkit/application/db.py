import os

from tinydb import TinyDB, Query, JSONStorage

from pgkit.application.settings import DB_PATH

DEFAULT_MAX_CONNECTIONS = 100
DEFAULT_MAX_WORKERS = 8


class LimitedPermissionJSONStorage(JSONStorage):

    def __init__(self, path: str, permission: int, **kwargs):
        super().__init__(path=path, **kwargs)
        os.chmod(path, permission)


class DBClass:
    DEFAULT_PERMISSION = 0o600

    def __init__(self, db_path):

        self.db = TinyDB(path=db_path,
                         create_dirs=True,
                         permission=self.DEFAULT_PERMISSION,
                         storage=LimitedPermissionJSONStorage)
        self.config_table = self.db.table('config')

        # Always check if the db file is secure
        assert os.stat(db_path).st_mode & 0o777 == self.DEFAULT_PERMISSION

    def add_config(self, name, version, host, port, dbname, slot, username, password, replica_port, use_separate_receivewal_service):
        self.config_table.insert({
            'name': name,
            'version': version,
            'host': host,
            'port': port,
            'dbname': dbname,
            'slot': slot,
            'username': username,
            'password': password,
            'replica_port': replica_port,
            'use_separate_receivewal_service': use_separate_receivewal_service,
            'max_connections': DEFAULT_MAX_CONNECTIONS,
            'max_worker_processes': DEFAULT_MAX_WORKERS,
        })

    def remove_config(self, name):
        self.config_table.remove(Query().name == name)

    def get_config(self, name):
        results = self.config_table.search(Query().name == name)
        if not results:
            raise ValueError(f'No config found by the name {name}')
        return self.config_table.search(Query().name == name)[0]

    def get_configs_list(self):
        return [item['name'] for item in self.config_table.all()]

    def update_config(self, name, fields):
        self.config_table.update(fields, Query().name == name)


DB = DBClass(DB_PATH)
