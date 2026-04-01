import tkinter as tk
from ventana_principal import VentanaPrincipal

class AppPrincipal:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CreaGUIPy IDE")

        #  PANTALLA COMPLETA
        self.root.state("zoomed")  # Windows

        self.crear_menu()

        # CONTENEDOR DINÁMICO
        self.contenedor = tk.Frame(self.root)
        self.contenedor.pack(fill="both", expand=True)

    # =========================
    # MENÚ SUPERIOR
    # =========================
    def crear_menu(self):

        menu_bar = tk.Menu(self.root)

        archivo_menu = tk.Menu(menu_bar, tearoff=0)
        archivo_menu.add_command(label="Nuevo", command=self.abrir_disenador)
        archivo_menu.add_command(label="Salir", command=self.root.quit)

        menu_bar.add_cascade(label="Archivo", menu=archivo_menu)

        self.root.config(menu=menu_bar)

    # =========================
    # CAMBIAR VISTA
    # =========================
    def limpiar_contenedor(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def abrir_disenador(self):
        self.limpiar_contenedor()

        # 🔥 IMPORTANTE: pasar el contenedor
        self.ventana = VentanaPrincipal(self.contenedor)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AppPrincipal()
    app.run()