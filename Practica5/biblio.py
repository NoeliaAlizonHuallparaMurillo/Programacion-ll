
# SISTEMA DE BIBLIOTECA UNIVERSITARIA - UMSA


from datetime import date


# Clase Autor (agregación)

class Autor:
    def __init__(self, nombre, nacionalidad):
        self.nombre = nombre
        self.nacionalidad = nacionalidad

    def mostrarInfo(self):
        print(f"Autor: {self.nombre}, Nacionalidad: {self.nacionalidad}")



# Clase Estudiante (asociación)

class Estudiante:
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre

    def mostrarInfo(self):
        print(f"Estudiante: {self.nombre}, Código: {self.codigo}")



# Clase Libro (composición con Pagina)

class Libro:
    class Pagina:
        def __init__(self, numero, contenido):
            self.numero = numero
            self.contenido = contenido

        def mostrarPagina(self):
            print(f"Página {self.numero}: {self.contenido}")

    def __init__(self, titulo, isbn, contenidos_paginas):
        self.titulo = titulo
        self.isbn = isbn
        # COMPOSICIÓN: el libro crea sus propias páginas
        self.paginas = [self.Pagina(i + 1, contenido) for i, contenido in enumerate(contenidos_paginas)]

    def leer(self):
        print(f"\n--- Leyendo el libro '{self.titulo}' ---")
        for pagina in self.paginas:
            pagina.mostrarPagina()



# Clase Prestamo (asociación)

class Prestamo:
    def __init__(self, estudiante, libro):
        self.fecha_prestamo = date.today()
        self.fecha_devolucion = None
        self.estudiante = estudiante
        self.libro = libro

    def mostrarInfo(self):
        print(f"Préstamo: Libro '{self.libro.titulo}' a {self.estudiante.nombre} el {self.fecha_prestamo}")



# Clase Biblioteca (agregación y composición)

class Biblioteca:
    class Horario:
        def __init__(self, dias_apertura, hora_apertura, hora_cierre):
            self.dias_apertura = dias_apertura
            self.hora_apertura = hora_apertura
            self.hora_cierre = hora_cierre

        def mostrarHorario(self):
            print(f"Horario: {self.dias_apertura}, {self.hora_apertura} - {self.hora_cierre}")

    def __init__(self, nombre, dias, hora_ini, hora_fin):
        self.nombre = nombre
        self.libros = []
        self.autores = []
        self.prestamos = []
        # COMPOSICIÓN: el horario solo existe con la biblioteca
        self.horario = self.Horario(dias, hora_ini, hora_fin)

    def agregarLibro(self, libro):
        self.libros.append(libro)

    def agregarAutor(self, autor):
        self.autores.append(autor)

    def prestarLibro(self, estudiante, libro):
        prestamo = Prestamo(estudiante, libro)
        self.prestamos.append(prestamo)
        return prestamo

    def mostrarEstado(self):
        print(f"\n----- Estado de la Biblioteca '{self.nombre}' -----")
        if self.horario:
            self.horario.mostrarHorario()

        print("\nAutores registrados:")
        for autor in self.autores:
            autor.mostrarInfo()

        print("\nLibros disponibles:")
        for libro in self.libros:
            print(f"- {libro.titulo} (ISBN: {libro.isbn})")

        print("\nPréstamos activos:")
        for prestamo in self.prestamos:
            prestamo.mostrarInfo()

    def cerrarBiblioteca(self):
        print(f"\nLa biblioteca '{self.nombre}' ha cerrado. Todos los préstamos se eliminan.")
        self.prestamos.clear()
        self.horario = None


#Ejecuciom
if __name__ == "__main__":
    # Crear Biblioteca (tiene horario por composición)
    biblioteca = Biblioteca("Biblioteca Central UMSA", "Lunes a Viernes", "08:00", "18:00")

    # Crear autores (agregación)
    autor1 = Autor("Gabriel García Márquez", "Colombiano")
    autor2 = Autor("Julio Cortázar", "Argentino")

    # Registrar autores en la biblioteca
    biblioteca.agregarAutor(autor1)
    biblioteca.agregarAutor(autor2)

    # Crear libros (agregación) con sus páginas (composición)
    libro1 = Libro("Cien Años de Soledad", "ISBN001", ["Capítulo 1: Macondo", "Capítulo 2: La familia Buendía"])
    libro2 = Libro("Rayuela", "ISBN002", ["Tablero de dirección", "El lado de allá", "El lado de acá"])

    biblioteca.agregarLibro(libro1)
    biblioteca.agregarLibro(libro2)
    #(asociación)
    # Crear estudiante 
    estudiante = Estudiante("10016611", "Noelia Huallpara")

    # Crear préstamo 
    prestamo = biblioteca.prestarLibro(estudiante, libro1)

    # Mostrar estado 
    biblioteca.mostrarEstado()

    # Leer 
    libro1.leer()

    # Cerrar biblioteca aqui termina la composición con h y p, se restablece
    biblioteca.cerrarBiblioteca()

    # Mostrar de nuevo el estado de la biblio
    biblioteca.mostrarEstado()
