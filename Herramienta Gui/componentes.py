import tkinter as tk
from tkinter import ttk

def crear_boton(parent):
    return tk.Button(parent, text="Botón")

def crear_label(parent):
    return tk.Label(parent, text="Etiqueta")

def crear_entry(parent):
    return tk.Entry(parent)

def crear_checkbox(parent):
    return tk.Checkbutton(parent, text="Check")

def crear_radiobutton(parent):
    return tk.Radiobutton(parent, text="Opción")

def crear_combobox(parent):
    combo = ttk.Combobox(parent, values=["Opción 1", "Opción 2"])
    combo.current(0)
    return combo

def crear_textarea(parent):
    return tk.Text(parent, height=3, width=15)