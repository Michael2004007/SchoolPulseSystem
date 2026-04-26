class Reparto:
    def __init__(self, id=None, alumno_id=None, pulsera_id=None, fecha_reparto=None):
        self.id = id
        self.alumno_id = alumno_id
        self.pulsera_id = pulsera_id
        self.fecha_reparto = fecha_reparto

    def __str__(self):
        return f"ID: {self.id} | Alumno: {self.alumno_id} | Pulsera: {self.pulsera_id} | Fecha: {self.fecha_reparto}"