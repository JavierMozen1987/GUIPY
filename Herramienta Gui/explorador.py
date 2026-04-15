import tkinter as tk


def crear_explorador(parent):
    frame = tk.Frame(parent, bg="white", width=220)
    frame.pack(side="left", fill="y")
    frame.pack_propagate(False)

    contenido = tk.Frame(frame, bg="white")
    contenido.pack(fill="both", expand=True)

    titulo = tk.Label(
        contenido,
        text="Archivos",
        font=("Segoe UI", 11, "bold"),
        bg="white",
        anchor="w"
    )
    titulo.pack(fill="x", padx=10, pady=(10, 5))

    linea = tk.Frame(contenido, height=1, bg="gray")
    linea.pack(fill="x", padx=5, pady=(0, 5))

    lista = tk.Listbox(
        contenido,
        bg="white",
        bd=0,
        highlightthickness=0,
        activestyle="none",
        exportselection=False
    )
    lista.pack(fill="both", expand=True, padx=5, pady=5)

    separador = tk.Frame(frame, width=2, bg="gray")
    separador.pack(side="right", fill="y")

    return lista