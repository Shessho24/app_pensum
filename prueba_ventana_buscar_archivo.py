# Prueba de ventana para buscar archivos, siguiendo el estilo de la ventana de búsqueda de archivos de Windows.
# Este script utiliza customtkinter para crear una interfaz gráfica que permite al usuario seleccionar el pensum en un .xlsx y cargarlo en un DataFrame de pandas.
# Importar las bibliotecas necesarias

import pandas as pd
import customtkinter as ctk
from tkinter import messagebox
from functools import partial
import os
from tkinter import filedialog
def buscar_archivo_excel():
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de pensum",
        filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")]
    )
    if archivo:
        ruta= archivo
        print(f"Archivo seleccionado: {ruta}")
root = ctk.CTk()
root.title("Buscar Archivo de Pensum")
btn_cargar = ctk.CTkButton(root, text="Cargar Pensum desde Excel", command=buscar_archivo_excel)
btn_cargar.pack(pady=20, padx=20)

root.mainloop()