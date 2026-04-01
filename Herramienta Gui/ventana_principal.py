import tkinter as tk
from tkinter import ttk
from componentes import *

class VentanaPrincipal:


    def __init__(self, parent):
        self.root = parent
        self.widget_actual = None
        self.crear_ui()

    def crear_ui(self):

        # =========================
        # CONTENEDOR PRINCIPAL
        # =========================
        main_paned = ttk.PanedWindow(self.root, orient="horizontal")
        main_paned.pack(fill="both", expand=True)

        # =========================
        # PANEL IZQUIERDO (EXPLORADOR)
        # =========================
        panel_izq = ttk.Frame(main_paned, width=200)
        main_paned.add(panel_izq)

        ttk.Label(panel_izq, text="Explorador", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=5)

        self.lista_archivos = tk.Listbox(panel_izq)
        self.lista_archivos.insert(0, "main.py")
        self.lista_archivos.pack(fill="both", expand=True, padx=5, pady=5)

        # =========================
        # PANEL CENTRAL (TABS)
        # =========================
        panel_centro = ttk.Frame(main_paned)
        main_paned.add(panel_centro, weight=1)

        tabs = ttk.Notebook(panel_centro)
        tabs.pack(fill="both", expand=True)

        # --- TAB DISEÑO ---
        frame_diseno = ttk.Frame(tabs)
        tabs.add(frame_diseno, text="Diseño")

        # Canvas
        self.canvas = tk.Frame(frame_diseno, bg="white", relief="solid", borderwidth=1)
        self.canvas.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)

        # --- TAB CÓDIGO ---
        frame_codigo = ttk.Frame(tabs)
        tabs.add(frame_codigo, text="Código")

        self.text_codigo = tk.Text(frame_codigo)
        self.text_codigo.pack(fill="both", expand=True)

        # =========================
        # PANEL DERECHO (COMPONENTES + PROPIEDADES)
        # =========================
        panel_der = ttk.Frame(main_paned, width=250)
        main_paned.add(panel_der)

        # Notebook derecho
        tabs_der = ttk.Notebook(panel_der)
        tabs_der.pack(fill="both", expand=True)

        # COMPONENTES
        tab_componentes = ttk.Frame(tabs_der)
        tabs_der.add(tab_componentes, text="Componentes")

        componentes = [
            ("Botón", "Button"),
            ("Label", "Label"),
            ("Input", "Entry")
        ]

        for nombre, tipo in componentes:
            btn = ttk.Button(tab_componentes, text=nombre,
                             command=lambda t=tipo: self.crear_componente(t))
            btn.pack(fill="x", padx=5, pady=5)

        # PROPIEDADES
        self.tab_propiedades = ttk.Frame(tabs_der)
        tabs_der.add(self.tab_propiedades, text="Propiedades")

        ttk.Label(self.tab_propiedades, text="Texto:").pack(pady=5)
        self.entry_texto = ttk.Entry(self.tab_propiedades)
        self.entry_texto.pack(fill="x", padx=5)

        ttk.Button(self.tab_propiedades, text="Aplicar",
                   command=self.aplicar_propiedades).pack(pady=5)

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

        else:
            return

        widget.place(x=50, y=50)

        widget.bind("<Button-1>", self.seleccionar)
        widget.bind("<B1-Motion>", self.arrastrar)

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

    # =========================
    # PROPIEDADES
    # =========================
    def aplicar_propiedades(self):
        if self.widget_actual:
            try:
                self.widget_actual.config(text=self.entry_texto.get())
            except:
                pass

 