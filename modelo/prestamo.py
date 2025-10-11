from datetime import datetime, timedelta

class Prestamo:
    _auto_id = 1

    def __init__(self, usuario, libro, fecha_prestamo=None, fecha_limite=None, dias_plazo=7):
        self._id = Prestamo._auto_id
        Prestamo._auto_id += 1
        self._usuario = usuario
        self._libro = libro
        self._fecha_prestamo = fecha_prestamo or datetime.now()
        # ✅ Si el usuario no define fecha límite, se calcula automáticamente (+7 días)
        self._fecha_limite = fecha_limite or (self._fecha_prestamo + timedelta(days=dias_plazo))
        self._fecha_devolucion = None
        self._estado = "prestado"
        self._monto_mora = 0

    # --- Getters ---
    def get_id(self): return self._id
    def get_usuario(self): return self._usuario
    def get_libro(self): return self._libro
    def get_fecha_prestamo(self): return self._fecha_prestamo
    def get_fecha_limite(self): return self._fecha_limite
    def get_fecha_devolucion(self): return self._fecha_devolucion
    def get_estado(self): return self._estado
    def get_monto_mora(self): return self._monto_mora

    # --- Devolución ---
    def marcar_devuelto(self):
        self._fecha_devolucion = datetime.now()
        self._estado = "devuelto"
        self._libro.devolver_uno()

        # ✅ Calcular mora si se pasó la fecha límite
        if self._fecha_devolucion > self._fecha_limite:
            dias_mora = (self._fecha_devolucion - self._fecha_limite).days
            self._monto_mora = dias_mora * 5  # 💰 Ejemplo: S/5 por día de atraso
