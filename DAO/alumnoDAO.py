from conexion import Conexion
from entidades.Alumno import Alumno


class AlumnoDAO:
    SELECCIONAR = 'SELECT * FROM alumno ORDER BY apellido'
    INSERTAR = 'INSERT INTO alumno(nombre, apellido, curso) VALUES(%s, %s, %s)'
    ACTUALIZAR = 'UPDATE alumno SET nombre=%s, apellido=%s, curso=%s WHERE id=%s'
    ELIMINAR = 'DELETE FROM alumno WHERE id=%s'
    SELECCIONAR_POR_ID = 'SELECT * FROM alumno WHERE id=%s'
    BUSCAR_POR_NOMBRE = 'SELECT * FROM alumno WHERE nombre LIKE %s OR apellido LIKE %s ORDER BY apellido'
    BUSCAR_POR_CURSO = 'SELECT * FROM alumno WHERE UPPER(TRIM(curso)) LIKE UPPER(%s) ORDER BY apellido'

    @classmethod
    def seleccionar(cls):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.SELECCIONAR)
            registros = cursor.fetchall()
            alumnos = []
            for registro in registros:
                alumno = Alumno(registro[0], registro[1], registro[2], registro[3])
                alumnos.append(alumno)
            return alumnos
        except Exception as e:
            print(f'Ocurrio un error al seleccionar alumnos: {e}')
            return []
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def seleccionar_por_id(cls, alumno_id):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.SELECCIONAR_POR_ID, (alumno_id,))
            registro = cursor.fetchone()
            if registro:
                return Alumno(registro[0], registro[1], registro[2], registro[3])
            return None
        except Exception as e:
            print(f'Ocurrio un error al seleccionar el alumno: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def buscar_por_nombre(cls, texto):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (f'%{texto}%', f'%{texto}%')
            cursor.execute(cls.BUSCAR_POR_NOMBRE, valores)
            registros = cursor.fetchall()
            alumnos = []
            for registro in registros:
                alumno = Alumno(registro[0], registro[1], registro[2], registro[3])
                alumnos.append(alumno)
            return alumnos
        except Exception as e:
            print(f'Ocurrio un error al buscar alumnos por nombre: {e}')
            return []
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def buscar_por_curso(cls, curso):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.BUSCAR_POR_CURSO, (f'%{curso}%',))
            registros = cursor.fetchall()
            alumnos = []
            for registro in registros:
                alumno = Alumno(registro[0], registro[1], registro[2], registro[3])
                alumnos.append(alumno)
            return alumnos
        except Exception as e:
            print(f'Ocurrio un error al buscar alumnos por curso: {e}')
            return []
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def insertar(cls, alumno):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (alumno.nombre, alumno.apellido, alumno.curso)
            cursor.execute(cls.INSERTAR, valores)
            conexion.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f'Ocurrio un error al insertar el alumno: {e}')
            return None
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def actualizar(cls, alumno):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (alumno.nombre, alumno.apellido, alumno.curso, alumno.id)
            cursor.execute(cls.ACTUALIZAR, valores)
            conexion.commit()
            return cursor.rowcount
        except Exception as e:
            print(f'Ocurrio un error al actualizar el alumno: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def eliminar(cls, alumno):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (alumno.id,)
            cursor.execute(cls.ELIMINAR, valores)
            conexion.commit()
            return cursor.rowcount
        except Exception as e:
            print(f'Ocurrio un error al eliminar el alumno: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)