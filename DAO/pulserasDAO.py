from conexion import Conexion
from entidades.Pulsera import Pulsera


class PulseraDAO:
    SELECCIONAR = 'SELECT * FROM pulsera ORDER BY id'
    INSERTAR = 'INSERT INTO pulsera(id, estado) VALUES(%s, %s)'
    ACTUALIZAR = 'UPDATE pulsera SET estado=%s WHERE id=%s'
    ELIMINAR = 'DELETE FROM pulsera WHERE id=%s'
    SELECCIONAR_POR_ID = 'SELECT * FROM pulsera WHERE id=%s'

    @classmethod
    def seleccionar(cls):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.SELECCIONAR)
            registros = cursor.fetchall()
            pulseras = []
            for registro in registros:
                pulsera = Pulsera(registro[0], registro[1], registro[2])
                pulseras.append(pulsera)
            return pulseras
        except Exception as e:
            print(f'Ocurrio un error al seleccionar pulseras: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def seleccionar_por_id(cls, pulsera):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (pulsera.id,)
            cursor.execute(cls.SELECCIONAR_POR_ID, valores)
            registro = cursor.fetchone()
            if registro:
                return Pulsera(registro[0], registro[1], registro[2])
            return None
        except Exception as e:
            print(f'Ocurrio un error al seleccionar la pulsera: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def insertar(cls, pulsera):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (pulsera.id, pulsera.estado)
            cursor.execute(cls.INSERTAR, valores)
            conexion.commit()
            return cursor.rowcount
        except Exception as e:
            return None
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def actualizar(cls, pulsera):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (pulsera.estado, pulsera.id)
            cursor.execute(cls.ACTUALIZAR, valores)
            conexion.commit()
            return cursor.rowcount
        except Exception as e:
            print(f'Ocurrio un error al actualizar la pulsera: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def eliminar(cls, pulsera):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (pulsera.id,)
            cursor.execute(cls.ELIMINAR, valores)
            conexion.commit()
            return cursor.rowcount
        except Exception as e:
            print(f'Ocurrio un error al eliminar la pulsera: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    SELECCIONAR_MAXIMO = 'SELECT MAX(id) FROM pulsera'

    @classmethod
    def obtener_maximo_id(cls):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.SELECCIONAR_MAXIMO)
            registro = cursor.fetchone()
            return registro[0] if registro[0] else 0
        except Exception as e:
            print(f'Ocurrio un error al obtener maximo id: {e}')
            return 0
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    SELECCIONAR_PROXIMA = "SELECT MIN(id) FROM pulsera WHERE estado = 'disponible'"

    @classmethod
    def obtener_proxima_disponible(cls):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.SELECCIONAR_PROXIMA)
            registro = cursor.fetchone()
            return registro[0] if registro[0] else None
        except Exception as e:
            print(f'Ocurrio un error al obtener proxima disponible: {e}')
            return None
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)