"""Malla curricular interactiva de la Universidad de Pamplona
Version 1.0
Autor: Sergio Ibarra"""
import pandas as pd

# Cambia esta ruta si el archivo no está en la misma carpeta
archivo = "C:\\Users\\sergi\\Desktop\\App Pensum\\Data\\Materias Mecatrónica.xlsx"
class Materia:
    def __init__(self, nombre, codigo, creditos, prerequisitos=None, creditos_requeridos=0):
        self.nombre = nombre
        self.codigo = codigo
        self.creditos = creditos
        self.prerequisitos = prerequisitos if prerequisitos else []
        self.creditos_requeridos=creditos_requeridos if creditos_requeridos else 0

