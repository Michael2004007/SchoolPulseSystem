from conexion import Conexion
from entidades.Cobro import Cobro


class CobroDAO:
    SELECCIONAR = 'SELECT * FROM cobro ORDER BY fecha_cobro DESC'
    INSERTAR = 'INSERT INTO cobro(pulsera_id, monto) VALUES(%s, %s)'
    SELECCIONAR_POR_PULSERA = 'SELECT * FROM cobro WHERE pulsera_id=%s'

    @classmethod
    def seleccionar(cls):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.SELECCIONAR)
            registros = cursor.fetchall()
            cobros = []
            for registro in registros:
                cobro = Cobro(registro[0], registro[1], registro[2], registro[3])
                cobros.append(cobro)
            return cobros
        except Exception as e:
            print(f'Ocurrio un error al seleccionar cobros: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def insertar(cls, cobro):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (cobro.pulsera_id, cobro.monto)
            cursor.execute(cls.INSERTAR, valores)
            conexion.commit()
            return cursor.rowcount
        except Exception as e:
            print(f'Ocurrio un error al insertar el cobro: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def seleccionar_por_pulsera(cls, pulsera_id):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (pulsera_id,)
            cursor.execute(cls.SELECCIONAR_POR_PULSERA, valores)
            registro = cursor.fetchone()
            if registro:
                return Cobro(registro[0], registro[1], registro[2], registro[3])
            return None
        except Exception as e:
            print(f'Ocurrio un error al seleccionar el cobro por pulsera: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    SELECCIONAR_PULSERAS_POR_ALUMNO = '''
        SELECT p.id as pulsera_id, p.estado, c.fecha_cobro
        FROM reparto r
        JOIN pulsera p ON r.pulsera_id = p.id
        LEFT JOIN cobro c ON p.id = c.pulsera_id
        WHERE r.alumno_id = %s
        ORDER BY p.id
    '''

    @classmethod
    def seleccionar_pulseras_por_alumno(cls, alumno_id):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.SELECCIONAR_PULSERAS_POR_ALUMNO, (alumno_id,))
            registros = cursor.fetchall()
            resultado = []
            for registro in registros:
                cobro = Cobro()
                cobro.pulsera_id = registro[0]
                cobro.estado = registro[1]
                cobro.fecha_cobro = registro[2]
                resultado.append(cobro)
            return resultado
        except Exception as e:
            print(f'Ocurrio un error al seleccionar pulseras por alumno: {e}')
            return []
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    ELIMINAR_COBRO = 'DELETE FROM cobro WHERE pulsera_id = %s'

    @classmethod
    def eliminar_cobro(cls, pulsera_id):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.ELIMINAR_COBRO, (pulsera_id,))
            conexion.commit()
            return cursor.rowcount
        except Exception as e:
            print(f'Ocurrio un error al eliminar cobro: {e}')
            return None
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)