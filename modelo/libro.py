# modelo/libro.py

class Libro:
    _auto_id = 1

    def __init__(self, isbn, titulo, autor, anio, editorial, categoria, stock_total):
        self._id = Libro._auto_id
        Libro._auto_id += 1
        self._isbn = isbn
        self._titulo = titulo
        self._autor = autor
        self._anio = anio
        self._editorial = editorial
        self._categoria = categoria
        self._stock_total = stock_total
        self._stock_disponible = stock_total

    # Getters
    def get_id(self): return self._id
    def get_isbn(self): return self._isbn
    def get_titulo(self): return self._titulo
    def get_autor(self): return self._autor
    def get_anio(self): return self._anio
    def get_editorial(self): return self._editorial
    def get_categoria(self): return self._categoria
    def get_stock_total(self): return self._stock_total
    def get_stock_disponible(self): return self._stock_disponible

    # Setters
    def set_isbn(self, v): self._isbn = v
    def set_titulo(self, v): self._titulo = v
    def set_autor(self, v): self._autor = v
    def set_anio(self, v): self._anio = v
    def set_editorial(self, v): self._editorial = v
    def set_categoria(self, v): self._categoria = v
    def set_stock_total(self, v): self._stock_total = v
    def set_stock_disponible(self, v): self._stock_disponible = v

    # Lógica de stock
    def hay_disponible(self):
        return self._stock_disponible > 0

    def reservar_uno(self):
        if self.hay_disponible():
            self._stock_disponible -= 1
            return True
        return False

    def devolver_uno(self):
        if self._stock_disponible < self._stock_total:
            self._stock_disponible += 1