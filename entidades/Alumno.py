class Alumno:
    def __init__(self, id=None, nombre=None, apellido=None, curso=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.curso = curso

    def __str__(self):
        return f"ID: {self.id} | Nombre: {self.nombre} {self.apellido} | Curso: {self.curso}"