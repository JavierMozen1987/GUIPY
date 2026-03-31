def generar_codigo(componentes):
    codigo = "import tkinter as tk\n\nroot = tk.Tk()\nroot.geometry('500x400')\n\n"

    for comp in componentes:
        x = comp["x"]
        y = comp["y"]
        texto = comp["texto"]

        if comp["tipo"] == "Button":
            codigo += f"tk.Button(root, text='{texto}').place(x={x}, y={y})\n"

        elif comp["tipo"] == "Label":
            codigo += f"tk.Label(root, text='{texto}').place(x={x}, y={y})\n"

        elif comp["tipo"] == "Entry":
            codigo += f"tk.Entry(root).place(x={x}, y={y})\n"

    codigo += "\nroot.mainloop()"
    return codigo