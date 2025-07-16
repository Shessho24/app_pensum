"""Pruebas de la interfaz de usuario sin fucionalidad completa, solo visualización"""

import pandas as pd
import customtkinter as ctk
from tkinter import messagebox
from functools import partial

#configurar apariencia de la interfaz
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue") 

#carga de colores institucionales
colores_institucionales = {"rojo":"#ad3333", "azul":"#003366", "gris":"#DADADA", "dorado":"#FFD700"}

#crear el scroll horizontal principal de la interfaz
class PensumApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Seguimiento Pensum - Ing. Mecatrónica")
        self.root.geometry("1200x800")
        
        # Configuración de tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variables
        self.materias = {}
        self.materias_aprobadas = set()
        self.creditos_acumulados = 0
        self.pensum_cargado = False
        
        # Interfaz
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame superior para controles
        #scroll horizontal
        self.scroll_horizontal = ctk.CTkScrollableFrame(self.root, width=1200, height=600, fg_color=colores_institucionales["gris"], orientation="horizontal")
        self.scroll_horizontal.pack(pady=10, padx=10, fill="both", expand=True)
        #espacios para los 10 semestres de izquierda a derecha dentro del scroll
        self.frames_semestre = {}
        for semestre in range(1, 11):
            frame_semestre = ctk.CTkFrame(self.scroll_horizontal, width=200, height=600, fg_color=colores_institucionales["gris"])
            frame_semestre.pack(side="left", padx=20, pady=20, fill="both", expand=True)
            self.frames_semestre[semestre] = frame_semestre
            
            # Etiqueta del semestre
            lbl_semestre = ctk.CTkLabel(frame_semestre, text=f"Semestre {semestre}", font=("Arial", 16), fg_color=colores_institucionales["azul"], text_color="white")
            lbl_semestre.pack(pady=10)
        # simular los botones de materias
        for semestre, frame in self.frames_semestre.items():
            for i in range(1, 6):
                btn_materia = ctk.CTkButton(
                    frame, 
                    text=f"Materia {i} - Sem {semestre}", 
                    width=180, 
                    height=40,
                    fg_color=colores_institucionales["rojo"],
                    text_color="white",
                    #al presionar el botón cambiará de color a dorado
                    command=partial(self.cambiar_color_materia, f"Materia {i} - Sem {semestre}")
                    
                )
                
                btn_materia.pack(pady=5)   
    def cambiar_color_materia(self, nombre_materia):
        # Cambiar el color del botón al ser presionado
        for semestre, frame in self.frames_semestre.items():
            for widget in frame.winfo_children():
                if isinstance(widget, ctk.CTkButton) and widget.cget("text") == nombre_materia:
                    widget.configure(fg_color=colores_institucionales["dorado"], text_color="black")
                    messagebox.showinfo("Materia Seleccionada", f"Has seleccionado: {nombre_materia}")
                    return


if __name__ == "__main__":
    root = ctk.CTk()
    app = PensumApp(root)
    root.mainloop()