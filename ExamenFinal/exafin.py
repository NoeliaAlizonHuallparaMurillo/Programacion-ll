import json
import os

class Consulta:
    def __init__(self, id_consulta, nombre_paciente, apellido_paciente, dia, mes, ano):
        self.id = id_consulta
        self.nombre_paciente = nombre_paciente
        self.apellido_paciente = apellido_paciente
        self.dia = dia
        self.mes = mes
        self.ano = ano
    
    def __str__(self):
        return f"Consulta {self.id}: {self.nombre_paciente} {self.apellido_paciente} - {self.dia}/{self.mes}/{self.ano}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre_paciente': self.nombre_paciente,
            'apellido_paciente': self.apellido_paciente,
            'dia': self.dia,
            'mes': self.mes,
            'ano': self.ano
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data['id'],
            data['nombre_paciente'],
            data['apellido_paciente'],
            data['dia'],
            data['mes'],
            data['ano']
        )

class Medico:
    def __init__(self, nombre, apellido, especialidad, anios_experiencia):
        self.nombre = nombre
        self.apellido = apellido
        self.especialidad = especialidad
        self.anios_experiencia = anios_experiencia
        self.consultas = []  # Lista 
    
    def __str__(self):
        return f"Dr. {self.nombre} {self.apellido} - {self.especialidad} ({self.anios_experiencia} años exp.)"
    
    def agregar_consulta(self, consulta):
        self.consultas.append(consulta)
    
    def eliminar_consulta(self, id_consulta):
        self.consultas = [c for c in self.consultas if c.id != id_consulta]
        return len(self.consultas)
    
    def tiene_consultas_en_fecha(self, dia, mes):
        for consulta in self.consultas:
            if consulta.dia == dia and consulta.mes == mes:
                return True
        return False
    
    def to_dict(self):
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'especialidad': self.especialidad,
            'anios_experiencia': self.anios_experiencia,
            'consultas': [c.to_dict() for c in self.consultas]
        }
    
    @classmethod
    def from_dict(cls, data):
        medico = cls(
            data['nombre'],
            data['apellido'],
            data['especialidad'],
            data['anios_experiencia']
        )
        medico.consultas = [Consulta.from_dict(c) for c in data['consultas']]
        return medico

class Consultorio:
    def __init__(self, archivo_medicos="medicos.json"):
        self.archivo_medicos = archivo_medicos
        self.medicos = []
        self._cargar_desde_archivo()
    
    def _cargar_desde_archivo(self):
        """Carga los datos desde el archivo JSON"""
        try:
            if os.path.exists(self.archivo_medicos):
                with open(self.archivo_medicos, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.medicos = [Medico.from_dict(m) for m in data]
                print(f"Datos cargados desde {self.archivo_medicos}")
            else:
                print(f"Archivo {self.archivo_medicos} no encontrado. Se creará uno nuevo.")
        except Exception as e:
            print(f"Error al cargar archivo: {e}")
            self.medicos = []
    
    def _guardar_en_archivo(self):
        """Guarda los datos en el archivo JSON"""
        try:
            with open(self.archivo_medicos, 'w', encoding='utf-8') as f:
                data = [m.to_dict() for m in self.medicos]
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Datos guardados en {self.archivo_medicos}")
        except Exception as e:
            print(f"Error al guardar archivo: {e}")
    
    # a) Dar de alta a al menos 3 Médicos y 9 Consultas
    def inicializar_datos(self):
        """Inicializa el sistema con datos de prueba"""
        if self.medicos:
            print("Ya existen datos en el sistema.")
            return
        
        # Crear 3 médicos
        medico1 = Medico("Carlos", "Gómez", "Cardiología", 10)
        medico2 = Medico("Anahi", "Huallpara", "Pediatría", 8)
        medico3 = Medico("Juan", "Martínez", "Dermatología", 12)
        
        # Crear 9 consultas (3 por cada médico)
        # Consultas para médico1
        medico1.agregar_consulta(Consulta(1, "María", "García", 15, "diciembre", 2024))
        medico1.agregar_consulta(Consulta(2, "Pedro", "Sánchez", 25, "diciembre", 2024))  # Navidad
        medico1.agregar_consulta(Consulta(3, "Lucía", "Fernández", 10, "enero", 2024))
        
        # Consultas para médico2
        medico2.agregar_consulta(Consulta(4, "Jorge", "Ramírez", 31, "diciembre", 2024))  # Año Nuevo
        medico2.agregar_consulta(Consulta(5, "Sofía", "Díaz", 5, "enero", 2024))
        medico2.agregar_consulta(Consulta(6, "Diego", "Torres", 1, "enero", 2024))  # Año Nuevo
        
        # Consultas para médico3
        medico3.agregar_consulta(Consulta(7, "Elena", "Ruiz", 24, "diciembre", 2024))  # Nochebuena
        medico3.agregar_consulta(Consulta(8, "Miguel", "Vargas", 15, "noviembre", 2024))
        medico3.agregar_consulta(Consulta(9, "Carmen", "Ortega", 25, "diciembre", 2024))  # Navidad
        
        self.medicos = [medico1, medico2, medico3]
        self._guardar_en_archivo()
        print(" 3 médicos y 9 consultas inicializados correctamente.")
    
    # b) Dar de baja al Médico de nombreX y apellidoY, y sus consultas
    def dar_baja_medico(self, nombre, apellido):
        """Elimina un médico y todas sus consultas"""
        medico_original = len(self.medicos)
        self.medicos = [m for m in self.medicos if not (m.nombre == nombre and m.apellido == apellido)]
        
        if len(self.medicos) < medico_original:
            self._guardar_en_archivo()
            print(f" Médico {nombre} {apellido} eliminado ")
            return True
        else:
            print(f" Médico {nombre} {apellido} no encontrado.")
            return False
    
    # c) Cambiar el día de la consulta de los pacientes en navidad o año nuevo
    def cambiar_consultas_navidad(self, nuevo_dia):
        """Cambia el día de las consultas en Navidad (25 dic) o Año Nuevo (1 ene)"""
        consultas_modificadas = 0
        
        for medico in self.medicos:
            for consulta in medico.consultas:
                # Verificar si es Navidad etc
                if (consulta.dia == 25 and consulta.mes == "diciembre") or \
                   (consulta.dia == 1 and consulta.mes == "enero"):
                    consulta.dia = nuevo_dia
                    consultas_modificadas += 1
        
        if consultas_modificadas > 0:
            self._guardar_en_archivo()
            print(f"{consultas_modificadas} consultas modificadas al día {nuevo_dia}.")
        else:
            print(" No se encontraron consultas en Navidad o Año Nuevo.")
    
    # d) pacientes en mi cumple
    def mostrar_pacientes_cumpleanos(self, dia_cumple, mes_cumple):
        """Muestra pacientes atendidos en una fecha específica"""
        print(f"\n--- Pacientes atendidos el {dia_cumple} de {mes_cumple} ---")
        encontrados = False
        
        for medico in self.medicos:
            for consulta in medico.consultas:
                if consulta.dia == dia_cumple and consulta.mes == mes_cumple:
                    print(f"• {consulta.nombre_paciente} {consulta.apellido_paciente}")
                    print(f"  Médico: Dr. {medico.nombre} {medico.apellido}")
                    print(f"  Especialidad: {medico.especialidad}")
                    print()
                    encontrados = True
        
        if not encontrados:
            print(f"No hay pacientes atendidos el {dia_cumple} de {mes_cumple}")
    
    # Métodos adicionales para mostrar información
    def mostrar_medicos(self):
        """Muestra todos los médicos registrados"""
        print("\n--- Médicos registrados ---")
        if not self.medicos:
            print("No hay médicos registrados.")
            return
        
        for i, medico in enumerate(self.medicos, 1):
            print(f"{i}. {medico}")
            print(f"   Consultas agendadas: {len(medico.consultas)}")
    
    def mostrar_consultas(self):
        """Muestra todas las consultas agendadas"""
        print("\n--- Todas las consultas ---")
        total_consultas = 0
        
        for medico in self.medicos:
            print(f"\nMédico: {medico.nombre} {medico.apellido}")
            if medico.consultas:
                for consulta in medico.consultas:
                    print(f"  - {consulta}")
                    total_consultas += 1
            else:
                print("  Sin consultas agendadas")
        
        print(f"\nTotal de consultas: {total_consultas}")
    
    def buscar_paciente(self, nombre, apellido):
        """Busca consultas de un paciente específico"""
        print(f"\n--- Buscando paciente: {nombre} {apellido} ---")
        encontrado = False
        
        for medico in self.medicos:
            for consulta in medico.consultas:
                if consulta.nombre_paciente == nombre and consulta.apellido_paciente == apellido:
                    print(f"• Fecha: {consulta.dia}/{consulta.mes}/{consulta.ano}")
                    print(f"  Médico: Dr. {medico.nombre} {medico.apellido}")
                    print(f"  Especialidad: {medico.especialidad}")
                    print()
                    encontrado = True
        
        if not encontrado:
            print(f"Paciente {nombre} {apellido} no encontrado.")

# Función principal para ejecutar el sistema
def main():
    consultorio = Consultorio()
    
    # Menú interactivo
    while True:
        print("\n" + "="*50)
        print(" CONSULTORIO MÉDIMAX UMSA")
        print("="*50)
        print("1. Inicializar datos (3 médicos, 9 consultas)")
        print("2. Mostrar todos los médicos")
        print("3. Mostrar todas las consultas")
        print("4. Dar de baja médico")
        print("5. Cambiar consultas de Navidad/Año Nuevo")
        print("6. Mostrar pacientes por fecha (cumpleaños)")
        print("7. Buscar paciente")
        print("8. Salir")
        
        opcion = input("\nSeleccione una opción (1-8): ")
        
        if opcion == "1":
            consultorio.inicializar_datos()
        
        elif opcion == "2":
            consultorio.mostrar_medicos()
        
        elif opcion == "3":
            consultorio.mostrar_consultas()
        
        elif opcion == "4":
            nombre = input("Nombre del médico a eliminar: ")
            apellido = input("Apellido del médico a eliminar: ")
            consultorio.dar_baja_medico(nombre, apellido)
        
        elif opcion == "5":
            try:
                nuevo_dia = int(input("Nuevo día para las consultas (1-31): "))
                if 1 <= nuevo_dia <= 31:
                    consultorio.cambiar_consultas_navidad(nuevo_dia)
                else:
                    print("Día inválido. Debe estar entre 1 y 31.")
            except ValueError:
                print("Entrada inválida. Ingrese un número.")
        
        elif opcion == "6":
            try:
                dia = int(input("Día del cumpleaños (1-31): "))
                mes = input("Mes del cumpleaños (ej: 'enero', 'febrero', etc.): ")
                consultorio.mostrar_pacientes_cumpleanos(dia, mes)
            except ValueError:
                print("Día inválido.")
        
        elif opcion == "7":
            nombre = input("Nombre del paciente: ")
            apellido = input("Apellido del paciente: ")
            consultorio.buscar_paciente(nombre, apellido)
        
        elif opcion == "8":
            print("¡Gracias por usar el sistema!")
            break
        
        else:
            print("Opción inválida. Intente nuevamente.")
        
        input("\nPresione Enter para continuar...")

# Ejecutar ejemplo completo
def ejemplo_completo():
    print("="*60)
    print("Consultorio MediMax umsa")
    print("="*60)
    
    consultorio = Consultorio()
    
    # a) Inicializar datos con 3 médicos y 9 consultas
    print("\na) Inicializando datos...")
    consultorio.inicializar_datos()
    
    # Mostrar datos iniciales
    consultorio.mostrar_medicos()
    consultorio.mostrar_consultas()
    
    # b) Dar de baja al médico "Ana López" y sus consultas
    print("\n\nb) Dando de baja a la Dra. Ana López...")
    consultorio.dar_baja_medico("Ana", "López")
    
    # c) Cambiar día de consultas de Navidad y Año Nuevo al día 28
    print("\n\nc) Cambiando consultas de Navidad y Año Nuevo al día 28...")
    consultorio.cambiar_consultas_navidad(28)
    
    # Mostrar consultas después de los cambios
    print("\nConsultas después de los cambios:")
    consultorio.mostrar_consultas()
    
    # d) Mostrar pacientes atendidos en mi cumple 
    print("\n\nd) Mostrando pacientes atendidos el 25 de noviembre:")
    consultorio.mostrar_pacientes_cumpleanos(25, "noviembre")
    
    # Ejemplo adicional: buscar paciente
   # print("\n\nEjemplo adicional: Buscando al paciente María García")
    #consultorio.buscar_paciente("María", "García")

if __name__ == "__main__":
    
    ejemplo_completo()
    
   
