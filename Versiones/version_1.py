"""Malla curricular interactiva de la Universidad de Pamplona
Version 1.0
Autor: Sergio Ibarra"""
import pandas as pd

# Cambia esta ruta si el archivo no está en la misma carpeta
archivo = "C:\\Users\\sergi\\Desktop\\App Pensum\\Data\\Materias Mecatrónica.xlsx"


# Leer el Excel
df = pd.read_excel(archivo)

# Mostrar las primeras 10 filas
print("Primeras filas del archivo:")
print(df.head(10))

# Mostrar las columnas detectadas
print("\nColumnas en el archivo:")
print(df.columns.tolist())
