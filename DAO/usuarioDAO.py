from conexion import Conexion
from entidades.Usuarios import Usuario


class UsuarioDAO:
    SELECCIONAR = 'SELECT * FROM usuario ORDER BY nombre'
    BUSCAR_POR_USERNAME = 'SELECT * FROM usuario WHERE username = %s'
    INSERTAR = 'INSERT INTO usuario(username, password, rol, nombre) VALUES(%s, %s, %s, %s)'
    ACTUALIZAR = 'UPDATE usuario SET username=%s, password=%s, rol=%s, nombre=%s WHERE id=%s'
    ELIMINAR = 'DELETE FROM usuario WHERE id=%s'

    @classmethod
    def seleccionar(cls):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.SELECCIONAR)
            registros = cursor.fetchall()
            usuarios = []
            for r in registros:
                usuario = Usuario(r[0], r[1], r[2], r[3], r[4] if len(r) > 4 else None)
                usuarios.append(usuario)
            return usuarios
        except Exception as e:
            print(f'Ocurrio un error al seleccionar usuarios: {e}')
            return []
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def buscar_por_username(cls, username):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.BUSCAR_POR_USERNAME, (username,))
            r = cursor.fetchone()
            if r:
                return Usuario(r[0], r[1], r[2], r[3], r[4] if len(r) > 4 else None)
            return None
        except Exception as e:
            print(f'Ocurrio un error al buscar usuario: {e}')
            return None
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def insertar(cls, usuario):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (usuario.username, usuario.password, usuario.rol, usuario.nombre)
            cursor.execute(cls.INSERTAR, valores)
            conexion.commit()
            return cursor.rowcount
        except Exception as e:
            print(f'Ocurrio un error al insertar usuario: {e}')
            return None
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def actualizar(cls, usuario):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (usuario.username, usuario.password, usuario.rol, usuario.nombre, usuario.id)
            cursor.execute(cls.ACTUALIZAR, valores)
            conexion.commit()
            return cursor.rowcount
        except Exception as e:
            print(f'Ocurrio un error al actualizar usuario: {e}')
            return None
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def eliminar(cls, usuario_id):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls.ELIMINAR, (usuario_id,))
            conexion.commit()
            return cursor.rowcount
        except Exception as e:
            print(f'Ocurrio un error al eliminar usuario: {e}')
            return None
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)