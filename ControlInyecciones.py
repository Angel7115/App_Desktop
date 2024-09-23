import tkinter as tk
from tkinter import ttk
import requests
import threading
import time
from datetime import datetime

# URL de MockAPI
MOCKAPI_URL = "https://66eafa8655ad32cda47b3666.mockapi.io/IoTCarStatus"

def obtener_ultimos_registros():
    """Obtener los últimos 10 registros de MockAPI."""
    try:
        response = requests.get(MOCKAPI_URL)
        if response.status_code == 200:
            registros = response.json()
            return registros[-10:]  # Obtener los últimos 10 registros
        else:
            return []
    except Exception as e:
        print(f"Error al consultar MockAPI: {str(e)}")
        return []

def convertir_fecha(timestamp):
    """Convertir fecha de formato timestamp a legible."""
    try:
        return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        return "Fecha inválida"

def actualizar_tabla():
    """Actualizar la tabla con los últimos 10 registros."""
    registros = obtener_ultimos_registros()

    # Limpiar la tabla antes de agregar los nuevos registros
    for row in tabla.get_children():
        tabla.delete(row)

    # Agregar registros a la tabla
    for registro in registros:
        # Convertir la fecha timestamp a un formato legible
        fecha_legible = convertir_fecha(registro["date"])
        # Insertar el registro en la tabla
        tabla.insert("", "end", values=(registro["id"], registro["name"], registro["status"], fecha_legible, registro["ipClient"]))

def actualizar_automatico():
    """Actualizar la tabla automáticamente cada 10 segundos."""
    actualizar_tabla()
    root.after(10000, actualizar_automatico)  # Ejecutar cada 10 segundos

# --- Interfaz gráfica ---
root = tk.Tk()
root.title("Control de Inyecciones MockAPI")
root.geometry("700x450")
root.configure(bg="#f0f0f0")

# Título de la aplicación
titulo = tk.Label(root, text="Últimos 10 registros de MockAPI", font=("Arial", 16, "bold"), bg="#f0f0f0")
titulo.pack(pady=10)

# Crear tabla
columns = ("ID", "Nombre", "Estado", "Fecha", "IP del Cliente")
tabla = ttk.Treeview(root, columns=columns, show="headings", height=10)
tabla.pack(pady=10)

# Definir encabezados
for col in columns:
    tabla.heading(col, text=col)
    tabla.column(col, anchor="center")

# Agregar barra de desplazamiento
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tabla.yview)
scrollbar.pack(side="right", fill="y")
tabla.config(yscrollcommand=scrollbar.set)

# Botón de actualización manual
btn_actualizar = tk.Button(root, text="Actualizar ahora", command=actualizar_tabla, bg="#4CAF50", fg="white", font=("Arial", 12))
btn_actualizar.pack(pady=10)

# Iniciar la actualización automática
root.after(10000, actualizar_automatico)

# Ejecutar la interfaz gráfica
root.mainloop()
