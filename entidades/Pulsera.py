class Pulsera:
    def __init__(self, id=None, estado='disponible', fecha_creacion=None):
        self.id = id
        self.estado = estado
        self.fecha_creacion = fecha_creacion

    def __str__(self):
        return f"ID: {self.id} | Estado: {self.estado} | Fecha: {self.fecha_creacion}"