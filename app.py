from flask import Flask, request
from helpers.endpoint import Endpoint


# Implementación de la APP
app = Flask(__name__)


# Rutas generales de endpoints
ENDPOINT_DEV = '/dev'
ENDPOINT_PROD = '/prod'


# Generación de endpoints
ep1 = Endpoint(route=ENDPOINT_DEV+'/test', methods=['POST'])


# Generación de rutas con los endpoints desarrollados
@app.route(ep1.route, methods=ep1.methods)
def devTest():
    # Entregar información sobre el endpoint en la terminal
    ep1.info()

    # Obtenemos el json y los datos del cuerpo de la solicitud
    json_content = request.json
    test = json_content.get("test")

    # Procesamos la respuesta
    if test is None :
        response = {'response': 'No se ha podido recuperar la data'}
    else :
        response = {'response': 'Se ha podido recuperar la data correctamente: ' + test}
    
    return response


# Función para iniciar la APP, está se ejecutá si el módulo fue ejecutado de forma directa
def start_app():
    app.run(host="0.0.0.0", port=8080, debug=True)


# Verificar la variable especial de python, si es el valor es '__main__', es porque se ejecutó el módulo
# app.py directamente.
if __name__ == "__main__":
    start_app()

