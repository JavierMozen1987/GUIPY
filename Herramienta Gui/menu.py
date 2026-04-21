import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from ventana_principal import VentanaPrincipal
from PIL import Image, ImageTk
from explorador import crear_explorador
import os


class AppPrincipal:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CreaGUIPy")
        self.root.state("zoomed")
        self.root.configure(bg="white")

        self.contador_archivos = 0
        self.carpeta_actual = os.path.join(os.getcwd(), "archivos")
        os.makedirs(self.carpeta_actual, exist_ok=True)

        self.archivos_abiertos = {}

        self.crear_menu()

        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(fill="both", expand=True)

        self.panel_izq = tk.Frame(self.main_frame, width=220, bg="white")
        self.panel_izq.pack(side="left", fill="y")
        self.panel_izq.pack_propagate(False)

        self.lista_archivos = crear_explorador(self.panel_izq)
        self.lista_archivos.bind("<<ListboxSelect>>", self.al_seleccionar_en_explorador)

        linea = tk.Frame(self.main_frame, width=2, bg="#cccccc")
        linea.pack(side="left", fill="y")

        self.area_trabajo = tk.Frame(self.main_frame, bg="white")
        self.area_trabajo.pack(side="right", fill="both", expand=True)

        self.notebook_archivos = ttk.Notebook(self.area_trabajo)
        self.notebook_archivos.pack(fill="both", expand=True)
        self.notebook_archivos.bind("<Button-1>", self.click_en_pestana)

        self.label_fondo = None
        self.mostrar_fondo()
        self.actualizar_explorador()

    def crear_menu(self):
        menu_bar = tk.Menu(self.root)

        archivo_menu = tk.Menu(menu_bar, tearoff=0)
        archivo_menu.add_command(label="Nuevo archivo", command=self.abrir_disenador)
        archivo_menu.add_command(label="Abrir carpeta", command=self.abrir_carpeta)
        archivo_menu.add_command(label="Guardar archivo", command=self.guardar_codigo_python)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.root.quit)

        menu_bar.add_cascade(label="Archivo", menu=archivo_menu)
        self.root.config(menu=menu_bar)

    def mostrar_fondo(self):
        if len(self.notebook_archivos.tabs()) > 0:
            return

        try:
            ruta_base = os.path.dirname(__file__)
            ruta_imagen = os.path.join(ruta_base, "imagenes", "marcade_agua.png")

            imagen = Image.open(ruta_imagen).convert("RGBA")
            imagen = imagen.resize(
                (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
            )

            alpha = imagen.split()[3]
            alpha = alpha.point(lambda p: int(p * 1))
            imagen.putalpha(alpha)

            self.img_tk = ImageTk.PhotoImage(imagen)

            self.label_fondo = tk.Label(
                self.area_trabajo,
                image=self.img_tk,
                bg="white"
            )
            self.label_fondo.place(relwidth=1, relheight=1)

        except Exception as e:
            self.label_fondo = tk.Label(
                self.area_trabajo,
                text="CreaGUIPy",
                font=("Arial", 28, "bold"),
                fg="gray",
                bg="white"
            )
            self.label_fondo.place(relx=0.5, rely=0.5, anchor="center")
            print(f"No se pudo cargar la imagen de fondo: {e}")

    def ocultar_fondo(self):
        if self.label_fondo is not None:
            self.label_fondo.destroy()
            self.label_fondo = None

    def seleccionar_en_explorador(self, nombre_archivo):
        self.lista_archivos.selection_clear(0, tk.END)

        for i in range(self.lista_archivos.size()):
            texto = self.lista_archivos.get(i).replace("* ", "").strip()
            if texto == nombre_archivo:
                self.lista_archivos.selection_set(i)
                self.lista_archivos.activate(i)
                self.lista_archivos.see(i)
                break

    def actualizar_explorador(self, seleccionar_nombre=None):
        self.lista_archivos.delete(0, tk.END)

        nombres_mostrados = set()

        for _, data in self.archivos_abiertos.items():
            nombre = data["nombre_mostrar"]

            if data.get("modificado", False):
                nombre_visible = f"* {nombre}"
            else:
                nombre_visible = nombre

            if nombre not in nombres_mostrados:
                self.lista_archivos.insert(tk.END, nombre_visible)
                nombres_mostrados.add(nombre)

        if os.path.exists(self.carpeta_actual):
            for archivo in sorted(os.listdir(self.carpeta_actual)):
                ruta_completa = os.path.join(self.carpeta_actual, archivo)
                if os.path.isfile(ruta_completa) and archivo not in nombres_mostrados:
                    self.lista_archivos.insert(tk.END, archivo)
                    nombres_mostrados.add(archivo)

        if seleccionar_nombre:
            self.seleccionar_en_explorador(seleccionar_nombre)

    def abrir_disenador(self):
        self.ocultar_fondo()

        self.contador_archivos += 1
        nombre_temporal = f"Archivo{self.contador_archivos}"

        frame_archivo = tk.Frame(self.notebook_archivos, bg="white")
        self.notebook_archivos.add(frame_archivo, text=f"{nombre_temporal}   ✕")
        self.notebook_archivos.select(frame_archivo)

        tab_id = str(frame_archivo)

        ventana = VentanaPrincipal(
            frame_archivo,
            on_change=lambda tid=tab_id: self.marcar_archivo_modificado(tid)
        )

        ventana.nombre_archivo = nombre_temporal
        ventana.ruta_archivo = None

        self.archivos_abiertos[tab_id] = {
            "frame": frame_archivo,
            "ventana": ventana,
            "nombre_mostrar": nombre_temporal,
            "ruta": None,
            "guardado": False,
            "modificado": False
        }

        self.actualizar_titulo_pestana(tab_id)
        self.actualizar_explorador()

    def obtener_archivo_actual(self):
        pestaña_actual = self.notebook_archivos.select()
        if not pestaña_actual:
            return None
        return self.archivos_abiertos.get(pestaña_actual)

    def marcar_archivo_modificado(self, tab_id):
        archivo = self.archivos_abiertos.get(tab_id)
        if not archivo:
            return

        archivo["modificado"] = True
        self.actualizar_titulo_pestana(tab_id)
        self.actualizar_explorador()

    def actualizar_titulo_pestana(self, tab_id):
        archivo = self.archivos_abiertos.get(tab_id)
        if not archivo:
            return

        nombre = archivo["nombre_mostrar"]

        if archivo.get("modificado", False):
            titulo = f"*{nombre}   ✕"
        else:
            titulo = f"{nombre}   ✕"

        self.notebook_archivos.tab(archivo["frame"], text=titulo)

    def click_en_pestana(self, event):
        try:
            x, y = event.x, event.y
            elem = self.notebook_archivos.identify(x, y)

            if "label" not in elem:
                return

            tab_index = self.notebook_archivos.index(f"@{x},{y}")
            tab_id = self.notebook_archivos.tabs()[tab_index]

            bbox = self.notebook_archivos.bbox(tab_index)
            if not bbox:
                return

            tab_x, tab_y, tab_w, tab_h = bbox
            zona_cierre_inicio = tab_x + tab_w - 25

            if x >= zona_cierre_inicio:
                self.cerrar_archivo(tab_id)

        except Exception:
            pass

    def archivo_tiene_contenido(self, archivo):
        ventana = archivo["ventana"]

        if hasattr(ventana, "widgets") and len(ventana.widgets) > 0:
            return True

        if hasattr(ventana, "text_codigo"):
            texto = ventana.text_codigo.get("1.0", "end").strip()
            texto_base = (
                "import tkinter as tk\nfrom tkinter import ttk\n\n"
                "root = tk.Tk()\n"
                "root.geometry('900x600')\n\n"
                "root.mainloop()"
            )
            if texto and texto != texto_base:
                return True

        return False

    def cerrar_archivo(self, tab_id):
        archivo = self.archivos_abiertos.get(tab_id)
        if not archivo:
            return

        necesita_confirmacion = archivo.get("modificado", False) or (
            not archivo.get("guardado", False) and self.archivo_tiene_contenido(archivo)
        )

        if necesita_confirmacion:
            respuesta = messagebox.askyesnocancel(
                "Cerrar archivo",
                f"El archivo '{archivo['nombre_mostrar']}' tiene cambios sin guardar.\n\n"
                "¿Quieres guardarlo antes de cerrar?\n\n"
                "Sí = Guardar\n"
                "No = Cerrar sin guardar\n"
                "Cancelar = No cerrar"
            )

            if respuesta is None:
                return

            if respuesta is True:
                guardado = self.guardar_archivo_especifico(tab_id)
                if not guardado:
                    return

        self.notebook_archivos.forget(archivo["frame"])
        del self.archivos_abiertos[tab_id]

        self.actualizar_explorador()

        if not self.archivos_abiertos:
            self.mostrar_fondo()

    def abrir_carpeta(self):
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta")

        if carpeta:
            self.carpeta_actual = carpeta
            self.actualizar_explorador()

    def guardar_codigo_python(self):
        pestaña_actual = self.notebook_archivos.select()

        if not pestaña_actual:
            messagebox.showwarning("Aviso", "Primero debes crear un archivo nuevo.")
            return

        guardado = self.guardar_archivo_especifico(pestaña_actual)

        if guardado:
            messagebox.showinfo("Éxito", "Archivo guardado correctamente.")

    def guardar_archivo_especifico(self, tab_id):
        archivo_actual = self.archivos_abiertos.get(tab_id)

        if archivo_actual is None:
            return False

        ventana = archivo_actual["ventana"]
        ruta_actual = archivo_actual["ruta"]

        try:
            if ruta_actual is None:
                ruta = filedialog.asksaveasfilename(
                    initialdir=self.carpeta_actual,
                    initialfile=archivo_actual["nombre_mostrar"] + ".py",
                    defaultextension=".py",
                    filetypes=[("Archivos Python", "*.py")],
                    title="Guardar archivo como"
                )

                if not ruta:
                    return False
            else:
                ruta = ruta_actual

            ventana.guardar_codigo_python(ruta)

            nombre_real = os.path.basename(ruta)

            archivo_actual["ruta"] = ruta
            archivo_actual["guardado"] = True
            archivo_actual["modificado"] = False
            archivo_actual["nombre_mostrar"] = nombre_real

            ventana.nombre_archivo = nombre_real
            ventana.ruta_archivo = ruta

            self.actualizar_titulo_pestana(tab_id)
            self.actualizar_explorador(seleccionar_nombre=nombre_real)
            self.notebook_archivos.select(archivo_actual["frame"])
            ventana.canvas.focus_set()

            return True

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")
            return False

    # =========================
    # EXPLORADOR -> ABRIR ARCHIVO
    # =========================
    def al_seleccionar_en_explorador(self, event=None):
        seleccion = self.lista_archivos.curselection()
        if not seleccion:
            return

        nombre = self.lista_archivos.get(seleccion[0]).replace("* ", "").strip()
        self.abrir_o_seleccionar_archivo(nombre)

    def abrir_o_seleccionar_archivo(self, nombre_archivo):
        # 1. Si ya está abierto, solo seleccionarlo
        for tab_id, data in self.archivos_abiertos.items():
            if data["nombre_mostrar"] == nombre_archivo:
                self.notebook_archivos.select(data["frame"])
                data["ventana"].canvas.focus_set()
                self.seleccionar_en_explorador(nombre_archivo)
                return

        # 2. Si no existe físicamente, no hacer nada
        ruta = os.path.join(self.carpeta_actual, nombre_archivo)
        if not os.path.isfile(ruta):
            return

        # 3. Validar si se puede abrir en diseñador
        if not VentanaPrincipal.es_archivo_compatible(ruta):
            messagebox.showwarning(
                "Archivo no compatible",
                "Este archivo no se puede abrir en modo diseño.\n\n"
                "Solo se aceptan archivos hechos con tkinter/ttk y con la estructura que genera tu programa."
            )
            return

        # 4. Abrir en nueva pestaña
        self.ocultar_fondo()

        frame_archivo = tk.Frame(self.notebook_archivos, bg="white")
        self.notebook_archivos.add(frame_archivo, text=f"{nombre_archivo}   ✕")
        self.notebook_archivos.select(frame_archivo)

        tab_id = str(frame_archivo)

        ventana = VentanaPrincipal(
            frame_archivo,
            on_change=lambda tid=tab_id: self.marcar_archivo_modificado(tid)
        )

        ok = ventana.cargar_desde_archivo(ruta)

        if not ok:
            self.notebook_archivos.forget(frame_archivo)
            messagebox.showerror(
                "Error",
                "No se pudo reconstruir el archivo en el diseñador."
            )
            return

        ventana.nombre_archivo = nombre_archivo
        ventana.ruta_archivo = ruta

        self.archivos_abiertos[tab_id] = {
            "frame": frame_archivo,
            "ventana": ventana,
            "nombre_mostrar": nombre_archivo,
            "ruta": ruta,
            "guardado": True,
            "modificado": False
        }

        self.actualizar_titulo_pestana(tab_id)
        self.actualizar_explorador(seleccionar_nombre=nombre_archivo)
        ventana.canvas.focus_set()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AppPrincipal()
    app.run()