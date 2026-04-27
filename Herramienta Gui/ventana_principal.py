import tkinter as tk
from tkinter import ttk, colorchooser, font, filedialog, messagebox
from componentes import *
import re
import copy
from PIL import Image, ImageTk
import os


class VentanaPrincipal:

    def __init__(self, parent, on_change=None):
        self.root = parent
        self.widget_actual = None
        self.data_actual = None
        self.widgets = []
        self.nombre_archivo = "archivo.py"
        self.ruta_archivo = None
        self.on_change = on_change
        self.iconos_componentes = {}

        # =========================
        # UNIONES / PRESENTACIÓN
        # =========================
        self.pantallas_unidas = []
        self.indice_presentacion = 0
        self.ventana_presentacion = None
        self.frame_preview = None
        self.lbl_titulo_presentacion = None

        self.historial = []
        self.historial_index = -1
        self.restaurando_historial = False

        self.crear_ui()
        self.generar_codigo()
        self.guardar_estado_historial()

    def crear_ui(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#ECE7E7")
        style.configure("TNotebook", background="#ECE7E7", borderwidth=0, tabmargins=[0, 0, 0, 0])

        style.configure(
            "TNotebook.Tab",
            background="#ECE7E7",
            padding=[10, 5],
            borderwidth=0,
            relief="flat"
        )

        style.map(
            "TNotebook.Tab",
            background=[("selected", "white"), ("!selected", "#ECE7E7")],
            relief=[("selected", "flat"), ("!selected", "flat")]
        )

        style.configure("Blanco.TFrame", background="white")

        contenedor_principal = tk.Frame(self.root, bg="white")
        contenedor_principal.pack(fill="both", expand=True)

        main_paned = ttk.PanedWindow(contenedor_principal, orient="horizontal")
        main_paned.pack(side="left", fill="both", expand=True)

        panel_der = ttk.Frame(contenedor_principal, width=300)
        panel_der.pack(side="right", fill="y")
        panel_der.pack_propagate(False)

        panel_centro = ttk.Frame(main_paned)
        main_paned.add(panel_centro, weight=1)

        tabs = ttk.Notebook(panel_centro)
        tabs.pack(fill="both", expand=True)

        linea_tabs = tk.Frame(panel_centro, height=1, bg="#cccccc")
        linea_tabs.pack(fill="x")

        frame_diseno = ttk.Frame(tabs, style="Blanco.TFrame")
        tabs.add(frame_diseno, text="Diseño")

        contenedor_ventana = tk.Frame(frame_diseno, bg="#ECE7E7")
        contenedor_ventana.place(relx=0.5, rely=0.5, anchor="center", width=720, height=480)

        ventana_mock = tk.Frame(
            contenedor_ventana,
            bg="white",
            relief="solid",
            borderwidth=1
        )
        ventana_mock.pack(fill="both", expand=True)

        barra_titulo = tk.Frame(
            ventana_mock,
            bg="#ECE7E7",
            height=30
        )
        barra_titulo.pack(fill="x")

        tk.Label(
            barra_titulo,
            text="Ventana de diseño",
            bg="#ECE7E7"
        ).pack(side="left", padx=10)

        frame_botones = tk.Frame(barra_titulo, bg="#ECE7E7")
        frame_botones.pack(side="right", padx=5)

        tk.Label(frame_botones, text="—", bg="#ECE7E7", width=3).pack(side="left")
        tk.Label(frame_botones, text="□", bg="#ECE7E7", width=3).pack(side="left")
        tk.Label(frame_botones, text="✕", bg="#ECE7E7", width=3).pack(side="left")

        self.canvas = tk.Frame(ventana_mock, bg="white")
        self.canvas.pack(fill="both", expand=True)

        frame_codigo = ttk.Frame(tabs)
        tabs.add(frame_codigo, text="Código")

        contenedor_codigo = tk.Frame(frame_codigo, bg="white")
        contenedor_codigo.pack(fill="both", expand=True)

        barra_codigo = tk.Frame(contenedor_codigo, bg="#F3F3F3", height=36)
        barra_codigo.pack(fill="x")
        barra_codigo.pack_propagate(False)

        tk.Label(
            barra_codigo,
            text="archivo.py",
            bg="#F3F3F3",
            fg="#333333",
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=10)

        self.btn_copiar_codigo = tk.Button(
            barra_codigo,
            text="📋 Copiar",
            bg="#F3F3F3",
            fg="#333333",
            activebackground="#E8E8E8",
            activeforeground="#111111",
            relief="flat",
            bd=0,
            font=("Segoe UI", 9),
            cursor="hand2",
            command=self.copiar_codigo
        )
        self.btn_copiar_codigo.pack(side="right", padx=8, pady=4)

        editor_container = tk.Frame(contenedor_codigo, bg="white")
        editor_container.pack(fill="both", expand=True)

        self.label_marca_codigo = None
        self.img_marca_codigo = None
        self.mostrar_marca_agua_codigo(editor_container)

        scroll_y_codigo = ttk.Scrollbar(editor_container, orient="vertical")
        scroll_x_codigo = ttk.Scrollbar(editor_container, orient="horizontal")

        self.text_codigo = tk.Text(
            editor_container,
            wrap="none",
            undo=False,
            bg="white",
            fg="#000000",
            insertbackground="black",
            selectbackground="#D7E9FF",
            selectforeground="black",
            relief="flat",
            bd=0,
            padx=12,
            pady=10,
            font=("Consolas", 11),
            yscrollcommand=scroll_y_codigo.set,
            xscrollcommand=scroll_x_codigo.set
        )

        scroll_y_codigo.config(command=self.text_codigo.yview)
        scroll_x_codigo.config(command=self.text_codigo.xview)

        scroll_y_codigo.pack(side="right", fill="y")
        scroll_x_codigo.pack(side="bottom", fill="x")
        self.text_codigo.pack(side="left", fill="both", expand=True)

        self.configurar_tags_codigo()

        tabs_der = ttk.Notebook(panel_der)
        tabs_der.pack(fill="both", expand=True)

        tab_componentes = tk.Frame(tabs_der, bg="white")
        tabs_der.add(tab_componentes, text="Componentes")

        contenedor_lateral = tk.Frame(tab_componentes, bg="white")
        contenedor_lateral.pack(fill="both", expand=True)

        frame_componentes_externo = tk.Frame(contenedor_lateral, bg="white", height=320)
        frame_componentes_externo.pack(fill="x", side="top")
        frame_componentes_externo.pack_propagate(False)

        canvas_componentes = tk.Canvas(
            frame_componentes_externo,
            bg="white",
            highlightthickness=0,
            bd=0
        )
        scrollbar_componentes = ttk.Scrollbar(
            frame_componentes_externo,
            orient="vertical",
            command=canvas_componentes.yview
        )
        canvas_componentes.configure(yscrollcommand=scrollbar_componentes.set)

        scrollbar_componentes.pack(side="right", fill="y")
        canvas_componentes.pack(side="left", fill="both", expand=True)

        frame_componentes = tk.Frame(canvas_componentes, bg="white", padx=8, pady=8)
        self.window_componentes = canvas_componentes.create_window(
            (0, 0),
            window=frame_componentes,
            anchor="nw"
        )

        def actualizar_scroll_componentes(event=None):
            canvas_componentes.configure(scrollregion=canvas_componentes.bbox("all"))

        def ajustar_ancho_componentes(event):
            canvas_componentes.itemconfig(self.window_componentes, width=event.width)

        frame_componentes.bind("<Configure>", actualizar_scroll_componentes)
        canvas_componentes.bind("<Configure>", ajustar_ancho_componentes)

        def on_mousewheel_componentes(event):
            canvas_componentes.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def bind_mousewheel_componentes(event):
            canvas_componentes.bind_all("<MouseWheel>", on_mousewheel_componentes)

        def unbind_mousewheel_componentes(event):
            canvas_componentes.unbind_all("<MouseWheel>")

        frame_componentes.bind("<Enter>", bind_mousewheel_componentes)
        frame_componentes.bind("<Leave>", unbind_mousewheel_componentes)

        tk.Label(
            frame_componentes,
            text="Componentes",
            bg="white",
            font=("Segoe UI", 10, "bold"),
            anchor="w"
        ).pack(fill="x", pady=(0, 6))

        linea_componentes = tk.Frame(frame_componentes, bg="#9F8484", height=2)
        linea_componentes.pack(fill="x", pady=(0, 10))

        componentes = [
            ("Botón", "Button", None),
            ("Label", "Label", None),
            ("Input", "Entry", None),
            ("CheckBox", "Check", None),
            ("RadioButton", "Radio", None),
            ("ComboBox", "Combo", None),
            ("TextArea", "Text", None),
            ("Frame", "Frame", None)
        ]

        for nombre, tipo, ruta_icono in componentes:
            icono = self.cargar_icono(ruta_icono) if ruta_icono else None

            btn = tk.Button(
                frame_componentes,
                text=nombre,
                image=icono,
                compound="left",
                anchor="center",
                justify="center",
                bg="white",
                activebackground="#F5F5F5",
                relief="solid",
                bd=1,
                padx=10,
                pady=8,
                font=("Segoe UI", 9),
                cursor="hand2",
                command=lambda t=tipo: self.crear_componente(t)
            )
            btn.image = icono
            btn.pack(fill="x", pady=4)

        separador_fijo = tk.Frame(contenedor_lateral, bg="#D0D0D0", height=2)
        separador_fijo.pack(fill="x", pady=(10, 0))

        frame_propiedades_externo = tk.Frame(contenedor_lateral, bg="white")
        frame_propiedades_externo.pack(fill="both", expand=True)

        canvas_props = tk.Canvas(
            frame_propiedades_externo,
            bg="white",
            highlightthickness=0,
            bd=0
        )
        scrollbar_props = ttk.Scrollbar(
            frame_propiedades_externo,
            orient="vertical",
            command=canvas_props.yview
        )
        canvas_props.configure(yscrollcommand=scrollbar_props.set)

        scrollbar_props.pack(side="right", fill="y")
        canvas_props.pack(side="left", fill="both", expand=True)

        frame_propiedades = tk.Frame(canvas_props, bg="white", padx=10, pady=10)
        self.window_propiedades = canvas_props.create_window(
            (0, 0),
            window=frame_propiedades,
            anchor="nw"
        )

        self._configurar_scroll_propiedades(canvas_props, frame_propiedades)

        tk.Label(
            frame_propiedades,
            text="Propiedades",
            bg="white",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(0, 5))

        linea = tk.Frame(frame_propiedades, bg="#9F8484", height=2)
        linea.pack(fill="x", pady=(0, 10))

        tk.Label(frame_propiedades, text="Texto:", bg="white").pack(anchor="w", pady=(0, 3))
        self.entry_texto = ttk.Entry(frame_propiedades)
        self.entry_texto.pack(fill="x", pady=(0, 8))
        self.entry_texto.bind("<Return>", self.aplicar_propiedades_evento)
        self.entry_texto.bind("<FocusOut>", self.aplicar_propiedades_evento)

        tk.Label(frame_propiedades, text="Tamaño letra:", bg="white").pack(anchor="w", pady=(0, 3))
        self.entry_size = ttk.Entry(frame_propiedades)
        self.entry_size.pack(fill="x", pady=(0, 8))
        self.entry_size.bind("<Return>", self.aplicar_propiedades_evento)
        self.entry_size.bind("<FocusOut>", self.aplicar_propiedades_evento)

        tk.Label(frame_propiedades, text="Fuente:", bg="white").pack(anchor="w", pady=(0, 3))
        self.combo_font = ttk.Combobox(
            frame_propiedades,
            values=["Arial", "Times New Roman", "Courier New", "Verdana", "Segoe UI"],
            state="readonly"
        )
        self.combo_font.pack(fill="x", pady=(0, 8))
        self.combo_font.set("Arial")
        self.combo_font.bind("<<ComboboxSelected>>", self.aplicar_propiedades_evento)
        self.combo_font.bind("<Return>", self.aplicar_propiedades_evento)

        tk.Label(frame_propiedades, text="Ancho:", bg="white").pack(anchor="w", pady=(0, 3))
        self.entry_width = ttk.Entry(frame_propiedades)
        self.entry_width.pack(fill="x", pady=(0, 8))
        self.entry_width.bind("<Return>", self.aplicar_propiedades_evento)
        self.entry_width.bind("<FocusOut>", self.aplicar_propiedades_evento)

        tk.Label(frame_propiedades, text="Alto:", bg="white").pack(anchor="w", pady=(0, 3))
        self.entry_height = ttk.Entry(frame_propiedades)
        self.entry_height.pack(fill="x", pady=(0, 8))
        self.entry_height.bind("<Return>", self.aplicar_propiedades_evento)
        self.entry_height.bind("<FocusOut>", self.aplicar_propiedades_evento)

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

        tk.Frame(frame_propiedades, bg="white", height=40).pack(fill="x")

        self.tab_uniones = ttk.Frame(tabs_der)
        tabs_der.add(self.tab_uniones, text="Uniones")

        self.crear_panel_uniones()

        self.root.bind_all("<Control-z>", self.deshacer)
        self.root.bind_all("<Control-Z>", self.deshacer)
        self.root.bind_all("<Delete>", self.eliminar_componente_evento)
        self.root.bind_all("<BackSpace>", self.eliminar_componente_evento)

    # ==================================================
    # MÓDULO DE UNIONES
    # ==================================================

    def crear_panel_uniones(self):
        contenedor = tk.Frame(self.tab_uniones, bg="white", padx=10, pady=10)
        contenedor.pack(fill="both", expand=True)

        tk.Label(
            contenedor,
            text="Uniones",
            bg="white",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w")

        tk.Label(
            contenedor,
            text="Agrega archivos de interfaces para crear una secuencia visual de navegación.",
            bg="white",
            fg="#555555",
            wraplength=260,
            justify="left",
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(4, 10))

        linea = tk.Frame(contenedor, bg="#9F8484", height=2)
        linea.pack(fill="x", pady=(0, 10))

        ttk.Button(
            contenedor,
            text="Agregar pantalla",
            command=self.agregar_pantalla_union
        ).pack(fill="x", pady=3)

        ttk.Button(
            contenedor,
            text="Quitar última pantalla",
            command=self.quitar_ultima_pantalla_union
        ).pack(fill="x", pady=3)

        ttk.Button(
            contenedor,
            text="Limpiar uniones",
            command=self.limpiar_uniones
        ).pack(fill="x", pady=3)

        ttk.Button(
            contenedor,
            text="▶ Run enlaces",
            command=self.run_uniones
        ).pack(fill="x", pady=(10, 3))

        tk.Label(
            contenedor,
            text="Flujo de pantallas:",
            bg="white",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(15, 5))

        frame_canvas = tk.Frame(contenedor, bg="white")
        frame_canvas.pack(fill="both", expand=True)

        self.canvas_uniones = tk.Canvas(
            frame_canvas,
            bg="#F7F7F7",
            highlightthickness=1,
            highlightbackground="#CCCCCC",
            height=260
        )
        self.canvas_uniones.pack(side="left", fill="both", expand=True)

        scroll_y = ttk.Scrollbar(
            frame_canvas,
            orient="vertical",
            command=self.canvas_uniones.yview
        )
        scroll_y.pack(side="right", fill="y")

        self.canvas_uniones.configure(yscrollcommand=scroll_y.set)

        self.dibujar_uniones()

    def agregar_pantalla_union(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar pantalla",
            filetypes=[("Archivos Python", "*.py")]
        )

        if not ruta:
            return

        if not self.es_archivo_compatible(ruta):
            messagebox.showerror(
                "Archivo no compatible",
                "El archivo seleccionado no parece haber sido creado con esta herramienta."
            )
            return

        nombre = os.path.basename(ruta)

        pantalla = {
            "nombre": nombre,
            "ruta": ruta
        }

        self.pantallas_unidas.append(pantalla)
        self.dibujar_uniones()

    def quitar_ultima_pantalla_union(self):
        if not self.pantallas_unidas:
            messagebox.showwarning(
                "Sin pantallas",
                "No hay pantallas para quitar."
            )
            return

        self.pantallas_unidas.pop()
        self.dibujar_uniones()

    def limpiar_uniones(self):
        if not self.pantallas_unidas:
            return

        respuesta = messagebox.askyesno(
            "Limpiar uniones",
            "¿Deseas eliminar todas las pantallas agregadas?"
        )

        if respuesta:
            self.pantallas_unidas.clear()
            self.dibujar_uniones()

    def dibujar_uniones(self):
        if not hasattr(self, "canvas_uniones"):
            return

        self.canvas_uniones.delete("all")

        if not self.pantallas_unidas:
            self.canvas_uniones.create_text(
                135,
                120,
                text="Aún no hay pantallas agregadas.\nPresiona 'Agregar pantalla'.",
                fill="#777777",
                font=("Segoe UI", 9),
                justify="center",
                width=220
            )
            return

        x = 25
        y = 25
        ancho = 210
        alto = 70
        espacio_y = 95

        for i, pantalla in enumerate(self.pantallas_unidas):
            y_actual = y + i * espacio_y

            self.canvas_uniones.create_rectangle(
                x,
                y_actual,
                x + ancho,
                y_actual + alto,
                fill="white",
                outline="#9F8484",
                width=2
            )

            self.canvas_uniones.create_text(
                x + 15,
                y_actual + 18,
                text=f"Pantalla {i + 1}",
                anchor="w",
                font=("Segoe UI", 9, "bold"),
                fill="#333333"
            )

            self.canvas_uniones.create_text(
                x + 15,
                y_actual + 43,
                text=pantalla["nombre"],
                anchor="w",
                font=("Segoe UI", 9),
                fill="#333333",
                width=180
            )

            if i < len(self.pantallas_unidas) - 1:
                self.canvas_uniones.create_line(
                    x + ancho / 2,
                    y_actual + alto,
                    x + ancho / 2,
                    y_actual + espacio_y,
                    arrow=tk.LAST,
                    width=2,
                    fill="#333333"
                )

        self.canvas_uniones.configure(
            scrollregion=self.canvas_uniones.bbox("all")
        )

    def run_uniones(self):
        if not self.pantallas_unidas:
            messagebox.showwarning(
                "Sin pantallas",
                "Primero agrega pantallas en la pestaña Uniones."
            )
            return

        self.indice_presentacion = 0

        self.ventana_presentacion = tk.Toplevel(self.root)
        self.ventana_presentacion.title("Run enlaces")
        self.ventana_presentacion.geometry("900x620")
        self.ventana_presentacion.configure(bg="#ECE7E7")

        barra = tk.Frame(self.ventana_presentacion, bg="#F3F3F3", height=45)
        barra.pack(fill="x")
        barra.pack_propagate(False)

        self.lbl_titulo_presentacion = tk.Label(
            barra,
            text="",
            bg="#F3F3F3",
            fg="#333333",
            font=("Segoe UI", 11, "bold")
        )
        self.lbl_titulo_presentacion.pack(side="left", padx=15)

        contenedor = tk.Frame(self.ventana_presentacion, bg="#ECE7E7")
        contenedor.pack(fill="both", expand=True, padx=20, pady=20)

        self.frame_preview = tk.Frame(
            contenedor,
            bg="white",
            relief="solid",
            borderwidth=1
        )
        self.frame_preview.pack(fill="both", expand=True)

        controles = tk.Frame(self.ventana_presentacion, bg="#ECE7E7", height=55)
        controles.pack(fill="x")
        controles.pack_propagate(False)

        ttk.Button(
            controles,
            text="Anterior",
            command=self.presentacion_anterior
        ).pack(side="left", padx=20, pady=10)

        ttk.Button(
            controles,
            text="Siguiente",
            command=self.presentacion_siguiente
        ).pack(side="left", padx=10, pady=10)

        ttk.Button(
            controles,
            text="Cerrar",
            command=self.ventana_presentacion.destroy
        ).pack(side="right", padx=20, pady=10)

        self.mostrar_pantalla_presentacion()

    def presentacion_siguiente(self):
        if self.indice_presentacion < len(self.pantallas_unidas) - 1:
            self.indice_presentacion += 1
            self.mostrar_pantalla_presentacion()

    def presentacion_anterior(self):
        if self.indice_presentacion > 0:
            self.indice_presentacion -= 1
            self.mostrar_pantalla_presentacion()

    def mostrar_pantalla_presentacion(self):
        for widget in self.frame_preview.winfo_children():
            widget.destroy()

        pantalla = self.pantallas_unidas[self.indice_presentacion]
        ruta = pantalla["ruta"]

        total = len(self.pantallas_unidas)
        actual = self.indice_presentacion + 1

        self.lbl_titulo_presentacion.config(
            text=f"Pantalla {actual} de {total}: {pantalla['nombre']}"
        )

        try:
            with open(ruta, "r", encoding="utf-8") as f:
                codigo = f.read()

            ventana_mock = tk.Frame(
                self.frame_preview,
                bg="white",
                relief="solid",
                borderwidth=1
            )
            ventana_mock.place(relx=0.5, rely=0.5, anchor="center", width=720, height=480)

            barra_titulo = tk.Frame(ventana_mock, bg="#ECE7E7", height=30)
            barra_titulo.pack(fill="x")

            tk.Label(
                barra_titulo,
                text=pantalla["nombre"],
                bg="#ECE7E7",
                fg="#333333",
                font=("Segoe UI", 9)
            ).pack(side="left", padx=10)

            frame_botones = tk.Frame(barra_titulo, bg="#ECE7E7")
            frame_botones.pack(side="right", padx=5)

            tk.Label(frame_botones, text="—", bg="#ECE7E7", width=3).pack(side="left")
            tk.Label(frame_botones, text="□", bg="#ECE7E7", width=3).pack(side="left")
            tk.Label(frame_botones, text="✕", bg="#ECE7E7", width=3).pack(side="left")

            area = tk.Frame(ventana_mock, bg="white")
            area.pack(fill="both", expand=True)

            patron_widget = re.compile(
                r'(widget_\d+)\s*=\s*'
                r'(tk\.Button|tk\.Label|tk\.Entry|tk\.Checkbutton|tk\.Radiobutton|ttk\.Combobox|tk\.Text|tk\.Frame)'
                r'\(root(.*?)\)\s*'
                r'(?:\n\1\.current\(0\))?'
                r'.*?\n\1\.place\(x=(\d+), y=(\d+), width=(\d+), height=(\d+)\)',
                re.DOTALL
            )

            for match in patron_widget.finditer(codigo):
                clase = match.group(2)
                config_str = match.group(3)

                x = int(match.group(4))
                y = int(match.group(5))
                width = int(match.group(6))
                height = int(match.group(7))

                texto = ""
                fg = ""
                bg = ""
                font_family = "Arial"
                font_size = 10

                m = re.search(r'text="([^"]*)"', config_str)
                if m:
                    texto = m.group(1)

                m = re.search(r'fg="([^"]*)"', config_str)
                if m:
                    fg = m.group(1)

                m = re.search(r'bg="([^"]*)"', config_str)
                if m:
                    bg = m.group(1)

                m = re.search(r'font=\("([^"]+)",\s*(\d+)\)', config_str)
                if m:
                    font_family = m.group(1)
                    font_size = int(m.group(2))

                fuente = (font_family, font_size)

                if clase == "tk.Button":
                    widget = tk.Button(area, text=texto, font=fuente)

                elif clase == "tk.Label":
                    widget = tk.Label(area, text=texto, font=fuente)

                elif clase == "tk.Entry":
                    widget = tk.Entry(area)

                elif clase == "tk.Checkbutton":
                    widget = tk.Checkbutton(area, text=texto, font=fuente)

                elif clase == "tk.Radiobutton":
                    widget = tk.Radiobutton(area, text=texto, font=fuente)

                elif clase == "ttk.Combobox":
                    widget = ttk.Combobox(area, values=["Opción 1", "Opción 2"])
                    widget.current(0)

                elif clase == "tk.Text":
                    widget = tk.Text(area)

                elif clase == "tk.Frame":
                    widget = tk.Frame(
                        area,
                        bg=bg if bg else "lightgray",
                        relief="solid",
                        borderwidth=1
                    )

                else:
                    continue

                try:
                    if fg and clase in ["tk.Button", "tk.Label", "tk.Checkbutton", "tk.Radiobutton"]:
                        widget.config(fg=fg)

                    if bg and clase in ["tk.Button", "tk.Label", "tk.Frame"]:
                        widget.config(bg=bg)
                except Exception:
                    pass

                widget.place(x=x, y=y, width=width, height=height)

        except Exception as e:
            tk.Label(
                self.frame_preview,
                text=f"No se pudo cargar la pantalla:\n{pantalla['nombre']}\n\n{e}",
                bg="white",
                fg="red",
                font=("Segoe UI", 10),
                justify="center"
            ).pack(expand=True)

    # ==================================================
    # FUNCIONES ORIGINALES
    # ==================================================

    def cargar_icono(self, ruta, size=(16, 16)):
        try:
            img = tk.PhotoImage(file=ruta)
            self.iconos_componentes[ruta] = img
            return img
        except Exception:
            return None

    def _configurar_scroll_propiedades(self, canvas, frame_interno):
        def actualizar_scroll(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def ajustar_ancho(event):
            canvas.itemconfig(self.window_propiedades, width=event.width)

        frame_interno.bind("<Configure>", actualizar_scroll)
        canvas.bind("<Configure>", ajustar_ancho)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def bind_mousewheel(event):
            canvas.bind_all("<MouseWheel>", on_mousewheel)

        def unbind_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")

        frame_interno.bind("<Enter>", bind_mousewheel)
        frame_interno.bind("<Leave>", unbind_mousewheel)

    def marcar_modificado(self):
        if self.on_change:
            self.on_change()

    def on_text_modified(self, event=None):
        if self.text_codigo.edit_modified():
            self.marcar_modificado()
            self.text_codigo.edit_modified(False)

    def guardar_estado_historial(self):
        if self.restaurando_historial:
            return

        estado = []
        for item in self.widgets:
            estado.append({
                "tipo": item["tipo"],
                "x": item["x"],
                "y": item["y"],
                "props": copy.deepcopy(item["props"])
            })

        if self.historial and self.historial[self.historial_index] == estado:
            return

        if self.historial_index < len(self.historial) - 1:
            self.historial = self.historial[:self.historial_index + 1]

        self.historial.append(estado)
        self.historial_index += 1

    def restaurar_estado(self, estado):
        self.restaurando_historial = True

        self.limpiar_canvas()

        for item in estado:
            tipo = item["tipo"]
            x = item["x"]
            y = item["y"]
            props = copy.deepcopy(item["props"])

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
                widget = tk.Frame(self.canvas, bg="lightgray", relief="solid", borderwidth=1)
            else:
                continue

            widget.place(
                x=x,
                y=y,
                width=props["width"],
                height=props["height"]
            )

            data = {
                "widget": widget,
                "tipo": tipo,
                "x": x,
                "y": y,
                "props": props
            }

            self.widgets.append(data)
            self.aplicar_estilo_inicial(data)

            try:
                if tipo in ["Button", "Label", "Check", "Radio"] and props.get("fg"):
                    widget.config(fg=props["fg"])
                if tipo in ["Button", "Label", "Frame"] and props.get("bg"):
                    widget.config(bg=props["bg"])
            except Exception:
                pass

            widget.bind("<Button-1>", self.seleccionar)
            widget.bind("<B1-Motion>", self.arrastrar)
            widget.bind("<ButtonRelease-1>", self.finalizar_arrastre)

        self.widget_actual = None
        self.data_actual = None

        self.entry_texto.delete(0, tk.END)
        self.entry_size.delete(0, tk.END)
        self.entry_width.delete(0, tk.END)
        self.entry_height.delete(0, tk.END)

        self.generar_codigo()
        self.restaurando_historial = False

    def deshacer(self, event=None):
        widget_con_foco = self.root.focus_get()

        if widget_con_foco == self.text_codigo:
            return "break"

        if self.historial_index <= 0:
            return "break"

        self.historial_index -= 1
        estado = self.historial[self.historial_index]
        self.restaurar_estado(estado)

        return "break"

    def eliminar_componente_evento(self, event=None):
        widget_con_foco = self.root.focus_get()

        if widget_con_foco in [
            self.entry_texto,
            self.entry_size,
            self.entry_width,
            self.entry_height,
            self.combo_font,
            self.text_codigo
        ]:
            return "break"

        if not self.widget_actual:
            return "break"

        self.eliminar_componente()
        return "break"

    def aplicar_propiedades_evento(self, event=None):
        self.aplicar_propiedades()

    @staticmethod
    def es_archivo_compatible(ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()

            imports = re.findall(
                r'^\s*(import\s+[^\n]+|from\s+[^\n]+\s+import\s+[^\n]+)',
                contenido,
                re.MULTILINE
            )

            permitidos = {
                "import tkinter as tk",
                "from tkinter import ttk"
            }

            for imp in imports:
                if imp.strip() not in permitidos:
                    return False

            if "root = tk.Tk()" not in contenido:
                return False

            return True

        except Exception:
            return False

    def limpiar_canvas(self):
        for item in self.widgets:
            try:
                item["widget"].destroy()
            except Exception:
                pass
        self.widgets.clear()
        self.widget_actual = None
        self.data_actual = None

    def cargar_desde_archivo(self, ruta):
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                codigo = f.read()

            self.limpiar_canvas()

            self.text_codigo.delete("1.0", tk.END)
            self.text_codigo.insert("1.0", codigo)
            self.text_codigo.edit_modified(False)

            patron_widget = re.compile(
                r'(widget_\d+)\s*=\s*(tk\.Button|tk\.Label|tk\.Entry|tk\.Checkbutton|tk\.Radiobutton|ttk\.Combobox|tk\.Text|tk\.Frame)\(root(.*?)\)\s*'
                r'(?:\n\1\.current\(0\))?'
                r'.*?\n\1\.place\(x=(\d+), y=(\d+), width=(\d+), height=(\d+)\)',
                re.DOTALL
            )

            for match in patron_widget.finditer(codigo):
                clase = match.group(2)
                config_str = match.group(3)
                x = int(match.group(4))
                y = int(match.group(5))
                width = int(match.group(6))
                height = int(match.group(7))

                tipo = None
                if clase == "tk.Button":
                    tipo = "Button"
                    widget = crear_boton(self.canvas)
                elif clase == "tk.Label":
                    tipo = "Label"
                    widget = crear_label(self.canvas)
                elif clase == "tk.Entry":
                    tipo = "Entry"
                    widget = crear_entry(self.canvas)
                elif clase == "tk.Checkbutton":
                    tipo = "Check"
                    widget = crear_checkbox(self.canvas)
                elif clase == "tk.Radiobutton":
                    tipo = "Radio"
                    widget = crear_radiobutton(self.canvas)
                elif clase == "ttk.Combobox":
                    tipo = "Combo"
                    widget = crear_combobox(self.canvas)
                elif clase == "tk.Text":
                    tipo = "Text"
                    widget = crear_textarea(self.canvas)
                elif clase == "tk.Frame":
                    tipo = "Frame"
                    widget = tk.Frame(self.canvas, bg="lightgray", relief="solid", borderwidth=1)
                else:
                    continue

                props = {
                    "text": "",
                    "fg": "",
                    "bg": "lightgray" if tipo == "Frame" else "",
                    "font_family": "Arial",
                    "font_size": 10,
                    "width": width,
                    "height": height
                }

                m = re.search(r'text="([^"]*)"', config_str)
                if m:
                    props["text"] = m.group(1)

                m = re.search(r'fg="([^"]*)"', config_str)
                if m:
                    props["fg"] = m.group(1)

                m = re.search(r'bg="([^"]*)"', config_str)
                if m:
                    props["bg"] = m.group(1)

                m = re.search(r'font=\("([^"]+)",\s*(\d+)\)', config_str)
                if m:
                    props["font_family"] = m.group(1)
                    props["font_size"] = int(m.group(2))

                widget.place(x=x, y=y, width=width, height=height)

                data = {
                    "widget": widget,
                    "tipo": tipo,
                    "x": x,
                    "y": y,
                    "props": props
                }

                self.widgets.append(data)
                self.aplicar_estilo_inicial(data)

                try:
                    if tipo in ["Button", "Label", "Check", "Radio"] and props["fg"]:
                        widget.config(fg=props["fg"])
                    if tipo in ["Button", "Label", "Frame"] and props["bg"]:
                        widget.config(bg=props["bg"])
                except Exception:
                    pass

                widget.bind("<Button-1>", self.seleccionar)
                widget.bind("<B1-Motion>", self.arrastrar)
                widget.bind("<ButtonRelease-1>", self.finalizar_arrastre)

            self.generar_codigo()
            self.text_codigo.edit_modified(False)
            self.historial = []
            self.historial_index = -1
            self.guardar_estado_historial()
            return True

        except Exception:
            return False

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
        widget.bind("<ButtonRelease-1>", self.finalizar_arrastre)

        self.generar_codigo()
        self.marcar_modificado()
        self.guardar_estado_historial()

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

    def seleccionar(self, event):
        self.widget_actual = event.widget
        self.data_actual = None
        self.root.focus_set()

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
        self.marcar_modificado()

    def aplicar_propiedades(self):
        if not self.widget_actual or not self.data_actual:
            return

        props = self.data_actual["props"]
        tipo = self.data_actual["tipo"]

        nuevo_texto = self.entry_texto.get()
        props["text"] = nuevo_texto

        try:
            if tipo in ["Button", "Label", "Check", "Radio"]:
                self.widget_actual.config(text=nuevo_texto)
        except Exception:
            pass

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
        self.marcar_modificado()
        self.guardar_estado_historial()

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
        self.marcar_modificado()
        self.guardar_estado_historial()

    def finalizar_arrastre(self, event=None):
        self.guardar_estado_historial()

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
        self.marcar_modificado()
        self.guardar_estado_historial()

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
        self.marcar_modificado()
        self.guardar_estado_historial()

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
                config.append(f'font=("{props["font_family"]}", {props["font_size"]})')

            config_str = ", ".join(config)

            if tipo == "Button":
                codigo += f"{nombre} = tk.Button(root"
                if config_str:
                    codigo += f", {config_str}"
                codigo += ")\n"

            elif tipo == "Label":
                codigo += f"{nombre} = tk.Label(root"
                if config_str:
                    codigo += f", {config_str}"
                codigo += ")\n"

            elif tipo == "Entry":
                codigo += f"{nombre} = tk.Entry(root)\n"

            elif tipo == "Check":
                codigo += f"{nombre} = tk.Checkbutton(root"
                if config_str:
                    codigo += f", {config_str}"
                codigo += ")\n"

            elif tipo == "Radio":
                codigo += f"{nombre} = tk.Radiobutton(root"
                if config_str:
                    codigo += f", {config_str}"
                codigo += ")\n"

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

        self.text_codigo.config(state="normal")
        self.text_codigo.delete("1.0", tk.END)
        self.text_codigo.insert("1.0", codigo)
        self.resaltar_codigo()
        self.text_codigo.config(state="disabled")

    def guardar_codigo_python(self, ruta):
        codigo = self.text_codigo.get("1.0", tk.END).strip()

        if not codigo:
            raise Exception("No hay código para guardar.")

        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(codigo)

    def configurar_tags_codigo(self):
        self.text_codigo.tag_configure("keyword", foreground="#0000FF")
        self.text_codigo.tag_configure("string", foreground="#A31515")
        self.text_codigo.tag_configure("comment", foreground="#008000")
        self.text_codigo.tag_configure("number", foreground="#098658")
        self.text_codigo.tag_configure("builtin", foreground="#267F99")
        self.text_codigo.tag_configure("class_name", foreground="#2B91AF")
        self.text_codigo.tag_configure("function_name", foreground="#795E26")

    def resaltar_codigo(self):
        for tag in self.text_codigo.tag_names():
            if tag in ["keyword", "string", "comment", "number", "builtin", "class_name", "function_name"]:
                self.text_codigo.tag_remove(tag, "1.0", tk.END)

        contenido = self.text_codigo.get("1.0", tk.END)

        keywords = [
            "import", "from", "as", "class", "def", "return", "if", "elif", "else",
            "try", "except", "for", "in", "while", "True", "False", "None", "with",
            "break", "continue", "pass"
        ]

        builtins = [
            "tk", "ttk", "Button", "Label", "Entry", "Frame", "Text", "Combobox"
        ]

        for palabra in keywords:
            patron = rf"\b{re.escape(palabra)}\b"
            for match in re.finditer(patron, contenido):
                inicio = f"1.0+{match.start()}c"
                fin = f"1.0+{match.end()}c"
                self.text_codigo.tag_add("keyword", inicio, fin)

        for palabra in builtins:
            patron = rf"\b{re.escape(palabra)}\b"
            for match in re.finditer(patron, contenido):
                inicio = f"1.0+{match.start()}c"
                fin = f"1.0+{match.end()}c"
                self.text_codigo.tag_add("builtin", inicio, fin)

        for match in re.finditer(r'"[^"\n]*"|\'[^\'\n]*\'', contenido):
            inicio = f"1.0+{match.start()}c"
            fin = f"1.0+{match.end()}c"
            self.text_codigo.tag_add("string", inicio, fin)

        for match in re.finditer(r"#.*", contenido):
            inicio = f"1.0+{match.start()}c"
            fin = f"1.0+{match.end()}c"
            self.text_codigo.tag_add("comment", inicio, fin)

        for match in re.finditer(r"\b\d+\b", contenido):
            inicio = f"1.0+{match.start()}c"
            fin = f"1.0+{match.end()}c"
            self.text_codigo.tag_add("number", inicio, fin)

        for match in re.finditer(r"\bclass\s+([A-Za-z_][A-Za-z0-9_]*)", contenido):
            inicio = f"1.0+{match.start(1)}c"
            fin = f"1.0+{match.end(1)}c"
            self.text_codigo.tag_add("class_name", inicio, fin)

        for match in re.finditer(r"\bdef\s+([A-Za-z_][A-Za-z0-9_]*)", contenido):
            inicio = f"1.0+{match.start(1)}c"
            fin = f"1.0+{match.end(1)}c"
            self.text_codigo.tag_add("function_name", inicio, fin)

    def copiar_codigo(self):
        codigo = self.text_codigo.get("1.0", tk.END).strip()
        self.root.clipboard_clear()
        self.root.clipboard_append(codigo)
        self.root.update()

        self.btn_copiar_codigo.config(text="✅ Copiado")
        self.root.after(1200, lambda: self.btn_copiar_codigo.config(text="📋 Copiar"))

    def mostrar_marca_agua_codigo(self, parent):
        try:
            ruta_base = os.path.dirname(__file__)
            ruta_imagen = os.path.join(ruta_base, "imagenes", "marcade_agua.png")

            imagen = Image.open(ruta_imagen).convert("RGBA")
            imagen = imagen.resize((420, 420))

            alpha = imagen.split()[3]
            alpha = alpha.point(lambda p: int(p * 1))
            imagen.putalpha(alpha)

            self.img_marca_codigo = ImageTk.PhotoImage(imagen)

            self.label_marca_codigo = tk.Label(
                parent,
                image=self.img_marca_codigo,
                bg="white",
                bd=0
            )
            self.label_marca_codigo.place(relx=0.5, rely=0.5, anchor="center")

        except Exception as e:
            self.label_marca_codigo = tk.Label(
                parent,
                text="CreaGUIPy",
                font=("Arial", 28, "bold"),
                fg="#E6E6E6",
                bg="white"
            )
            self.label_marca_codigo.place(relx=0.5, rely=0.5, anchor="center")
            print(f"No se pudo cargar la marca de agua del código: {e}")