import tkinter as tk
from tkinter import ttk
from componentes import *

class VentanaPrincipal:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CreaGUIPy - Diseñador")
        self.root.geometry("1000x600")

        self.tipo_actual = None
        self.widget_actual = None

        self.crear_interfaz()

    def crear_interfaz(self):

        # =========================
        # PANEL IZQUIERDO
        # =========================
        panel_izq = tk.Frame(self.root, width=180, bg="#e6e6e6")
        panel_izq.pack(side="left", fill="y")

        tk.Label(panel_izq, text="Archivos", bg="#e6e6e6",
                 font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=5)

        lista_archivos = tk.Listbox(panel_izq)
        lista_archivos.insert(0, "Archivo.py")
        lista_archivos.pack(fill="both", expand=True, padx=5, pady=5)

        # =========================
        # PANEL DERECHO (COMPONENTES)
        # =========================
        self.crear_panel_componentes(self.root)

        # =========================
        # ÁREA CENTRAL
        # =========================
        centro = tk.Frame(self.root, bg="#dddddd")
        centro.pack(expand=True, fill="both")

        tabs = ttk.Notebook(centro)
        tabs.pack(fill="both", expand=True)

        frame_diseno = tk.Frame(tabs, bg="#dddddd")
        frame_codigo = tk.Frame(tabs)

        tabs.add(frame_diseno, text="Diseño")
        tabs.add(frame_codigo, text="Código")

        # =========================
        # CANVAS
        # =========================
        self.canvas = tk.Frame(
            frame_diseno,
            width=500,
            height=400,
            bg="white",
            relief="solid",
            borderwidth=1
        )
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")

        barra = tk.Frame(self.canvas, bg="#dcdcdc", height=25)
        barra.pack(fill="x")

        tk.Label(barra, text="Archivo", bg="#dcdcdc").pack(side="left", padx=5)

    # =========================
    # PANEL COMPONENTES
    # =========================
    def crear_panel_componentes(self, parent):

        panel_der = tk.Frame(parent, width=220, bg="#f0f0f0")
        panel_der.pack(side="right", fill="y")

        tk.Label(panel_der, text="Componentes",
                 font=("Arial", 10, "bold"), bg="#f0f0f0").pack(pady=5)

        self.lista_componentes = [
            ("🔘", "Botón", "Button"),
            ("🏷️", "Etiqueta", "Label"),
            ("⌨️", "Input", "Entry"),
            ("☑️", "CheckBox", "Check"),
            ("🔵", "RadioButton", "Radio"),
            ("📋", "ComboBox", "Combo"),
            ("📝", "TextArea", "Text")
        ]

        for icono, nombre, tipo in self.lista_componentes:
            frame = tk.Frame(panel_der, bg="white", relief="solid", borderwidth=1)
            frame.pack(fill="x", padx=10, pady=4)

            label = tk.Label(frame, text=f"{icono} {nombre}", bg="white", anchor="w")
            label.pack(fill="x", padx=5, pady=5)

            label.bind("<Button-1>", lambda e, t=tipo: self.iniciar_drag(t))

    # =========================
    # DRAG INICIO
    # =========================
    def iniciar_drag(self, tipo):
        self.tipo_actual = tipo
        self.root.bind("<ButtonRelease-1>", self.soltar_componente)

    # =========================
    # SOLTAR COMPONENTE
    # =========================
    def soltar_componente(self, event):

        x = event.x_root - self.canvas.winfo_rootx()
        y = event.y_root - self.canvas.winfo_rooty()

        if self.tipo_actual == "Button":
            widget = crear_boton(self.canvas)

        elif self.tipo_actual == "Label":
            widget = crear_label(self.canvas)

        elif self.tipo_actual == "Entry":
            widget = crear_entry(self.canvas)

        elif self.tipo_actual == "Check":
            widget = crear_checkbox(self.canvas)

        elif self.tipo_actual == "Radio":
            widget = crear_radiobutton(self.canvas)

        elif self.tipo_actual == "Combo":
            widget = crear_combobox(self.canvas)

        elif self.tipo_actual == "Text":
            widget = crear_textarea(self.canvas)

        else:
            return

        widget.place(x=x, y=y)

        widget.bind("<Button-1>", self.seleccionar)
        widget.bind("<B1-Motion>", self.arrastrar)

        self.root.unbind("<ButtonRelease-1>")

    # =========================
    # MOVER COMPONENTES
    # =========================
    def seleccionar(self, event):
        self.widget_actual = event.widget

    def arrastrar(self, event):
        x = event.x_root - self.canvas.winfo_rootx()
        y = event.y_root - self.canvas.winfo_rooty()

        self.widget_actual.place(x=x, y=y)

    def run(self):
        self.root.mainloop()