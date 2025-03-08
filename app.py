from flask import Flask, request, jsonify
from helpers.endpoint import Endpoint

# Implementación de la APP
app = Flask(__name__)

# Rutas generales de endpoints
ENDPOINT_DEV = '/dev'
ENDPOINT_PROD = '/prod'

# Generación de endpoints
ep1 = Endpoint(route=ENDPOINT_DEV + '/test', methods=['POST'])

# Generación de rutas con los endpoints desarrollados
@app.route(ep1.route, methods=ep1.methods)
def devTest():
    """
    Endpoint para pruebas en el entorno de desarrollo.
    Recibe un JSON con una clave 'test' y responde con un mensaje.
    """
    # Entregar información sobre el endpoint en la terminal
    ep1.info()

    # Verificar si se recibió un JSON válido
    if not request.is_json:
        return jsonify({'error': 'Se esperaba una estructura de tipo JSON'}), 400

    # Obtenemos el json y los datos del cuerpo de la solicitud
    json_content = request.json
    test = json_content.get("test")

    # Procesamos la respuesta
    if test is None:
        return jsonify({'error': 'No es posible recuperar la data'}), 400
    else:
        response = {'response': 'Se ha podido recuperar la data correctamente: ' + test}

    return jsonify(response)

# Función para iniciar la APP, está se ejecutá si el módulo fue ejecutado de forma directa
def start_app():
    """
    Inicia la aplicación Flask.
    """
    app.run(host="0.0.0.0", port=8080, debug=True)

# Verificar la variable especial de python, si es el valor es '__main__', es porque se ejecutó el módulo
# app.py directamente.
if __name__ == "__main__":
    start_app()