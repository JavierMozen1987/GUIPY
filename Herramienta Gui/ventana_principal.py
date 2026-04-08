import tkinter as tk
from tkinter import ttk
from componentes import *
from tkinter import colorchooser
from tkinter import font

class VentanaPrincipal:

    def __init__(self, parent):
        self.root = parent
        self.widget_actual = None
        self.widgets = []
        self.crear_ui()

    def crear_ui(self):

        # =========================
        # CONTENEDOR PRINCIPAL
        # =========================
        main_paned = ttk.PanedWindow(self.root, orient="horizontal")
        main_paned.pack(fill="both", expand=True)

        # =========================
        # PANEL IZQUIERDO
        # =========================
        panel_izq = ttk.Frame(main_paned, width=200)
        main_paned.add(panel_izq)

        ttk.Label(panel_izq, text="Explorador",
                  font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=5)

        self.lista_archivos = tk.Listbox(panel_izq)
        self.lista_archivos.insert(0, "main.py")
        self.lista_archivos.pack(fill="both", expand=True, padx=5, pady=5)

        # =========================
        # PANEL CENTRAL
        # =========================
        panel_centro = ttk.Frame(main_paned)
        main_paned.add(panel_centro, weight=1)

        tabs = ttk.Notebook(panel_centro)
        tabs.pack(fill="both", expand=True)

        frame_diseno = ttk.Frame(tabs)
        tabs.add(frame_diseno, text="Diseño")

        self.canvas = tk.Frame(frame_diseno, bg="white", relief="solid", borderwidth=1)
        self.canvas.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)

        frame_codigo = ttk.Frame(tabs)
        tabs.add(frame_codigo, text="Código")

        self.text_codigo = tk.Text(frame_codigo)
        self.text_codigo.pack(fill="both", expand=True)

        # =========================
        # PANEL DERECHO
        # =========================
        panel_der = ttk.Frame(main_paned, width=250)
        main_paned.add(panel_der)

        tabs_der = ttk.Notebook(panel_der)
        tabs_der.pack(fill="both", expand=True)

        # =========================
        # TAB COMPONENTES
        # =========================
        tab_componentes = ttk.Frame(tabs_der)
        tabs_der.add(tab_componentes, text="Componentes")

        componentes = [
            ("Botón", "Button"),
            ("Label", "Label"),
            ("Input", "Entry"),
            ("CheckBox", "Check"),
            ("RadioButton", "Radio"),
            ("ComboBox", "Combo"),
            ("TextArea", "Text"),
            ("Frame", "Frame")
        ]

        for nombre, tipo in componentes:
            btn = ttk.Button(tab_componentes, text=nombre,
                             command=lambda t=tipo: self.crear_componente(t))
            btn.pack(fill="x", padx=5, pady=5)

        # =========================
        # TAB PROPIEDADES ✅ (AQUÍ ESTABA EL ERROR)
        # =========================
        self.tab_propiedades = ttk.Frame(tabs_der)
        tabs_der.add(self.tab_propiedades, text="Propiedades")

        ttk.Label(self.tab_propiedades, text="Texto:").pack(pady=5)
        self.entry_texto = ttk.Entry(self.tab_propiedades)
        self.entry_texto.pack(fill="x", padx=5)

        ttk.Label(self.tab_propiedades, text="Tamaño letra:").pack(pady=5)
        self.entry_size = ttk.Entry(self.tab_propiedades)
        self.entry_size.pack(fill="x", padx=5)

        ttk.Label(self.tab_propiedades, text="Fuente:").pack(pady=5)
        self.combo_font = ttk.Combobox(self.tab_propiedades,
                                       values=["Arial", "Times", "Courier"])
        self.combo_font.pack(fill="x", padx=5)

        ttk.Button(self.tab_propiedades, text="Color texto",
                   command=self.cambiar_color_texto).pack(pady=5)

        ttk.Button(self.tab_propiedades, text="Color fondo",
                   command=self.cambiar_color_fondo).pack(pady=5)

        ttk.Button(self.tab_propiedades, text="Aplicar",
                   command=self.aplicar_propiedades).pack(pady=10)

    # =========================
    # CREAR COMPONENTES
    # =========================
    def crear_componente(self, tipo):

        if tipo == "Button":
            widget = crear_boton(self.canvas)

        elif tipo == "Label":
            widget = crear_label(self.canvas)

        elif tipo == "Entry":
            widget = crear_entry(self.canvas)

        elif tipo == "Check":
            widget = crear_checkbox(self.canvas)

        elif tipo == "Radio":
            widget = crear_radiobutton(self.canvas)

        elif tipo == "Combo":
            widget = crear_combobox(self.canvas)

        elif tipo == "Text":
            widget = crear_textarea(self.canvas)

        elif tipo == "Frame":
            widget = tk.Frame(self.canvas, bg="lightgray", width=100, height=50)

        else:
            return

        widget.place(x=50, y=50)

        widget.bind("<Button-1>", self.seleccionar)
        widget.bind("<B1-Motion>", self.arrastrar)

        # 🔥 GUARDAR INFO
        self.widgets.append({
            "widget": widget,
            "tipo": tipo,
            "x": 50,
            "y": 50
        })

        self.generar_codigo()

    # =========================
    # SELECCIONAR
    # =========================
    def seleccionar(self, event):
        self.widget_actual = event.widget

        try:
            texto = self.widget_actual.cget("text")
            self.entry_texto.delete(0, tk.END)
            self.entry_texto.insert(0, texto)
        except:
            pass

    # =========================
    # ARRASTRAR
    # =========================
    def arrastrar(self, event):
        x = event.x_root - self.canvas.winfo_rootx()
        y = event.y_root - self.canvas.winfo_rooty()

        self.widget_actual.place(x=x, y=y)

        # 🔥 actualizar en lista
        for w in self.widgets:
            if w["widget"] == self.widget_actual:
                w["x"] = x
                w["y"] = y

        self.generar_codigo()

    # =========================
    # PROPIEDADES
    # =========================
    def aplicar_propiedades(self):

        if not self.widget_actual:
            return

        try:
            self.widget_actual.config(text=self.entry_texto.get())
        except:
            pass

        try:
            size = int(self.entry_size.get())
            tipo = self.combo_font.get()

            nueva_fuente = font.Font(family=tipo, size=size)
            self.widget_actual.config(font=nueva_fuente)
        except:
            pass

    def cambiar_color_texto(self):
        color = colorchooser.askcolor()[1]
        if self.widget_actual and color:
            try:
                self.widget_actual.config(fg=color)
            except:
                pass

    def cambiar_color_fondo(self):
        color = colorchooser.askcolor()[1]
        if self.widget_actual and color:
            try:
                self.widget_actual.config(bg=color)
            except:
                pass

    def generar_codigo(self):

        codigo = "import tkinter as tk\n\n"
        codigo += "root = tk.Tk()\n\n"

        for i, w in enumerate(self.widgets):
            tipo = w["tipo"]
            x = w["x"]
            y = w["y"]

            nombre = f"widget_{i}"

            if tipo == "Button":
                codigo += f'{nombre} = tk.Button(root, text="Botón")\n'

            elif tipo == "Label":
                codigo += f'{nombre} = tk.Label(root, text="Label")\n'

            elif tipo == "Entry":
                codigo += f'{nombre} = tk.Entry(root)\n'

            elif tipo == "Check":
                codigo += f'{nombre} = tk.Checkbutton(root, text="Check")\n'

            elif tipo == "Radio":
                codigo += f'{nombre} = tk.Radiobutton(root, text="Radio")\n'

            elif tipo == "Combo":
                codigo += f'{nombre} = ttk.Combobox(root)\n'

            elif tipo == "Text":
                codigo += f'{nombre} = tk.Text(root, height=4, width=20)\n'

            elif tipo == "Frame":
                codigo += f'{nombre} = tk.Frame(root, bg="lightgray", width=100, height=50)\n'

            codigo += f"{nombre}.place(x={x}, y={y})\n\n"

        codigo += "root.mainloop()"

        # 🔥 mostrar en pestaña código
        self.text_codigo.delete("1.0", tk.END)
        self.text_codigo.insert(tk.END, codigo)
