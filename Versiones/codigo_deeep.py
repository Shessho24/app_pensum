import pandas as pd
import customtkinter as ctk
from tkinter import messagebox

class Materia:
    def __init__(self, codigo, nombre, semestre, creditos, requisitos, creditos_requeridos, estado="pendiente"):
        self.codigo = codigo
        self.nombre = nombre
        self.semestre = semestre
        self.creditos = creditos
        self.requisitos = requisitos.split('.') if pd.notna(requisitos) else []
        self.creditos_requeridos = int(creditos_requeridos) if pd.notna(creditos_requeridos) else 0
        self.estado = estado
        self.boton = None
    
    def puede_cursarse(self, materias_aprobadas, creditos_acumulados):
        if self.estado == "aprobada":
            return False
        
        # Verificar créditos requeridos
        if self.creditos_requeridos > 0 and creditos_acumulados < self.creditos_requeridos:
            return False
        
        # Verificar materias requisito
        for req in self.requisitos:
            if req not in materias_aprobadas:
                return False
                
        return True

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
        self.frame_controles = ctk.CTkFrame(self.root)
        self.frame_controles.pack(pady=10, padx=10, fill="x")
        
        # Botón para cargar pensum
        self.btn_cargar = ctk.CTkButton(
            self.frame_controles, 
            text="Cargar Pensum desde Excel",
            command=self.cargar_pensum
        )
        self.btn_cargar.pack(side="left", padx=5)
        
        # Etiqueta para créditos
        self.lbl_creditos = ctk.CTkLabel(
            self.frame_controles, 
            text="Créditos acumulados: 0"
        )
        self.lbl_creditos.pack(side="right", padx=5)
        
        # Frame principal para la malla curricular
        self.frame_malla = ctk.CTkScrollableFrame(self.root)
        self.frame_malla.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Inicializar frames por semestre
        self.frames_semestre = {}
        for sem in range(1, 11):  # Asumiendo 10 semestres
            frame = ctk.CTkFrame(self.frame_malla)
            frame.pack(fill="x", pady=5)
            lbl = ctk.CTkLabel(frame, text=f"Semestre {sem}", font=("Arial", 14, "bold"))
            lbl.pack(side="left", padx=10)
            self.frames_semestre[sem] = frame
    
    def cargar_pensum(self):
        # Aquí deberías implementar la lógica para seleccionar un archivo Excel
        # Por ahora usaremos un ejemplo simulado
        
        try:
            # Simulamos la carga de datos (en tu caso usarías pd.read_excel)
            data = {
                "Código": ["168417", "168428", "168435"],
                "Nombre": ["Cálculo I", "Física I", "Programación"],
                "Semestre": [1, 1, 1],
                "Créditos": [4, 4, 3],
                "Requisitos": [None, None, None],
                "Créditos Requeridos": [None, None, None]
            }
            df = pd.DataFrame(data)
            
            # Procesar datos
            self.procesar_datos_pensum(df)
            self.pensum_cargado = True
            messagebox.showinfo("Éxito", "Pensum cargado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el pensum: {str(e)}")
    
    def procesar_datos_pensum(self, df):
        # Limpiar datos anteriores
        self.materias = {}
        self.materias_aprobadas = set()
        self.creditos_acumulados = 0
        
        # Procesar cada materia
        for _, row in df.iterrows():
            materia = Materia(
                row["Código"],
                row["Nombre"],
                row["Semestre"],
                row["Créditos"],
                row["Requisitos"],
                row["Créditos Requeridos"]
            )
            
            self.materias[materia.codigo] = materia
            
            # Crear botón para la materia
            self.crear_boton_materia(materia)
    
    def crear_boton_materia(self, materia):
        frame_semestre = self.frames_semestre.get(materia.semestre)
        if not frame_semestre:
            return
            
        btn = ctk.CTkButton(
            frame_semestre,
            text=f"{materia.codigo}\n{materia.nombre}\nCréditos: {materia.creditos}",
            width=150,
            height=80,
            command=lambda: self.toggle_materia(materia.codigo)
        )
        btn.pack(side="left", padx=5, pady=5)
        materia.boton = btn
        
        # Configurar color inicial
        self.actualizar_estado_boton(materia)
    
    def toggle_materia(self, codigo):
        if not self.pensum_cargado:
            return
            
        materia = self.materias.get(codigo)
        if not materia:
            return
            
        if materia.estado == "aprobada":
            materia.estado = "pendiente"
            self.materias_aprobadas.discard(codigo)
            self.creditos_acumulados -= materia.creditos
        else:
            if materia.puede_cursarse(self.materias_aprobadas, self.creditos_acumulados):
                materia.estado = "aprobada"
                self.materias_aprobadas.add(codigo)
                self.creditos_acumulados += materia.creditos
            else:
                messagebox.showwarning("No disponible", "No cumples los requisitos para esta materia")
        
        self.actualizar_estado_boton(materia)
        self.actualizar_todas_materias()
        self.lbl_creditos.configure(text=f"Créditos acumulados: {self.creditos_acumulados}")
    
    def actualizar_estado_boton(self, materia):
        if materia.estado == "aprobada":
            materia.boton.configure(fg_color="green", hover_color="dark green")
        elif materia.puede_cursarse(self.materias_aprobadas, self.creditos_acumulados):
            materia.boton.configure(fg_color="#1f538d", hover_color="#14375e")  # Azul estándar
        else:
            materia.boton.configure(fg_color="gray", hover_color="dark gray")
    
    def actualizar_todas_materias(self):
        for codigo, materia in self.materias.items():
            self.actualizar_estado_boton(materia)

if __name__ == "__main__":
    root = ctk.CTk()
    app = PensumApp(root)
    root.mainloop()