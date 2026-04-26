class Cobro:
    def __init__(self, id=None, pulsera_id=None, monto=None, fecha_cobro=None):
        self.id = id
        self.pulsera_id = pulsera_id
        self.monto = monto
        self.fecha_cobro = fecha_cobro

    def __str__(self):
        return f"ID: {self.id} | Pulsera: {self.pulsera_id} | Monto: {self.monto} | Fecha: {self.fecha_cobro}"