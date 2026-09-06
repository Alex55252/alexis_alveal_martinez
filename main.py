import json
import customtkinter as ctk
from tkinter import filedialog, messagebox

from views.forms import (
    render_datos_proyecto, render_radier, render_fierros,
    render_paredes, render_techumbre, render_electricidad, render_pintura
)
from views.summary import render_resumen

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class ConstructionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cubicador de obras")
        self.geometry("1240x800")

        self.info_proyecto = {
            "cliente": "",
            "obra": "",
            "fecha": "",
            "telefono": "",
            "email": "",
            "gastos_generales": 10.0,
            "utilidad": 15.0,
            "iva": 19.0,
            "modo_presupuesto": "rapido"
        }
        self.presupuesto_global = {}

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(self.sidebar, text="PARTIDAS DE OBRA", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 10))

        modulos = [
            ("0. Datos Proyecto", lambda: render_datos_proyecto(self), "#343a40"),
            ("1. Radier / Hormigón", lambda: render_radier(self), None),
            ("2. Enfierradura", lambda: render_fierros(self), None),
            ("3. Muros y Tabiquería", lambda: render_paredes(self), None),
            ("4. Techumbre / Cubiertas", lambda: render_techumbre(self), None),
            ("5. Red Eléctrica", lambda: render_electricidad(self), None),
            ("6. Pinturas y Acabados", lambda: render_pintura(self), None),
            ("7. Presupuesto Final", lambda: render_resumen(self), "#2b7a4b")
        ]

        for txt, cmd, col in modulos:
            btn = ctk.CTkButton(self.sidebar, text=txt, command=cmd)
            if col:
                btn.configure(fg_color=col)
            btn.pack(pady=3, padx=12, fill="x")

        f_acc = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        f_acc.pack(side="bottom", pady=15, padx=12, fill="x")

        ctk.CTkButton(f_acc, text="Nuevo Proyecto", fg_color="#6c757d", command=self.nuevo_proyecto).pack(pady=3, fill="x")
        ctk.CTkButton(f_acc, text="Guardar JSON", fg_color="#1f6aa5", command=self.guardar_json).pack(pady=3, fill="x")
        ctk.CTkButton(f_acc, text="Cargar JSON", fg_color="#495057", command=self.cargar_json).pack(pady=3, fill="x")

        # Main Panel
        self.main_frame = ctk.CTkScrollableFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        render_datos_proyecto(self)

    def clear_main(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def nuevo_proyecto(self):
        if messagebox.askyesno("Confirmar", "¿Crear nuevo presupuesto? Se perderán los datos no guardados."):
            self.presupuesto_global = {}
            self.info_proyecto = {
                "cliente": "",
                "obra": "",
                "fecha": "",
                "telefono": "",
                "email": "",
                "gastos_generales": 10.0,
                "utilidad": 15.0,
                "iva": 19.0,
                "modo_presupuesto": "rapido"
            }
            render_datos_proyecto(self)

    def guardar_json(self):
        if not self.presupuesto_global:
            messagebox.showwarning("Aviso", "No hay partidas calculadas para guardar.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"info_proyecto": self.info_proyecto, "presupuesto_global": self.presupuesto_global}, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("Éxito", "Guardado en JSON.")

    def cargar_json(self):
        path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.info_proyecto = data.get("info_proyecto", self.info_proyecto)
                self.presupuesto_global = data.get("presupuesto_global", {})
                messagebox.showinfo("Éxito", "Proyecto cargado.")
                render_resumen(self)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")

if __name__ == "__main__":
    app = ConstructionApp()
    app.mainloop()