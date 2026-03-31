import tkinter as tk
from ventana_principal import VentanaPrincipal

class MenuInicio:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CreaGUIPy")
        self.root.geometry("400x200")

        self.crear_menu()

    def crear_menu(self):
        menu_bar = tk.Menu(self.root)

        archivo_menu = tk.Menu(menu_bar, tearoff=0)
        archivo_menu.add_command(label="Nuevo archivo", command=self.nuevo_archivo)
        archivo_menu.add_command(label="Abrir archivo")
        archivo_menu.add_command(label="Guardar archivo")

        menu_bar.add_cascade(label="Archivo", menu=archivo_menu)

        self.root.config(menu=menu_bar)

    def nuevo_archivo(self):
        self.root.destroy()
        app = VentanaPrincipal()
        app.run()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MenuInicio()
    app.run()