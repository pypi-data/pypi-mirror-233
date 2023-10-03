import pymysql
from dbutils.pooled_db import PooledDB

class MySQLConnector:
    _pool = None

    @classmethod
    def get_pool(cls, credential_provider):
        if not cls._pool:
            creds = credential_provider.get_credentials("mysql")
            cls._pool = PooledDB(
                creator=pymysql,
                host=creds['host'],
                user=creds['user'],
                password=creds['password'],
                database=creds['database'],
                autocommit=True,
                blocking=True,
                maxconnections=10
            )
        return cls._pool

    @classmethod
    def get_connection(cls, credential_provider):
        pool = cls.get_pool(credential_provider)
        return pool.connection()