from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect
from modelo.usuario import Estudiante, Profesor, Bibliotecario
from modelo.prestamo import Prestamo
from modelo.libro import Libro

app = Flask(__name__)
usuarios = []  # Lista en memoria para almacenar usuarios
libros = []
prestamos = []

# 👤 Estudiantes
usuarios.append(Estudiante("Lucas", "Sánchez", "12345678", "lucas@mail.com", "999111222", "202301234", "Ingeniería de Sistemas"))
usuarios.append(Estudiante("María", "Quispe", "23456789", "maria@mail.com", "988222333", "202302345", "Psicología"))
usuarios.append(Estudiante("José", "García", "34567890", "jose@mail.com", "977333444", "202303456", "Administración"))
usuarios.append(Estudiante("Luisa", "Torres", "45678901", "luisa@mail.com", "966444555", "202304567", "Contabilidad"))
usuarios.append(Estudiante("Andrés", "Paredes", "56789012", "andres@mail.com", "955555666", "202305678", "Derecho"))

# 👨‍🏫 Profesores
usuarios.append(Profesor("Diana", "Ramos", "23456789", "diana@mail.com", "988111333", "Titular", "Ciencias Computacionales"))
usuarios.append(Profesor("Carlos", "Vega", "87654321", "carlos@mail.com", "944111222", "Auxiliar", "Psicología"))
usuarios.append(Profesor("Elena", "Martínez", "76543210", "elena@mail.com", "933222333", "Asociado", "Economía"))
usuarios.append(Profesor("Juan", "Cruz", "65432109", "juan@mail.com", "922333444", "Titular", "Ingeniería Ambiental"))
usuarios.append(Profesor("Sandra", "Lopez", "54321098", "sandra@mail.com", "911444555", "Auxiliar", "Marketing"))

# 🧑‍💼 Bibliotecarios
usuarios.append(Bibliotecario("Ana", "Gómez", "34567890", "ana@mail.com", "977111444", "Mañana"))
usuarios.append(Bibliotecario("Pedro", "Salas", "45678901", "pedro@mail.com", "966222555", "Tarde"))
usuarios.append(Bibliotecario("Lucía", "Fernández", "56789012", "lucia@mail.com", "955333666", "Noche"))
usuarios.append(Bibliotecario("Jorge", "Ríos", "67890123", "jorge@mail.com", "944444777", "Mañana"))
usuarios.append(Bibliotecario("Natalia", "Aguilar", "78901234", "natalia@mail.com", "933555888", "Tarde"))

# 📚 Libros
libros.append(Libro("978-84-376-0494-7", "Cien Años de Soledad", "Gabriel García Márquez", 1967, "Sudamericana", "Novela", 5))
libros.append(Libro("978-84-670-5191-1", "Don Quijote de la Mancha", "Miguel de Cervantes", 1605, "Castalia", "Clásico", 3))
libros.append(Libro("978-84-204-8623-2", "El Principito", "Antoine de Saint-Exupéry", 1943, "Salamandra", "Fábula", 4))
libros.append(Libro("978-84-339-7883-3", "Rayuela", "Julio Cortázar", 1963, "Alfaguara", "Narrativa", 2))
libros.append(Libro("978-84-233-5126-4", "La Sombra del Viento", "Carlos Ruiz Zafón", 2001, "Planeta", "Misterio", 6))

p1 = Prestamo(usuarios[0], libros[0], fecha_prestamo=datetime.now() - timedelta(days=5), fecha_limite=datetime.now() - timedelta(days=1))
p1._fecha_devolucion = p1.get_fecha_limite()  # Devuelto justo a tiempo
p1._estado = "devuelto"

p2 = Prestamo(usuarios[1], libros[1], fecha_prestamo=datetime.now() - timedelta(days=4), fecha_limite=datetime.now())
p2._fecha_devolucion = p2.get_fecha_limite()  # Devuelto justo a tiempo
p2._estado = "devuelto"

# 🔴 Préstamos con mora
p3 = Prestamo(usuarios[2], libros[2], fecha_prestamo=datetime.now() - timedelta(days=10), fecha_limite=datetime.now() - timedelta(days=3))
p3._fecha_devolucion = datetime.now()  # Devuelto con retraso
p3._estado = "devuelto"
dias_mora3 = (p3._fecha_devolucion - p3._fecha_limite).days
p3._monto_mora = dias_mora3 * 5

p4 = Prestamo(usuarios[3], libros[3], fecha_prestamo=datetime.now() - timedelta(days=12), fecha_limite=datetime.now() - timedelta(days=5))
p4._fecha_devolucion = datetime.now()
p4._estado = "devuelto"
dias_mora4 = (p4._fecha_devolucion - p4._fecha_limite).days
p4._monto_mora = dias_mora4 * 5

# 🟡 Préstamos aún prestados
p5 = Prestamo(usuarios[4], libros[4], fecha_prestamo=datetime.now() - timedelta(days=2), fecha_limite=datetime.now() + timedelta(days=5))
# Sin devolución aún

p6 = Prestamo(usuarios[5], libros[0], fecha_prestamo=datetime.now() - timedelta(days=1), fecha_limite=datetime.now() + timedelta(days=6))
# Sin devolución aún

# Agregar a la lista
prestamos.extend([p1, p2, p3, p4, p5, p6])

# libros[0].reservar_uno()
# libros[0].reservar_uno()
# libros[1].reservar_uno()
# libros[2].reservar_uno()
libros[3].reservar_uno()
libros[4].reservar_uno()

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/registrar-usuario", methods=["GET", "POST"])
def registrar_usuario():
    if request.method == "POST":
        data = request.form
        tipo = data.get("tipo")

        if tipo == "estudiante":
            usuario = Estudiante(
                data["nombres"], data["apellidos"], data["dni"],
                data["email"], data["telefono"], data["codigo"], data["escuela"]
            )
        elif tipo == "profesor":
            usuario = Profesor(
                data["nombres"], data["apellidos"], data["dni"],
                data["email"], data["telefono"], data["categoria"], data["departamento"]
            )
        elif tipo == "bibliotecario":
            usuario = Bibliotecario(
                data["nombres"], data["apellidos"], data["dni"],
                data["email"], data["telefono"], data["turno"]
            )
        else:
            return render_template("registrar_usuario.html", mensaje="❌ Tipo de usuario inválido")

        usuarios.append(usuario)
        return render_template("registrar_usuario.html", mensaje="✅ Usuario registrado correctamente")

    return render_template("registrar_usuario.html")

@app.route("/listar-usuarios")
def listar_usuarios():
    return render_template("listar_usuarios.html", usuarios=usuarios)

@app.route("/registrar-libro", methods=["GET", "POST"])
def registrar_libro():
    if request.method == "POST":
        data = request.form
        libro = Libro(
            data["isbn"], data["titulo"], data["autor"],
            int(data["anio"]), data["editorial"],
            data["categoria"], int(data["stock_total"])
        )
        libros.append(libro)
        return render_template("registrar_libro.html", mensaje="✅ Libro registrado correctamente")
    return render_template("registrar_libro.html")

@app.route("/listar-libros")
def listar_libros():
    return render_template("listar_libros.html", libros=libros)

@app.route("/registrar-prestamo", methods=["GET", "POST"])
def registrar_prestamo():
    if request.method == "POST":
        usuario_idx = int(request.form["usuario_id"])
        libro_idx = int(request.form["libro_id"])
        fecha_limite_str = request.form["fecha_limite"]

        usuario = usuarios[usuario_idx]
        libro = libros[libro_idx]

        if libro.get_stock_disponible() > 0:
            libro.reservar_uno()
            fecha_limite = datetime.strptime(fecha_limite_str, "%Y-%m-%d")

            nuevo = Prestamo(usuario, libro, fecha_prestamo=datetime.now(), fecha_limite=fecha_limite)
            prestamos.append(nuevo)

            return render_template("registrar_prestamo.html", usuarios=usuarios, libros=libros,
                                   mensaje="✅ Préstamo registrado exitosamente",
                                   hoy=datetime.today().strftime("%Y-%m-%d"))
        else:
            return render_template("registrar_prestamo.html", usuarios=usuarios, libros=libros,
                                   mensaje="❌ No hay stock disponible",
                                   hoy=datetime.today().strftime("%Y-%m-%d"))

    return render_template("registrar_prestamo.html", usuarios=usuarios, libros=libros,
                           hoy=datetime.today().strftime("%Y-%m-%d"))

@app.route("/listar-prestamos")
def listar_prestamos():
    return render_template("listar_prestamos.html", prestamos=prestamos)

@app.route("/devolver/<int:id>")
def devolver(id):
    prestamo = next((p for p in prestamos if p.get_id() == id), None)
    if prestamo and prestamo.get_estado() == "prestado":
        prestamo.marcar_devuelto()
    return redirect("/listar-prestamos")

@app.route("/morosos")
def ver_morosos():
    morosos = [p for p in prestamos if p.get_monto_mora() > 0]
    return render_template("morosos.html", morosos=morosos)

if __name__ == '__main__':
    app.run(debug=True)