import tkinter as tk
from componentes import crear_boton, crear_label, crear_entry

class Diseno:

    def __init__(self, parent, componentes, callback):
        self.parent = parent
        self.componentes = componentes
        self.callback = callback

        self.widget_seleccionado = None
        self.data_seleccionada = None

        self.crear_ui()

    def crear_ui(self):
        self.panel = tk.Frame(self.parent, width=200, bg="#f0f0f0")
        self.panel.pack(side="right", fill="y")

        tk.Button(self.panel, text="Botón", command=self.agregar_boton).pack(fill="x")
        tk.Button(self.panel, text="Label", command=self.agregar_label).pack(fill="x")
        tk.Button(self.panel, text="Input", command=self.agregar_entry).pack(fill="x")

        self.canvas = tk.Frame(self.parent, bg="white")
        self.canvas.pack(expand=True, fill="both")

    # =====================
    # CREAR COMPONENTES
    # =====================

    def agregar_boton(self):
        widget = crear_boton(self.canvas)
        self.registrar(widget, "Button", "Botón")

    def agregar_label(self):
        widget = crear_label(self.canvas)
        self.registrar(widget, "Label", "Etiqueta")

    def agregar_entry(self):
        widget = crear_entry(self.canvas)
        self.registrar(widget, "Entry", "")

    def registrar(self, widget, tipo, texto):
        widget.place(x=50, y=50)

        data = {
            "tipo": tipo,
            "x": 50,
            "y": 50,
            "texto": texto,
            "widget": widget
        }

        self.componentes.append(data)

        # 🔥 EVENTOS CORRECTOS
        widget.bind("<Button-1>", self.seleccionar)
        widget.bind("<B1-Motion>", self.arrastrar)

        self.callback()

    # =====================
    # SELECCIONAR
    # =====================

    def seleccionar(self, event):
        self.widget_seleccionado = event.widget

        for comp in self.componentes:
            if comp["widget"] == self.widget_seleccionado:
                self.data_seleccionada = comp
                break

    # =====================
    # ARRASTRAR (CORREGIDO)
    # =====================

    def arrastrar(self, event):
        if not self.widget_seleccionado:
            return

        # 🔥 COORDENADAS RELATIVAS AL CANVAS
        x = event.x_root - self.canvas.winfo_rootx()
        y = event.y_root - self.canvas.winfo_rooty()

        self.widget_seleccionado.place(x=x, y=y)

        # 🔥 ACTUALIZA DATOS
        self.data_seleccionada["x"] = x
        self.data_seleccionada["y"] = y

        self.callback()

    # =====================
    # LIMPIAR
    # =====================

    def limpiar_canvas(self):
        for widget in self.canvas.winfo_children():
            widget.destroy()