from conexion import Conexion


class ReporteDAO:
    REPORTE_PULSERAS = '''
        SELECT p.id, p.estado, a.nombre, a.apellido, a.curso
        FROM pulsera p
        LEFT JOIN reparto r ON p.id = r.pulsera_id
        LEFT JOIN alumno a ON r.alumno_id = a.id
        ORDER BY p.id
    '''

    REPORTE_DEUDORES = '''
        SELECT p.id, a.nombre, a.apellido, a.curso, a.id as alumno_id
        FROM pulsera p
        JOIN reparto r ON p.id = r.pulsera_id
        JOIN alumno a ON r.alumno_id = a.id
        WHERE p.estado = 'repartida'
        ORDER BY a.apellido
    '''

    REPORTE_PAGADOS = '''
        SELECT p.id, a.nombre, a.apellido, a.curso, c.monto, c.fecha_cobro
        FROM pulsera p
        JOIN reparto r ON p.id = r.pulsera_id
        JOIN alumno a ON r.alumno_id = a.id
        JOIN cobro c ON p.id = c.pulsera_id
        WHERE p.estado = 'pagada'
        ORDER BY c.fecha_cobro DESC
    '''

    @classmethod
    def reporte_pulseras(cls):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.REPORTE_PULSERAS)
            return cursor.fetchall()
        except Exception as e:
            print(f'Ocurrio un error al obtener reporte de pulseras: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def reporte_deudores(cls):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.REPORTE_DEUDORES)
            return cursor.fetchall()
        except Exception as e:
            print(f'Ocurrio un error al obtener reporte de deudores: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def reporte_pagados(cls):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.REPORTE_PAGADOS)
            return cursor.fetchall()
        except Exception as e:
            print(f'Ocurrio un error al obtener reporte de pagados: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    REPORTE_CURSOS = '''
        SELECT DISTINCT a.curso, COUNT(a.id) as total_alumnos,
               SUM(CASE WHEN p.estado = 'pagada' THEN 1 ELSE 0 END) as pagadas,
               SUM(CASE WHEN p.estado = 'repartida' THEN 1 ELSE 0 END) as pendientes
        FROM alumno a
        JOIN reparto r ON a.id = r.alumno_id
        JOIN pulsera p ON r.pulsera_id = p.id
        GROUP BY a.curso
        ORDER BY a.curso
    '''

    REPORTE_POR_CURSO = '''
        SELECT a.id, a.nombre, a.apellido, a.curso,
               GROUP_CONCAT(p.id ORDER BY p.id) as pulseras,
               SUM(CASE WHEN p.estado = 'pagada' THEN 1 ELSE 0 END) as pagadas,
               COUNT(p.id) as total
        FROM alumno a
        JOIN reparto r ON a.id = r.alumno_id
        JOIN pulsera p ON r.pulsera_id = p.id
        WHERE UPPER(TRIM(a.curso)) = UPPER(TRIM(%s))
        GROUP BY a.id, a.nombre, a.apellido, a.curso
        ORDER BY a.apellido
    '''

    @classmethod
    def reporte_cursos(cls):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.REPORTE_CURSOS)
            return cursor.fetchall()
        except Exception as e:
            print(f'Ocurrio un error al obtener reporte de cursos: {e}')
            return []
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def reporte_por_curso(cls, curso):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.REPORTE_POR_CURSO, (curso,))
            return cursor.fetchall()
        except Exception as e:
            print(f'Ocurrio un error al obtener reporte por curso: {e}')
            return []
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)