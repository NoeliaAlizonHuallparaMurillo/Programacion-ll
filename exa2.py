class Persona:
    def __init__(self, nombre, edad, peso):
        self.nombre = nombre
        self.edad = edad
        self.peso = peso


class Cabina:
    def __init__(self, nroCabina):
        self.nroCabina = nroCabina
        self.personasAbordo = []

    def agregarPersona(self, persona):
        # Máximo 10 personas
        if len(self.personasAbordo) >= 10:
            print(f"Cabina {self.nroCabina}: Ya hay 10 personas.")
            return False

        # Peso máximo 650kg
        peso_actual = sum(p.peso for p in self.personasAbordo)
        if peso_actual + persona.peso > 650:
            print(f"Cabina {self.nroCabina}: Exceso de peso (máx 650 kg).")
            return False

        self.personasAbordo.append(persona)
        print(f"{persona.nombre} agregado(a) a la cabina {self.nroCabina}.")
        return True


class Linea:
    def __init__(self, color, nroEstaciones):
        self.color = color
        self.nroEstaciones = nroEstaciones
        self.cabinas = []

    def agregarCabina(self, cabina):
        self.cabinas.append(cabina)


class MiTeleferico:
    def __init__(self):
        self.lineas = []
        self.cantidadIngresos = 0

    def agregarLinea(self, linea):
        self.lineas.append(linea)

    def agregarCabina(self, colorLinea, cabina):
        for l in self.lineas:
            if l.color == colorLinea:
                l.agregarCabina(cabina)
                return True
        print("Línea no encontrada.")
        return False

    def agregarPersona(self, colorLinea, nroCabina, persona):
        for l in self.lineas:
            if l.color == colorLinea:
                for c in l.cabinas:
                    if c.nroCabina == nroCabina:
                        if c.agregarPersona(persona):
                            ingreso = self.calcularTarifa(persona)
                            self.cantidadIngresos += ingreso
                            return True
                        return False
        print("No existe esa línea o cabina.")
        return False

    def calcularTarifa(self, persona):
        if persona.edad < 2:
            return 0
        elif 2 <= persona.edad <= 25:
            return 3
        elif 25 < persona.edad <= 60:
            return 1.5
        else:
            return 3

    def ingresosPorLinea(self):
        resultados = {}
        for l in self.lineas:
            total = 0
            for c in l.cabinas:
                for p in c.personasAbordo:
                    total += self.calcularTarifa(p)
            resultados[l.color] = total
        return resultados

    def lineaMayorIngreso(self):
        ingresos = self.ingresosPorLinea()
        if not ingresos:
            return None
        return max(ingresos, key=ingresos.get)


if __name__ == "__main__":
    sistema = MiTeleferico()

    # Crear líneas
    lineaRoja = Linea("Rojo", 8)
    lineaAmarilla = Linea("Amarillo", 6)

    sistema.agregarLinea(lineaRoja)
    sistema.agregarLinea(lineaAmarilla)

    # Agregar cabinas
    sistema.agregarCabina("Rojo", Cabina(1))
    sistema.agregarCabina("Rojo", Cabina(2))
    sistema.agregarCabina("Amarillo", Cabina(1))

    # Crear personas
    p1 = Persona("Noelia", 24, 67)
    p2 = Persona("Jose", 45, 70)
    p3 = Persona("Elizabeth", 1, 12)
    p4 = Persona("Anahi", 65, 68)

    # Agregar personas a cabinas
    sistema.agregarPersona("Rojo", 1, p1)
    sistema.agregarPersona("Rojo", 1, p2)
    sistema.agregarPersona("Rojo", 2, p3)
    sistema.agregarPersona("Amarillo", 1, p4)

    # Mostrar ingresos
    print("\nIngresos por línea:")
    for linea, ingreso in sistema.ingresosPorLinea().items():
        print(f" - Línea {linea}: {ingreso} Bs")

    print(f"\nLínea con mayor ingreso: {sistema.lineaMayorIngreso()}")