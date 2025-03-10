from helpers.endpoint import Endpoint
from flask import Flask, request, jsonify
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import PromptTemplate

# Implementación de la APP
app = Flask(__name__)

# Ruta de la base de datos vectorial
DB_PATH = "db"

# Configuración del modelo LLM que se va utilizar en Ollama
LLM = Ollama(model="llama3", temperature=0.3, num_predict=512)

# Tipo de embedding para procesar leer y manejar la data
EMBEDDING = FastEmbedEmbeddings()

# Configuración del procesamiento de los archivos para crear los chunks
TEXT_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size= 1024, chunk_overlap=80, 
    length_function= len, is_separator_regex=False
)

# Plantilla del prompt para realizar la solicitud
RAW_PROMPT= PromptTemplate.from_template("""
    <s>[INST] Eres un asistente virtual diseñado para guiar y asesorar a los afiliados de la Caja de Compensación Los Andes en temas relacionados con el seguro de Renta Hospitalaria. Tu función principal es proporcionar información sobre coberturas, requisitos, trámites y cualquier otra consulta específica relacionada con este seguro. Si la consulta realizada no está vinculada con tu rol o con las pólizas de Renta Hospitalaria, debes responder de manera educada y amable: 'Lamento informarte que no estoy capacitado para responder esa pregunta. Sin embargo, estaré encantado de ayudarte con cualquier consulta relacionada con el seguro de Renta Hospitalaria.' [/INST] </s>
    [INST] {input}
            Context: {context}
            Answer: 
    [/INST]
"""
)

# Rutas generales de endpoints
ENDPOINT_DEV = '/dev'
ENDPOINT_PROD = '/prod'

# Generación de endpoints
ep1 = Endpoint(route=ENDPOINT_DEV + '/test', methods=['POST'])
ep2 = Endpoint(route=ENDPOINT_DEV + "/load/data", methods=['POST'])



# Generación de rutas con los endpoints desarrollados
@app.route(ep1.route, methods=ep1.methods)
def devTest():
    """
    Endpoint para pruebas en el entorno de desarrollo.
    Recibe un JSON con una clave 'test' y responde con el modelo
    LLM configurado previamente.
    """
    # Entregar información sobre el endpoint en la terminal
    ep1.info()

    # Verificar si se recibió un JSON válido
    if not request.is_json:
        return jsonify({'error': 'Se esperaba una estructura de tipo JSON'}), 400

    # Obtenemos el json y los datos del cuerpo de la solicitud
    json_body = request.json
    test = json_body.get("test")

    # Realizar consulta al modelo
    response = LLM.invoke(test)

    # Verificamos la respuesta
    if response is None:
        return jsonify({'error': 'No es posible recuperar la data'}), 400

    return jsonify({"response": response})



# Subir la información
@app.route(ep2.route, methods=ep2.methods)
def pdfPost():

    # Información del endpoint en la terminal
    ep2.info()

    # Recibimos el archivo con la llave 'data', construimos la ruta, y guardamos el archivo
    pdf_data = request.files["data"]
    pdf_name = pdf_data.filename
    pdf_path = "pdf/"+ pdf_name
    pdf_data.save(pdf_path)
    print(f"Cargando archivo: {pdf_name}")

    # Creamos una instancia de PDFPlumberLoader con la ruta del archivo
    pdf_plumber = PDFPlumberLoader(pdf_path) # Cargar archivo subido

    # Cargamos y dividimos los documentos
    pdf_docs = pdf_plumber.load_and_split()  # Split docs
    print(f"Documentos cargados: {len(pdf_docs)}") 

    # Creamos los chunks con la configuración de TEXT_SPLITTER
    chunks = TEXT_SPLITTER.split_documents(pdf_docs) # Chunks de texto
    print(f"Chunks Totales: {len(chunks)}")

    # Creación y almacenamiendo de bases vectoriales
    vector_db = Chroma.from_documents(
        documents= chunks,
        embedding= EMBEDDING,
        persist_directory= DB_PATH)
    vector_db.persist()

    # Ajuste de la respuesta
    response = {"status": "Archivo cargado correctamente",
               "filename": pdf_name,
               "total_docs": len(pdf_docs),
               "chunks": len(chunks)}
    
    return response



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