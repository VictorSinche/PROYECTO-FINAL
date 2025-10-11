# modelo/usuario.py

class Usuario:
    _auto_id = 1

    def __init__(self, nombres, apellidos, dni, email, telefono, estado="activo"):
        self._id = Usuario._auto_id
        Usuario._auto_id += 1
        self._nombres = nombres
        self._apellidos = apellidos
        self._dni = dni
        self._email = email
        self._telefono = telefono
        self._estado = estado

    # Getters
    def get_id(self): return self._id
    def get_nombres(self): return self._nombres
    def get_apellidos(self): return self._apellidos
    def get_dni(self): return self._dni
    def get_email(self): return self._email
    def get_telefono(self): return self._telefono
    def get_estado(self): return self._estado

    # Nuevo: nombre completo
    def get_nombre(self):
        return f"{self._nombres} {self._apellidos}"

    def tipo(self): 
        return "usuario"


class Estudiante(Usuario):
    def __init__(self, nombres, apellidos, dni, email, telefono, codigo, escuela):
        super().__init__(nombres, apellidos, dni, email, telefono)
        self._codigo = codigo
        self._escuela = escuela

    def get_codigo(self): return self._codigo
    def get_escuela(self): return self._escuela
    def tipo(self): return "estudiante"


class Profesor(Usuario):
    def __init__(self, nombres, apellidos, dni, email, telefono, categoria, departamento):
        super().__init__(nombres, apellidos, dni, email, telefono)
        self._categoria = categoria
        self._departamento = departamento

    def get_categoria(self): return self._categoria
    def get_departamento(self): return self._departamento
    def tipo(self): return "profesor"


class Bibliotecario(Usuario):
    def __init__(self, nombres, apellidos, dni, email, telefono, turno):
        super().__init__(nombres, apellidos, dni, email, telefono)
        self._turno = turno

    def get_turno(self): return self._turno
    def tipo(self): return "bibliotecario"
