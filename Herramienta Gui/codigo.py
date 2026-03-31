import tkinter as tk

class Codigo:

    def __init__(self, parent):
        self.texto = tk.Text(parent)
        self.texto.pack(expand=True, fill="both")

    def mostrar_codigo(self, codigo):
        self.texto.delete("1.0", tk.END)
        self.texto.insert(tk.END, codigo)