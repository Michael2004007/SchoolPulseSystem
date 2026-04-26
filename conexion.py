import os
import mysql.connector
from mysql.connector import Error


class Conexion:
    HOST = os.environ.get('MYSQL_HOST', 'localhost')
    DATABASE = os.environ.get('MYSQL_DATABASE', 'schoolpulsesystem')
    USER = os.environ.get('MYSQL_USER', 'root')
    PASSWORD = os.environ.get('MYSQL_PASSWORD', 'Oscar2025-')
    DB_PORT = int(os.environ.get('MYSQL_PORT', '3306'))
    POOL_SIZE = 5
    POOL_NAME = "school_pulse_pool"
    _pool = None

    @classmethod
    def obtener_pool(cls):
        if cls._pool is None:
            try:
                cls._pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name=cls.POOL_NAME,
                    pool_size=cls.POOL_SIZE,
                    host=cls.HOST,
                    port=cls.DB_PORT,
                    database=cls.DATABASE,
                    user=cls.USER,
                    password=cls.PASSWORD
                )
                print("✅ Pool de conexiones creado correctamente.")
            except Error as e:
                print(f"❌ Error al crear el pool: {e}")
        return cls._pool

    @classmethod
    def obtener_conexion(cls):
        return cls.obtener_pool().get_connection()

    @classmethod
    def liberar_conexion(cls, conexion):
        if conexion is not None:
            conexion.close()