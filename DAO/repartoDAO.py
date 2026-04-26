from conexion import Conexion
from entidades.Reparto import Reparto


class RepartoDAO:
    SELECCIONAR = '''SELECT r.id, r.alumno_id, r.pulsera_id, r.fecha_reparto,
                     a.nombre, a.apellido, a.curso
                     FROM reparto r
                     JOIN alumno a ON r.alumno_id = a.id
                     ORDER BY r.id'''
    INSERTAR = 'INSERT INTO reparto(alumno_id, pulsera_id) VALUES(%s, %s)'
    SELECCIONAR_POR_ALUMNO = '''SELECT r.id, r.alumno_id, r.pulsera_id, r.fecha_reparto,
                                a.nombre, a.apellido, a.curso
                                FROM reparto r
                                JOIN alumno a ON r.alumno_id = a.id
                                WHERE r.alumno_id=%s'''

    @classmethod
    def seleccionar(cls):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.SELECCIONAR)
            registros = cursor.fetchall()
            repartos = []
            for registro in registros:
                reparto = Reparto(registro[0], registro[1], registro[2], registro[3])
                repartos.append(reparto)
            return repartos
        except Exception as e:
            print(f'Ocurrio un error al seleccionar repartos: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def insertar(cls, reparto):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (reparto.alumno_id, reparto.pulsera_id)
            cursor.execute(cls.INSERTAR, valores)
            conexion.commit()
            return cursor.rowcount
        except Exception as e:
            print(f'Ocurrio un error al insertar el reparto: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def seleccionar_por_alumno(cls, alumno_id):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (alumno_id,)
            cursor.execute(cls.SELECCIONAR_POR_ALUMNO, valores)
            registros = cursor.fetchall()
            repartos = []
            for registro in registros:
                reparto = Reparto(registro[0], registro[1], registro[2], registro[3])
                repartos.append(reparto)
            return repartos
        except Exception as e:
            print(f'Ocurrio un error al seleccionar repartos por alumno: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    SELECCIONAR_AGRUPADO = '''
        SELECT a.id, a.nombre, a.apellido, a.curso,
               r.pulsera_id, r.fecha_reparto
        FROM alumno a
        JOIN reparto r ON a.id = r.alumno_id
        ORDER BY a.apellido, a.nombre, r.pulsera_id
    '''

    @classmethod
    def seleccionar_agrupado(cls):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.SELECCIONAR_AGRUPADO)
            registros = cursor.fetchall()

            agrupado = {}
            for registro in registros:
                alumno_id = registro[0]
                if alumno_id not in agrupado:
                    r = Reparto()
                    r.alumno_id = registro[0]
                    r.nombre = registro[1]
                    r.apellido = registro[2]
                    r.curso = registro[3]
                    r.pulseras = []
                    r.fecha_reparto = registro[5]
                    agrupado[alumno_id] = r
                agrupado[alumno_id].pulseras.append(registro[4])

            return list(agrupado.values())
        except Exception as e:
            print(f'Ocurrio un error al seleccionar repartos agrupados: {e}')
            return []
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    ELIMINAR_POR_ALUMNO = 'DELETE FROM reparto WHERE alumno_id = %s'
    ELIMINAR_ALUMNO = 'DELETE FROM alumno WHERE id = %s'

    @classmethod
    def eliminar_asignacion(cls, alumno_id):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            # Primero obtenemos las pulseras asignadas para liberarlas
            cursor.execute('SELECT pulsera_id FROM reparto WHERE alumno_id = %s', (alumno_id,))
            pulseras = [row[0] for row in cursor.fetchall()]
            # Eliminamos el reparto
            cursor.execute(cls.ELIMINAR_POR_ALUMNO, (alumno_id,))
            # Eliminamos el alumno
            cursor.execute(cls.ELIMINAR_ALUMNO, (alumno_id,))
            conexion.commit()
            return pulseras
        except Exception as e:
            print(f'Ocurrio un error al eliminar asignacion: {e}')
            return None
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    SELECCIONAR_POR_PULSERA = '''
        SELECT id, alumno_id, pulsera_id, fecha_reparto
        FROM reparto WHERE pulsera_id = %s
    '''

    @classmethod
    def seleccionar_por_pulsera(cls, pulsera_id):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.SELECCIONAR_POR_PULSERA, (pulsera_id,))
            registro = cursor.fetchone()
            if registro:
                return Reparto(registro[0], registro[1], registro[2], registro[3])
            return None
        except Exception as e:
            print(f'Ocurrio un error al seleccionar reparto por pulsera: {e}')
            return None
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)