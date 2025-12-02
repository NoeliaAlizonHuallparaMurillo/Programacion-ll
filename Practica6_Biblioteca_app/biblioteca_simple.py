#!/usr/bin/env python3
# biblioteca_simple.py
#  JSON + Tkinter (listas) 

import json
import os
from datetime import date
import tkinter as tk
from tkinter import simpledialog, messagebox

DATA_FILE = "biblioteca.json"

# - Modelos míni
class Autor:
    def __init__(self, nombre, nacionalidad):
        self.nombre = nombre
        self.nacionalidad = nacionalidad
    def to_dict(self): return {"nombre": self.nombre, "nacionalidad": self.nacionalidad}
    @classmethod
    def from_dict(cls,d): return cls(d["nombre"], d["nacionalidad"])

class Estudiante:
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre
    def to_dict(self): return {"codigo": self.codigo, "nombre": self.nombre}
    @classmethod
    def from_dict(cls,d): return cls(d["codigo"], d["nombre"])

class Libro:
    def __init__(self, titulo, isbn, contenidos):
        self.titulo = titulo
        self.isbn = isbn
        self.paginas = contenidos[:]  # lista de textos
        self.disponible = True
    def to_dict(self): return {"titulo":self.titulo,"isbn":self.isbn,"paginas":self.paginas,"disponible":self.disponible}
    @classmethod
    def from_dict(cls,d):
        l = cls(d["titulo"], d["isbn"], d.get("paginas", []))
        l.disponible = d.get("disponible", True)
        return l

class Prestamo:
    def __init__(self, estudiante_codigo, libro_isbn):
        self.estudiante_codigo = estudiante_codigo
        self.libro_isbn = libro_isbn
        self.fecha_prestamo = date.today().isoformat()
        self.fecha_devolucion = None
    def to_dict(self): return {"estudiante_codigo":self.estudiante_codigo,"libro_isbn":self.libro_isbn,"fecha_prestamo":self.fecha_prestamo,"fecha_devolucion":self.fecha_devolucion}
    @classmethod
    def from_dict(cls,d):
        p = cls(d["estudiante_codigo"], d["libro_isbn"])
        p.fecha_prestamo = d.get("fecha_prestamo")
        p.fecha_devolucion = d.get("fecha_devolucion")
        return p

# -- Biblioteca (colecciones) --
class Biblioteca:
    def __init__(self):
        self.autores = []
        self.libros = []
        self.estudiantes = []
        self.prestamos = []

    def to_dict(self):
        return {
            "autores":[a.to_dict() for a in self.autores],
            "libros":[l.to_dict() for l in self.libros],
            "estudiantes":[e.to_dict() for e in self.estudiantes],
            "prestamos":[p.to_dict() for p in self.prestamos]
        }

    @classmethod
    def from_dict(cls,d):
        b = cls()
        b.autores = [Autor.from_dict(ad) for ad in d.get("autores",[])]
        b.libros = [Libro.from_dict(ld) for ld in d.get("libros",[])]
        b.estudiantes = [Estudiante.from_dict(ed) for ed in d.get("estudiantes",[])]
        b.prestamos = [Prestamo.from_dict(pd) for pd in d.get("prestamos",[])]
        return b

    # operaciones 
    def agregar_autor(self, nombre, nac):
        self.autores.append(Autor(nombre, nac))

    def agregar_estudiante(self, codigo, nombre):
        if any(e.codigo==codigo for e in self.estudiantes): raise ValueError("Código ya existe")
        self.estudiantes.append(Estudiante(codigo, nombre))

    def agregar_libro(self, titulo, isbn, paginas):
        if any(l.isbn==isbn for l in self.libros): raise ValueError("ISBN ya existe")
        self.libros.append(Libro(titulo, isbn, paginas))

    def prestar_libro(self, codigo, isbn):
        est = next((e for e in self.estudiantes if e.codigo==codigo), None)
        lib = next((l for l in self.libros if l.isbn==isbn), None)
        if not est: raise ValueError("Estudiante no encontrado")
        if not lib: raise ValueError("Libro no encontrado")
        if not lib.disponible: raise ValueError("Libro no disponible")
        lib.disponible = False
        p = Prestamo(codigo, isbn)
        self.prestamos.append(p)
        return p

    def devolver_libro(self, codigo, isbn):
        p = next((x for x in self.prestamos if x.estudiante_codigo==codigo and x.libro_isbn==isbn and x.fecha_devolucion is None), None)
        if not p: raise ValueError("Préstamo activo no encontrado")
        p.fecha_devolucion = date.today().isoformat()
        lib = next((l for l in self.libros if l.isbn==isbn), None)
        if lib: lib.disponible = True
        return p

# -- Guardar o Cargar JSON --
def guardar(bib, ruta=DATA_FILE):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(bib.to_dict(), f, ensure_ascii=False, indent=4)

def cargar(ruta=DATA_FILE):
    if not os.path.exists(ruta):
        return Biblioteca()
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)
    return Biblioteca.from_dict(data)

# ----- Interfaz Tkinter -----
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Biblioteca simple")
        self.geometry("760x420")
        self.bib = cargar()
        self.crear_ui()
        self.refrescar_listas()

    def crear_ui(self):
        # botones arriba
        frm = tk.Frame(self)
        frm.pack(fill=tk.X, pady=6)
        tk.Button(frm, text="Agregar Autor", command=self.agregar_autor).pack(side=tk.LEFT, padx=4)
        tk.Button(frm, text="Agregar Libro", command=self.agregar_libro).pack(side=tk.LEFT, padx=4)
        tk.Button(frm, text="Agregar Estudiante", command=self.agregar_estudiante).pack(side=tk.LEFT, padx=4)
        tk.Button(frm, text="Prestar Libro", command=self.prestar).pack(side=tk.LEFT, padx=4)
        tk.Button(frm, text="Devolver Libro", command=self.devolver).pack(side=tk.LEFT, padx=4)
        tk.Button(frm, text="Guardar", command=self.guardar).pack(side=tk.RIGHT, padx=6)

        # listas (autores | libros | estudiantes | prestamos)
        cont = tk.Frame(self)
        cont.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        # Autores
        la = tk.Label(cont, text="Autores")
        la.grid(row=0, column=0, sticky="w")
        self.lst_aut = tk.Listbox(cont, width=30, height=15)
        self.lst_aut.grid(row=1, column=0, padx=4, pady=2)

        # Libros
        ll = tk.Label(cont, text="Libros (ISBN | Titulo | Estado)")
        ll.grid(row=0, column=1, sticky="w")
        self.lst_lib = tk.Listbox(cont, width=40, height=15)
        self.lst_lib.grid(row=1, column=1, padx=4, pady=2)

        # Estudiantes
        le = tk.Label(cont, text="Estudiantes (Codigo | Nombre)")
        le.grid(row=0, column=2, sticky="w")
        self.lst_est = tk.Listbox(cont, width=30, height=15)
        self.lst_est.grid(row=1, column=2, padx=4, pady=2)

        # Préstamos
        lp = tk.Label(cont, text="Préstamos (ISBN -> Codigo | Prest | Devolución)")
        lp.grid(row=2, column=0, columnspan=3, sticky="w", pady=(8,0))
        self.lst_pres = tk.Listbox(cont, width=110, height=8)
        self.lst_pres.grid(row=3, column=0, columnspan=3, padx=4, pady=2)

    # acciones 
    def agregar_autor(self):
        n = simpledialog.askstring("Autor","Nombre:")
        if not n: return
        c = simpledialog.askstring("Autor","Nacionalidad:")
        if not c: return
        self.bib.agregar_autor(n.strip(), c.strip())
        self.refrescar_listas()

    def agregar_estudiante(self):
        codigo = simpledialog.askstring("Estudiante","Código:")
        if not codigo: return
        nombre = simpledialog.askstring("Estudiante","Nombre:")
        if not nombre: return
        try:
            self.bib.agregar_estudiante(codigo.strip(), nombre.strip())
            self.refrescar_listas()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def agregar_libro(self):
        titulo = simpledialog.askstring("Libro","Título:")
        if not titulo: return
        isbn = simpledialog.askstring("Libro","ISBN:")
        if not isbn: return
        paginas = simpledialog.askstring("Libro","Páginas (separe por ';'):")
        if paginas is None: return
        contenidos = [p.strip() for p in paginas.split(";") if p.strip()]
        if not contenidos: contenidos = ["Contenido"]
        try:
            self.bib.agregar_libro(titulo.strip(), isbn.strip(), contenidos)
            self.refrescar_listas()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def prestar(self):
        codigo = simpledialog.askstring("Prestar","Código del estudiante:")
        if not codigo: return
        isbn = simpledialog.askstring("Prestar","ISBN del libro a prestar:")
        if not isbn: return
        try:
            self.bib.prestar_libro(codigo.strip(), isbn.strip())
            self.refrescar_listas()
            messagebox.showinfo("OK","Préstamo registrado")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def devolver(self):
        codigo = simpledialog.askstring("Devolver","Código del estudiante:")
        if not codigo: return
        isbn = simpledialog.askstring("Devolver","ISBN del libro a devolver:")
        if not isbn: return
        try:
            self.bib.devolver_libro(codigo.strip(), isbn.strip())
            self.refrescar_listas()
            messagebox.showinfo("OK","Devolución registrada")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def guardar(self):
        try:
            guardar(self.bib)
            messagebox.showinfo("Guardar","Datos guardados en "+DATA_FILE)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refrescar_listas(self):
        self.lst_aut.delete(0, tk.END)
        for a in self.bib.autores: self.lst_aut.insert(tk.END, f"{a.nombre} ({a.nacionalidad})")
        self.lst_lib.delete(0, tk.END)
        for l in self.bib.libros: self.lst_lib.insert(tk.END, f"{l.isbn} | {l.titulo} | {'Disponible' if l.disponible else 'Prestado'}")
        self.lst_est.delete(0, tk.END)
        for e in self.bib.estudiantes: self.lst_est.insert(tk.END, f"{e.codigo} | {e.nombre}")
        self.lst_pres.delete(0, tk.END)
        for p in self.bib.prestamos:
            self.lst_pres.insert(tk.END, f"{p.libro_isbn} -> {p.estudiante_codigo} | {p.fecha_prestamo} | {p.fecha_devolucion or 'No devuelto'}")

# Main
if __name__ == "__main__":
    app = App()
    app.mainloop()
