from flask_login import UserMixin

class Usuario(UserMixin):
    def __init__(self, id, username, password, rol, nombre=None):
        self.id = id
        self.username = username
        self.password = password
        self.rol = rol
        self.nombre = nombre

    def __str__(self):
        return f"ID: {self.id} | Username: {self.username} | Rol: {self.rol}"