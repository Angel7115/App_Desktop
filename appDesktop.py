import tkinter as tk
import requests
import socket
from datetime import datetime
from flask import Flask, request, jsonify
import threading

# --- Configuración de Flask para la API RESTful ---
app = Flask(__name__)

# URL de MockAPI
MOCKAPI_URL = "https://66eafa8655ad32cda47b3666.mockapi.io/IoTCarStatus"

@app.route('/carstatus', methods=['POST'])
def create_car_status():
    """Crear un nuevo registro en MockAPI."""
    data = request.json  # Obtener datos del cuerpo de la solicitud
    response = requests.post(MOCKAPI_URL, json=data)  # Hacer POST a MockAPI
    return jsonify(response.json()), response.status_code

@app.route('/carstatus', methods=['GET'])
@app.route('/carstatus/<int:car_id>', methods=['GET'])
def get_car_status(car_id=None):
    """Leer registros de MockAPI."""
    if car_id:
        response = requests.get(f"{MOCKAPI_URL}/{car_id}")
    else:
        response = requests.get(MOCKAPI_URL)
    return jsonify(response.json()), response.status_code

@app.route('/carstatus/<int:car_id>', methods=['PUT'])
def update_car_status(car_id):
    """Actualizar un registro existente en MockAPI."""
    data = request.json
    response = requests.put(f"{MOCKAPI_URL}/{car_id}", json=data)
    return jsonify(response.json()), response.status_code

@app.route('/carstatus/<int:car_id>', methods=['DELETE'])
def delete_car_status(car_id):
    """Eliminar un registro de MockAPI."""
    response = requests.delete(f"{MOCKAPI_URL}/{car_id}")
    return jsonify({'message': 'El registro ha sido eliminado'}), response.status_code

# --- Código de la aplicación Desktop ---
def obtener_fecha_actual():
    """Obtener la fecha actual en formato legible."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def obtener_ip_local():
    """Obtener la IP local del equipo."""
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception as e:
        return "No se pudo obtener la IP"

def enviar_datos(status):
    """Enviar datos a la API Flask."""
    date = obtener_fecha_actual()
    ip_client = obtener_ip_local()
    name = "Angel Jafet"

    data = {
        "status": status,
        "date": date,
        "ipClient": ip_client,
        "name": name
    }

    try:
        # Hacer la solicitud POST al servidor Flask
        response = requests.post('http://localhost:5000/carstatus', json=data)
        if response.status_code == 201:
            mostrar_mensaje(f"Éxito: Registro {status} enviado", "green")
            mostrar_datos_enviados(data)
            mostrar_ultimo_comando(status)
        else:
            mostrar_mensaje(f"Error al enviar registro: {response.status_code}", "red")
    except Exception as e:
        mostrar_mensaje(f"Error de red: {str(e)}", "red")

def mostrar_mensaje(mensaje, color):
    """Mostrar un mensaje de éxito o error."""
    label_mensaje.config(text=mensaje, fg=color)

def mostrar_datos_enviados(data):
    """Mostrar los datos enviados en el recuadro."""
    for widget in frame_datos.winfo_children():
        widget.destroy()
    for key, value in data.items():
        tk.Label(frame_datos, text=f"{key}: {value}", bg="lightblue", anchor="w").pack(fill='x')

def mostrar_ultimo_comando(status):
    """Mostrar el último comando enviado."""
    label_ultimo_comando.config(text=f"Último comando enviado: {status}")

def boton_derecha():
    """Manejar el botón de derecha."""
    enviar_datos("derecha")

def boton_izquierda():
    """Manejar el botón de izquierda."""
    enviar_datos("izquierda")

def boton_adelante():
    """Manejar el botón de adelante."""
    enviar_datos("adelante")

def boton_atras():
    """Manejar el botón de atrás."""
    enviar_datos("atras")

def boton_detener():
    """Manejar el botón de detener."""
    enviar_datos("detener")

def obtener_ultimo_registro():
    """Obtener el último registro de MockAPI y mostrar su status."""
    try:
        response = requests.get(MOCKAPI_URL)
        if response.status_code == 200 and response.json():
            ultimo_registro = response.json()[-1]  # Obtener el último registro
            status = ultimo_registro['status']
            mostrar_ultimo_comando(status)  # Mostrar el último status en la interfaz
        else:
            mostrar_ultimo_comando("Ninguno")
    except Exception as e:
        mostrar_ultimo_comando("Error al obtener último registro")

# --- Interfaz gráfica de la aplicación Desktop ---
root = tk.Tk()
root.title("Inyector de Registros MockAPI")

# Botones de control
btn_derecha = tk.Button(root, text="Derecha", width=10, command=boton_derecha)
btn_izquierda = tk.Button(root, text="Izquierda", width=10, command=boton_izquierda)
btn_adelante = tk.Button(root, text="Adelante", width=10, command=boton_adelante)
btn_atras = tk.Button(root, text="Atrás", width=10, command=boton_atras)
btn_detener = tk.Button(root, text="Detener", width=10, command=boton_detener)

# Posicionamiento de botones en forma de cruceta
btn_adelante.grid(row=0, column=1, padx=10, pady=10)
btn_izquierda.grid(row=1, column=0, padx=10, pady=10)
btn_detener.grid(row=1, column=1, padx=10, pady=10)
btn_derecha.grid(row=1, column=2, padx=10, pady=10)
btn_atras.grid(row=2, column=1, padx=10, pady=10)

# Etiqueta para mostrar mensajes (éxito o error)
label_mensaje = tk.Label(root, text="", fg="green")
label_mensaje.grid(row=3, column=0, columnspan=3, pady=10)

# Crear un frame para mostrar los datos enviados
frame_datos = tk.Frame(root, bg="lightblue", padx=10, pady=10)
frame_datos.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="we")

# Etiqueta para mostrar el último comando enviado
label_ultimo_comando = tk.Label(root, text="Último comando enviado: Ninguno", fg="blue")
label_ultimo_comando.grid(row=5, column=0, columnspan=3, pady=10)

# Obtener el último registro al iniciar la aplicación
obtener_ultimo_registro()

# --- Ejecutar la aplicación Flask en un hilo separado ---
def iniciar_flask():
    """Iniciar el servidor Flask."""
    app.run(debug=True, use_reloader=False)

# Iniciar Flask en un hilo separado
flask_thread = threading.Thread(target=iniciar_flask)
flask_thread.daemon = True
flask_thread.start()

# Iniciar la interfaz gráfica
root.mainloop()
