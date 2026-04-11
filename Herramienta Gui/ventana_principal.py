import tkinter as tk
from tkinter import ttk, colorchooser, font, messagebox, filedialog
from componentes import *
from explorador import crear_explorador
import os

class VentanaPrincipal:

    def __init__(self, parent):
        self.root = parent
        self.widget_actual = None
        self.data_actual = None
        self.widgets = []
        self.nombre_archivo = "archivo.py"
        self.ruta_archivo = os.path.join(os.getcwd(), self.nombre_archivo)

        self.crear_ui()

    def crear_ui(self):
        style = ttk.Style()

        # Tema base
        style.theme_use("default")

        # Fondo general
        style.configure("TFrame", background="#ECE7E7")

        # Notebook (pestañas)
        style.configure("TNotebook", background="#ECE7E7", borderwidth=0)

        # Pestañas normales (NO seleccionadas)
        style.configure(
            "TNotebook.Tab",
            background="#ECE7E7",
            padding=5
        )

        # Pestaña seleccionada
        style.map(
            "TNotebook.Tab",
            background=[("selected", "white")],
            expand=[("selected", [1, 1, 1, 0])]
        )

        # Frame blanco personalizado
        style.configure("Blanco.TFrame", background="white")
        # =========================
        # CONTENEDOR PRINCIPAL
        # =========================
        contenedor_principal = tk.Frame(self.root)
        contenedor_principal.pack(fill="both", expand=True)

        # IZQUIERDA + CENTRO (movible)
        main_paned = ttk.PanedWindow(contenedor_principal, orient="horizontal")
        main_paned.pack(side="left", fill="both", expand=True)

        # PANEL DERECHO (FIJO)
        panel_der = ttk.Frame(contenedor_principal, width=280)
        panel_der.pack(side="right", fill="y")

        panel_der.pack_propagate(False)

        # =========================
        # PANEL IZQUIERDO
        # =========================
        self.lista_archivos = crear_explorador(main_paned)

        try:
            self.lista_archivos.delete(0, tk.END)
            self.lista_archivos.insert(tk.END, self.nombre_archivo)
        except Exception:
            pass

        try:
            contenedor_explorador = self.lista_archivos.master
            ttk.Button(
                contenedor_explorador,
                text="Guardar archivo",
                command=self.guardar_codigo_python
            ).pack(fill="x", padx=5, pady=5)
        except Exception:
            pass

        # =========================
        # PANEL CENTRAL
        # =========================
        panel_centro = ttk.Frame(main_paned)
        main_paned.add(panel_centro, weight=1)

        tabs = ttk.Notebook(panel_centro)
        tabs.pack(fill="both", expand=True)

        frame_diseno = ttk.Frame(tabs, style="Blanco.TFrame")
        tabs.add(frame_diseno, text="Diseño")

        # =========================
        # VENTANA DE DISEÑO (FAKE WINDOW)
        # =========================
        contenedor_ventana = tk.Frame(
            frame_diseno,
            bg="#ECE7E7"
        )
        contenedor_ventana.place(relx=0.5, rely=0.5, anchor="center", width=720, height=480)

        # Marco de ventana
        ventana_mock = tk.Frame(
            contenedor_ventana,
            bg="white",
            relief="solid",
            borderwidth=1
        )
        ventana_mock.pack(fill="both", expand=True)

        # =========================
        # BARRA SUPERIOR (tipo ventana)
        # =========================
        barra_titulo = tk.Frame(
            ventana_mock,
            bg="#ECE7E7",
            height=30
        )
        barra_titulo.pack(fill="x")

        # Título
        tk.Label(
            barra_titulo,
            text="Ventana de diseño",
            bg="#ECE7E7"
        ).pack(side="left", padx=10)

        # Botones (visual)
        frame_botones = tk.Frame(barra_titulo, bg="#ECE7E7")
        frame_botones.pack(side="right", padx=5)

        tk.Label(frame_botones, text="—", bg="#ECE7E7", width=3).pack(side="left")
        tk.Label(frame_botones, text="□", bg="#ECE7E7", width=3).pack(side="left")
        tk.Label(frame_botones, text="✕", bg="#ECE7E7", width=3).pack(side="left")

        # =========================
        # ÁREA DE DISEÑO (CANVAS)
        # =========================
        self.canvas = tk.Frame(
            ventana_mock,
            bg="white"
        )
        self.canvas.pack(fill="both", expand=True)
    
        frame_codigo = ttk.Frame(tabs)
        tabs.add(frame_codigo, text="Código")

        self.text_codigo = tk.Text(frame_codigo, wrap="none")
        self.text_codigo.pack(fill="both", expand=True)

        # =========================
        # PANEL DERECHO
        # =========================

        tabs_der = ttk.Notebook(panel_der)
        tabs_der.pack(fill="both", expand=True)

        # =========================
        # TAB COMPONENTES
        # =========================
        tab_componentes = tk.Frame(tabs_der, bg="white")
        tabs_der.add(tab_componentes, text="Componentes")

        # Dividir en dos secciones (arriba/abajo)
        contenedor_dividido = tk.PanedWindow(tab_componentes,orient="vertical",bg="#ECE7E7",sashwidth=5)
        contenedor_dividido.pack(fill="both", expand=True)

        # =========================
        # ARRIBA → COMPONENTES
        # =========================
        frame_componentes = tk.Frame(contenedor_dividido, bg="white")
        contenedor_dividido.add(frame_componentes)

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
            btn = ttk.Button(
                frame_componentes,
                text=nombre,
                command=lambda t=tipo: self.crear_componente(t)
            )
            btn.pack(fill="x", padx=5, pady=5)

        # =========================
        # ABAJO → PROPIEDADES
        # =========================
       
        frame_propiedades = tk.Frame(contenedor_dividido, bg="white", padx=10, pady=10)
        contenedor_dividido.add(frame_propiedades)

        # Título
        tk.Label(
            frame_propiedades,
            text="Propiedades",
            bg="white",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(0, 5))

        # Línea separadora
        linea = tk.Frame(frame_propiedades, bg="#9F8484", height=2)
        linea.pack(fill="x", pady=(0, 10))

        ttk.Label(frame_propiedades, text="Texto:").pack(anchor="w", pady=(0, 3))
        self.entry_texto = ttk.Entry(frame_propiedades)
        self.entry_texto.pack(fill="x", pady=(0, 8))

        ttk.Label(frame_propiedades, text="Tamaño letra:").pack(anchor="w", pady=(0, 3))
        self.entry_size = ttk.Entry(frame_propiedades)
        self.entry_size.pack(fill="x", pady=(0, 8))

        ttk.Label(frame_propiedades, text="Fuente:").pack(anchor="w", pady=(0, 3))
        self.combo_font = ttk.Combobox(
            frame_propiedades,
            values=["Arial", "Times New Roman", "Courier New", "Verdana", "Segoe UI"],
            state="readonly"
        )
        self.combo_font.pack(fill="x", pady=(0, 8))
        self.combo_font.set("Arial")

        ttk.Label(frame_propiedades, text="Ancho:").pack(anchor="w", pady=(0, 3))
        self.entry_width = ttk.Entry(frame_propiedades)
        self.entry_width.pack(fill="x", pady=(0, 8))

        ttk.Label(frame_propiedades, text="Alto:").pack(anchor="w", pady=(0, 3))
        self.entry_height = ttk.Entry(frame_propiedades)
        self.entry_height.pack(fill="x", pady=(0, 8))

        ttk.Button(
            frame_propiedades,
            text="Color texto",
            command=self.cambiar_color_texto
        ).pack(fill="x", pady=4)

        ttk.Button(
            frame_propiedades,
            text="Color fondo",
            command=self.cambiar_color_fondo
        ).pack(fill="x", pady=4)

        ttk.Button(
            frame_propiedades,
            text="Aplicar",
            command=self.aplicar_propiedades
        ).pack(fill="x", pady=(12, 4))

        ttk.Button(
            frame_propiedades,
            text="Eliminar componente",
            command=self.eliminar_componente
        ).pack(fill="x", pady=4)

        # =========================
        # TAB PROPIEDADES
        # =========================
        self.tab_uniones = ttk.Frame(tabs_der)
        tabs_der.add(self.tab_uniones, text="Uniones")

       
    # =========================
    # CREAR COMPONENTES
    # =========================
    def crear_componente(self, tipo):

        if tipo == "Button":
            widget = crear_boton(self.canvas)
            width, height = 100, 30
            text = "Botón"

        elif tipo == "Label":
            widget = crear_label(self.canvas)
            width, height = 100, 30
            text = "Etiqueta"

        elif tipo == "Entry":
            widget = crear_entry(self.canvas)
            width, height = 140, 28
            text = ""

        elif tipo == "Check":
            widget = crear_checkbox(self.canvas)
            width, height = 120, 30
            text = "Check"

        elif tipo == "Radio":
            widget = crear_radiobutton(self.canvas)
            width, height = 120, 30
            text = "Opción"

        elif tipo == "Combo":
            widget = crear_combobox(self.canvas)
            width, height = 140, 30
            text = ""

        elif tipo == "Text":
            widget = crear_textarea(self.canvas)
            width, height = 180, 80
            text = ""

        elif tipo == "Frame":
            widget = tk.Frame(self.canvas, bg="lightgray", relief="solid", borderwidth=1)
            width, height = 120, 70
            text = ""

        else:
            return

        widget.place(x=50, y=50, width=width, height=height)

        data = {
            "widget": widget,
            "tipo": tipo,
            "x": 50,
            "y": 50,
            "props": {
                "text": text,
                "fg": "",
                "bg": "lightgray" if tipo == "Frame" else "",
                "font_family": "Arial",
                "font_size": 10,
                "width": width,
                "height": height
            }
        }

        self.widgets.append(data)
        self.aplicar_estilo_inicial(data)

        widget.bind("<Button-1>", self.seleccionar)
        widget.bind("<B1-Motion>", self.arrastrar)

        self.generar_codigo()

    def aplicar_estilo_inicial(self, data):
        widget = data["widget"]
        props = data["props"]

        try:
            if data["tipo"] in ["Button", "Label", "Check", "Radio"]:
                widget.config(text=props["text"])
        except Exception:
            pass

        try:
            f = font.Font(family=props["font_family"], size=props["font_size"])
            if data["tipo"] in ["Button", "Label", "Check", "Radio"]:
                widget.config(font=f)
        except Exception:
            pass

    # =========================
    # SELECCIONAR
    # =========================
    def seleccionar(self, event):
        self.widget_actual = event.widget
        self.data_actual = None

        for item in self.widgets:
            if item["widget"] == self.widget_actual:
                self.data_actual = item
                break

        if not self.data_actual:
            return

        props = self.data_actual["props"]

        self.entry_texto.delete(0, tk.END)
        self.entry_texto.insert(0, props["text"])

        self.entry_size.delete(0, tk.END)
        self.entry_size.insert(0, str(props["font_size"]))

        self.combo_font.set(props["font_family"])

        self.entry_width.delete(0, tk.END)
        self.entry_width.insert(0, str(props["width"]))

        self.entry_height.delete(0, tk.END)
        self.entry_height.insert(0, str(props["height"]))

    # =========================
    # ARRASTRAR
    # =========================
    def arrastrar(self, event):
        if not self.widget_actual:
            return

        x = event.x_root - self.canvas.winfo_rootx()
        y = event.y_root - self.canvas.winfo_rooty()

        x = max(0, x)
        y = max(0, y)

        self.widget_actual.place(x=x, y=y)

        for item in self.widgets:
            if item["widget"] == self.widget_actual:
                item["x"] = x
                item["y"] = y
                break

        self.generar_codigo()

    # =========================
    # PROPIEDADES
    # =========================
    def aplicar_propiedades(self):

        if not self.widget_actual or not self.data_actual:
            return

        props = self.data_actual["props"]
        tipo = self.data_actual["tipo"]

        # Texto
        nuevo_texto = self.entry_texto.get()
        props["text"] = nuevo_texto

        try:
            if tipo in ["Button", "Label", "Check", "Radio"]:
                self.widget_actual.config(text=nuevo_texto)
        except Exception:
            pass

        # Fuente
        try:
            size = int(self.entry_size.get())
            family = self.combo_font.get().strip() or "Arial"

            props["font_size"] = size
            props["font_family"] = family

            nueva_fuente = font.Font(family=family, size=size)

            if tipo in ["Button", "Label", "Check", "Radio"]:
                self.widget_actual.config(font=nueva_fuente)
        except Exception:
            pass

        # Tamaño
        try:
            width = int(self.entry_width.get())
            height = int(self.entry_height.get())

            props["width"] = width
            props["height"] = height

            self.widget_actual.place(
                x=self.data_actual["x"],
                y=self.data_actual["y"],
                width=width,
                height=height
            )
        except Exception:
            pass

        self.generar_codigo()

    def cambiar_color_texto(self):
        if not self.widget_actual or not self.data_actual:
            return

        color = colorchooser.askcolor()[1]
        if not color:
            return

        self.data_actual["props"]["fg"] = color

        try:
            if self.data_actual["tipo"] in ["Button", "Label", "Check", "Radio"]:
                self.widget_actual.config(fg=color)
        except Exception:
            pass

        self.generar_codigo()

    def cambiar_color_fondo(self):
        if not self.widget_actual or not self.data_actual:
            return

        color = colorchooser.askcolor()[1]
        if not color:
            return

        self.data_actual["props"]["bg"] = color

        try:
            if self.data_actual["tipo"] in ["Button", "Label", "Frame"]:
                self.widget_actual.config(bg=color)
        except Exception:
            pass

        self.generar_codigo()

    def eliminar_componente(self):
        if not self.widget_actual:
            return

        for item in self.widgets:
            if item["widget"] == self.widget_actual:
                item["widget"].destroy()
                self.widgets.remove(item)
                break

        self.widget_actual = None
        self.data_actual = None

        self.entry_texto.delete(0, tk.END)
        self.entry_size.delete(0, tk.END)
        self.entry_width.delete(0, tk.END)
        self.entry_height.delete(0, tk.END)

        self.generar_codigo()

    # =========================
    # GENERAR CÓDIGO
    # =========================
    def generar_codigo(self):

        codigo = "import tkinter as tk\nfrom tkinter import ttk\n\n"
        codigo += "root = tk.Tk()\n"
        codigo += "root.geometry('900x600')\n\n"

        for i, item in enumerate(self.widgets):
            tipo = item["tipo"]
            x = item["x"]
            y = item["y"]
            props = item["props"]
            nombre = f"widget_{i}"

            config = []

            if props["text"] and tipo in ["Button", "Label", "Check", "Radio"]:
                config.append(f'text="{props["text"]}"')

            if props["bg"] and tipo in ["Button", "Label", "Frame"]:
                config.append(f'bg="{props["bg"]}"')

            if props["fg"] and tipo in ["Button", "Label", "Check", "Radio"]:
                config.append(f'fg="{props["fg"]}"')

            if tipo in ["Button", "Label", "Check", "Radio"]:
                config.append(
                    f'font=("{props["font_family"]}", {props["font_size"]})'
                )

            config_str = ", ".join(config)

            if tipo == "Button":
                codigo += f"{nombre} = tk.Button(root, {config_str})\n"

            elif tipo == "Label":
                codigo += f"{nombre} = tk.Label(root, {config_str})\n"

            elif tipo == "Entry":
                codigo += f"{nombre} = tk.Entry(root)\n"

            elif tipo == "Check":
                codigo += f"{nombre} = tk.Checkbutton(root, {config_str})\n"

            elif tipo == "Radio":
                codigo += f"{nombre} = tk.Radiobutton(root, {config_str})\n"

            elif tipo == "Combo":
                codigo += f"{nombre} = ttk.Combobox(root, values=['Opción 1', 'Opción 2'])\n"
                codigo += f"{nombre}.current(0)\n"

            elif tipo == "Text":
                codigo += f"{nombre} = tk.Text(root)\n"

            elif tipo == "Frame":
                frame_config = []
                if props["bg"]:
                    frame_config.append(f'bg="{props["bg"]}"')
                frame_config.append("relief='solid'")
                frame_config.append("borderwidth=1")
                codigo += f"{nombre} = tk.Frame(root, {', '.join(frame_config)})\n"

            codigo += (
                f"{nombre}.place(x={x}, y={y}, "
                f"width={props['width']}, height={props['height']})\n\n"
            )

        codigo += "root.mainloop()"

        self.text_codigo.delete("1.0", tk.END)
        self.text_codigo.insert(tk.END, codigo)

    # =========================
    # GUARDAR ARCHIVO
    # =========================
    def guardar_codigo_python(self):

        codigo = self.text_codigo.get("1.0", tk.END).strip()

        if not codigo:
            messagebox.showwarning("Aviso", "No hay código para guardar.")
            return

        # Ventana para elegir ruta
        ruta = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Archivos Python", "*.py")],
            title="Guardar archivo como"
        )

        # Si el usuario cancela
        if not ruta:
            return

        try:
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write(codigo)

            messagebox.showinfo("Éxito", "Archivo guardado correctamente")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar:\n{e}")
