import tkinter as tk

def crear_explorador(parent):

    frame = tk.Frame(parent, bg="#f0f0f0", width=200)
    frame.pack(side="left", fill="y")

    tk.Label(frame, text="Explorador",
             font=("Segoe UI", 10, "bold"),
             bg="#f0f0f0").pack(anchor="w", padx=10, pady=5)

    lista = tk.Listbox(frame)
    lista.pack(fill="both", expand=True, padx=5, pady=5)

    return lista