"""Malla curricular interactiva de la Universidad de Pamplona
Version 1.0
Autor: Sergio Ibarra"""
import pandas as pd
p= "ali"
for i in range(len(p)):
    if p[i] == ',':
        prerequisitos = p.split(',')
    else:
        prerequisitos = [p]
print(prerequisitos)

class Materia:
    def __init__(self, nombre, codigo,semestre, creditos, prerequisitos, creditos_requeridos=0, Estado="Pendiente"):
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
        self.creditos_requeridos=int(creditos_requeridos) if creditos_requeridos else 0
        self.estado = Estado
    def puede_cursarse(self, materias_aprobadas, creditos_acumulados):
        if self.estado == "Aprobada":
            print(f"[INFO] {self.nombre} ya está aprobada")
            return False
        
        # Verificar créditos
        if self.creditos_requeridos > 0 and creditos_acumulados < self.creditos_requeridos:
            print(f"[REQ] Faltan créditos para {self.nombre} (Requiere: {self.creditos_requeridos})")
            return False
        
        # Verificar prerrequisitos
        for req in self.prerequisitos:
            if req not in materias_aprobadas:
                print(f"[REQ] Prerrequisito no cumplido: {req} para {self.nombre}")
                return False
        
        print(f"[OK] {self.nombre} puede cursarse")
        return True
class Pensum:
    def __init__(self):
        self.materias = []
        self.materias_aprobadas = set()
        self.creditos_acumulados = 0
    
    def cargar_pensum(self, ruta_archivo):
        
        try:
            df = pd.read_excel(ruta_archivo)
            for _, row in df.iterrows():
                materia = Materia(
                    nombre=row['Nombre'],
                    codigo=row['Código'],
                    semestre=row['Semestre'],
                    creditos=row['Créditos'],
                    prerequisitos=str(row['Prerrequisitos'] if pd.notna(row['Prerrequisitos']) else ""),
                    creditos_requeridos=row['Creditos_Requisitos'] if pd.notna(row['Creditos_Requisitos']) else 0,
                    Estado=row['Estado'] if pd.notna(row['Estado']) else "Pendiente"
                )
                self.materias.append(materia)
            print("Pensum cargado exitosamente.")
        except Exception as e:
            print(f"Error al cargar el pensum: {e}")

    def buscar_materia_por_codigo(self, codigo):
        for materia in self.materias:
            if materia.codigo == codigo:
                print(f"Materia encontrada: {materia.nombre} (Código: {materia.codigo})")
                return materia
        print("Materia no encontrada.")
        return None
    
    def mostrar_materias(self):
        for materia in self.materias:
            print(f"{materia.codigo} - {materia.nombre} (Semestre {materia.semestre}, Créditos: {materia.creditos}), Prerrequisitos: {materia.prerequisitos}, Créditos Requeridos: {materia.creditos_requeridos}, Estado: {materia.estado})")

Pensum_principal = Pensum()
Pensum_principal.cargar_pensum(r"C:\Users\sergi\Desktop\App Pensum\Data\Materias Mecatrónica.xlsx")
materia= Pensum_principal.buscar_materia_por_codigo("153002")
materia.puede_cursarse(Pensum_principal.materias_aprobadas, Pensum_principal.creditos_acumulados)
integral= Pensum_principal.buscar_materia_por_codigo("157401")
integral.puede_cursarse(Pensum_principal.materias_aprobadas, Pensum_principal.creditos_acumulados)