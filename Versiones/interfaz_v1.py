"""Mensaje de inicio del archivo: Este archivo contiene la implementación de la interfaz gráfica para el seguimiento del pensum de Ingeniería Mecatrónica, utilizando customtkinter y pandas para manejar los datos de las materias."""

import pandas as pd
import customtkinter as ctk
from tkinter import messagebox
from functools import partial
from tkinter import filedialog

escudo= r"C:\Users\sergi\Desktop\App Pensum\Data\escudounipamplona-_1_.ico"
#configurar apariencia de la interfaz
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
#poner escudo en la esquina superior izquierda


#carga de colores institucionales
colores_institucionales = {"rojo":"#ad3333", "azul":"#003366","dorado":"#FFD700", "gris":"#DADADA", }
creditos_acumulados= 0
#crear el scroll horizontal principal de la interfaz
class Materia:
    def __init__(self, nombre, codigo,semestre, creditos, prerequisitos, corequisitos, creditos_requeridos=0, Estado="Pendiente"):
        self.nombre = nombre
        self.codigo = str(codigo)
        self.semestre = semestre
        self.creditos = int(creditos)
        # separar prerequisitos por coma y posteriromente agregar a una lista
        if pd.isna(prerequisitos) or str(prerequisitos).strip() == "":
            self.prerequisitos = []
        else:
            # Normalizar a string y eliminar espacios
            prereq_str = str(prerequisitos).strip()
            # Separar por slash y eliminar elementos vacíos
            self.prerequisitos = [req.strip() for req in prereq_str.split('/') if req.strip()]
        # separar corequisitos por coma y posteriromente agregar a una lista    
        if pd.isna(corequisitos) or str(corequisitos).strip() == "":
            self.corequisitos = []
        else:
            # Normalizar a string y eliminar espacios
            coreq_str= str(corequisitos).strip()
            # Separar por slash y eliminar elementos vacíos
            self.corequisitos = [req.strip() for req in coreq_str.split('/') if req.strip()]
        self.creditos_requeridos=int(creditos_requeridos) if creditos_requeridos else 0
        self.estado = Estado
    def puede_cursarse(self, materias_aprobadas, creditos_acumulados, pensum, visitadas=None):
        if visitadas is None:
            visitadas = set()

        if self.codigo in visitadas:
            return False

        visitadas.add(self.codigo)

        if self.estado == "Aprobada":
            return False

        for cod in self.prerequisitos:
            if cod not in materias_aprobadas:
                return False

        if creditos_acumulados < self.creditos_requeridos:
            return False

        for cod in self.corequisitos:
            coreq = pensum.buscar_materia_por_codigo(cod)
            if coreq and coreq.estado != "Aprobada":
                if not coreq.puede_cursarse(materias_aprobadas, creditos_acumulados, pensum, visitadas):
                    return False

        return True


    def aprobar(self):
        self.estado = "Aprobada"
        # Aumentar créditos acumulados al aprobar

    def color_estado(self, materias_aprobadas, creditos_acumulados,pensum):
        if self.estado == "Aprobada":
            return colores_institucionales["dorado"]
        elif self.estado == "Pendiente":
            if self.puede_cursarse(materias_aprobadas, creditos_acumulados, pensum):
                return colores_institucionales["rojo"]
            else:
                return colores_institucionales["azul"]
        else:
            return colores_institucionales["gris"]
class Pensum:
    def __init__(self):
        self.materias = []
        self.materias_aprobadas = set()
        self.creditos_acumulados = 0
    
    def crear_pensum(self):
        ruta= cargar_pensum()
        df= pd.read_excel(ruta, sheet_name="Pensum", engine='openpyxl')
        try:
            for _, row in df.iterrows():
                materia = Materia(
                    nombre=row['Nombre'],
                    codigo=row['Código'],
                    semestre=row['Semestre'],
                    creditos=row['Créditos'],
                    prerequisitos=str(row['Prerrequisitos'] if pd.notna(row['Prerrequisitos']) else ""),
                    corequisitos=str(row['Corequisitos'] if pd.notna(row['Corequisitos']) else ""),
                    creditos_requeridos=row['Creditos_Requisitos'] if pd.notna(row['Creditos_Requisitos']) else 0,
                    Estado=row['Estado'] if pd.notna(row['Estado']) else "Pendiente"
                )
                self.materias.append(materia)
        except Exception as e:
            return e

    def buscar_materia_por_codigo(self, codigo):
        for materia in self.materias:
            if materia.codigo == codigo:
                return materia
        return None

def cargar_pensum():
    archivo_pensum = filedialog.askopenfilename(
        title="Seleccionar archivo de pensum",
        filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")]
    )
    if archivo_pensum:
        ruta_archivo = archivo_pensum
        return ruta_archivo



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
        frame_titulo = ctk.CTkFrame(self.root, width=1200, height=70, fg_color=colores_institucionales["azul"])
        frame_titulo.pack(side="top", fill="x")
        lbl_titulo = ctk.CTkLabel(frame_titulo, text="Seguimiento del Pensum de Ingeniería Mecatrónica", font=("Arial", 24), fg_color=colores_institucionales["azul"], text_color="white")
        lbl_titulo.pack(pady=10, fill="x")
        #mostrar creditos acumulados que pueden ser actualizados facilmente
        global creditos_acumulados 
        self.lbl_creditos = ctk.CTkLabel(frame_titulo, text=f"Créditos Acumulados: {self.creditos_acumulados}", font=("Arial", 16), fg_color=colores_institucionales["azul"], text_color="white")
        self.lbl_creditos.pack(side="right", padx=5)
        # Botón para cargar pensum


        self.btn_cargar = ctk.CTkButton(
            frame_titulo, 
            text="Cargar Pensum desde Excel",
            command=self.crear_scroll_horizontal,
            width=200,
            height=40,
            fg_color=colores_institucionales["rojo"],
            hover_color=colores_institucionales["gris"],
            text_color="white"
        )
        self.btn_cargar.pack(side="left", padx=5, pady=10)
        
        self.frame_explicacion = ctk.CTkFrame(self.root, width=1200, height=50, fg_color="transparent")
        self.frame_explicacion.pack(side="top", fill="x")
        lbl_explicacion = ctk.CTkLabel(self.frame_explicacion, text="Colores de las Materias:", font=("Arial", 16), text_color="white", fg_color="transparent")
        lbl_explicacion.pack()
        # Crear etiquetas de colores y explicaciones
        for color, descripcion in zip(colores_institucionales.values(), ["Pendiente", "No Cursable", "Aprobada"]):
            #descartar el color gris, ya que no es un estado de materia
            if color == colores_institucionales["gris"]:
                continue
            frame_color = ctk.CTkFrame(self.frame_explicacion, width=200, height=50, fg_color=color)
            #centrar los tres frames de colores
            frame_color.pack_propagate(False)  # No permitir que el frame cambie de tamaño
            frame_color.pack(side="left", padx=10, pady=5, fill="both")
            # Etiqueta de color en negrita
            lbl_color = ctk.CTkLabel(frame_color, text=f"{descripcion.capitalize()}", font=("Arial", 18, "bold"), text_color="white")
            lbl_color.pack(pady=10)
        # frame inferior para explicaciones o controles adicionales
        self.frame_inferior = ctk.CTkFrame(self.root, width=1200, height=100, fg_color=colores_institucionales["azul"])
        self.frame_inferior.pack(side="bottom", fill="x")
        lbl_inferior = ctk.CTkLabel(self.frame_inferior, text="Desarrollado por Sergio Ibarra", font=("Arial", 16), fg_color=colores_institucionales["azul"], text_color="white")   
        lbl_inferior.pack(pady=20)


    def crear_scroll_horizontal(self):
        
        self.pensum_principal = Pensum()
        self.pensum_principal.crear_pensum()

        if self.pensum_principal.materias:
            #verificar si ya hay un scroll horizontal creado, si lo hay no crear uno nuevo
            if hasattr(self, 'scroll_horizontal'):
                pass
            else:
            #scroll horizontal
                self.scroll_horizontal = ctk.CTkScrollableFrame(self.root, width=0, height=500, fg_color=colores_institucionales["gris"], orientation="horizontal")
                self.scroll_horizontal.pack(side="top", fill="both", expand=True)

            #espacios para los 10 semestres de izquierda a derecha dentro del scroll y segun pensum
            #verificar si ya hay frames de semestres creados, si los hay destruirlos
            if hasattr(self, 'frames_semestre'):
                for frame in self.frames_semestre.values():
                    frame.destroy()
            else:
                self.frames_semestre = {}
            cantidad_semestres = set(materia.semestre for materia in self.pensum_principal.materias)
            for semestre in sorted(cantidad_semestres):
                frame_semestre = ctk.CTkFrame(self.scroll_horizontal, width=200, height=500, fg_color="gray")
                frame_semestre.pack(side="left", padx=10, pady=10, fill="both", expand=True)
                self.frames_semestre[semestre] = frame_semestre
                # Etiqueta para el semestre
                lbl_semestre = ctk.CTkLabel(frame_semestre, text=f"Semestre {semestre}", font=("Arial", 25), text_color="white")
                lbl_semestre.pack(pady=10, fill="x")
        # Limpiar materias anteriores si las hay
            if hasattr(self, 'materias'):
                for btn in self.materias.values():
                    btn.destroy()
            else:
                self.materias = {}
            for materia in self.pensum_principal.materias:
                
                btn_materia = ctk.CTkButton(
                    self.frames_semestre[materia.semestre],

                    text=f"{(str(materia.nombre))}\n{materia.codigo} - {materia.creditos} Créditos",
                    font=("Calibri", 20),
                    command=partial(self.cursar_materia, materia.codigo),
                    width=180,
                    height=40,
                    fg_color=materia.color_estado(self.pensum_principal.materias_aprobadas, self.pensum_principal.creditos_acumulados, self.pensum_principal),
                    hover_color="Gray",
                    bg_color="transparent",
                    text_color="white"
                )
                btn_materia.pack(pady=5, padx=5, fill="both", expand=True)
                self.materias[materia.codigo] = btn_materia


    def cursar_materia(self, codigo_materia):
        materia = self.pensum_principal.buscar_materia_por_codigo(codigo_materia)
        if materia and materia.puede_cursarse(self.pensum_principal.materias_aprobadas, 
                                            self.pensum_principal.creditos_acumulados, 
                                            self.pensum_principal):
            materia.aprobar()
            self.pensum_principal.materias_aprobadas.add(materia.codigo)
            self.pensum_principal.creditos_acumulados += materia.creditos
            
            # Actualizar el botón de la materia aprobada
            self.materias[materia.codigo].configure(
                fg_color=colores_institucionales["dorado"], 
                text_color="black"
            )
            
            # Actualizar todos los otros botones
            for m in self.pensum_principal.materias:
                if m.codigo != materia.codigo:
                    self.materias[m.codigo].configure(
                        fg_color=m.color_estado(
                            self.pensum_principal.materias_aprobadas,
                            self.pensum_principal.creditos_acumulados,
                            self.pensum_principal
                        ),
                        
                    )

            # Actualizar créditos acumulados
            self.creditos_acumulados = self.pensum_principal.creditos_acumulados
            self.lbl_creditos.configure(text=f"Créditos Acumulados: {self.creditos_acumulados}")
            
            if self.creditos_acumulados >= 160:
                messagebox.showinfo("Felicidades", "¡Has completado los créditos necesarios para graduarte!")
        else:
            if materia.estado == "Aprobada":
                messagebox.showinfo("Materia Aprobada", f"{materia.nombre} ya ha sido aprobada.")
            else:
                requisitos = materia.prerequisitos if materia.prerequisitos else "ninguno"
                creditos_requeridos = materia.creditos_requeridos if materia.creditos_requeridos > 0 else "ninguno"
                materias_requeridas = []
                for i in requisitos:
                    variable_temporal= self.pensum_principal.buscar_materia_por_codigo(i)
                    if variable_temporal:
                        materias_requeridas.append(variable_temporal.nombre)
                requisitos = ", ".join(materias_requeridas) if materias_requeridas else requisitos
                # Validar si hay corequisitos
                if materia.corequisitos:    
                    materias_corequeridas = []
                    for j in materia.corequisitos:
                        variable_temporal= self.pensum_principal.buscar_materia_por_codigo(j)
                        if variable_temporal:
                            materias_corequeridas.append(variable_temporal.nombre)
                    corequisitos = ", ".join(materias_corequeridas) if materias_corequeridas else "ninguno"
                    messagebox.showwarning("No se puede cursar", f"No se puede cursar {materia.nombre}.\n Es necesario cursar los prerrequisitos: {requisitos}.\n Corequisitos: {corequisitos}.\n Créditos requeridos: {creditos_requeridos}.\n Créditos acumulados: {self.creditos_acumulados}.")
                else:
                    messagebox.showwarning("No se puede cursar", f"No se puede cursar {materia.nombre}.\n Es necesario cursar los prerrequisitos: {requisitos}.\n Créditos requeridos: {creditos_requeridos}.\n Créditos acumulados: {self.creditos_acumulados}.")
        # Actualizar créditos acumulados en la etiqueta    
if __name__ == "__main__":
    root = ctk.CTk()
    root.iconbitmap(escudo)  # Establecer el icono de la ventana
    app = PensumApp(root)
    root.mainloop()