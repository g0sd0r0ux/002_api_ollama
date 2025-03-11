import logging
from flask import Flask, request, jsonify
from langchain_ollama import OllamaLLM
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import PromptTemplate
from helpers.endpoint import Endpoint

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Implementación de la APP
app = Flask(__name__)
app.config['TIMEOUT'] = 300  # Aumentar el tiempo de espera

# Ruta de la base de datos vectorial
DB_PATH = "db"

# Configuración del modelo LLM que se va utilizar en Ollama
LLM = OllamaLLM(model="llama3", temperature=0.3, num_predict=512)

# Tipo de embedding para procesar leer y manejar la data
EMBEDDING = FastEmbedEmbeddings()

# Configuración del procesamiento de los archivos para crear los chunks
TEXT_SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False
)

# Plantilla del prompt para realizar la solicitud
RAW_PROMPT = PromptTemplate.from_template("""
    <s>[INST] Eres un asistente virtual diseñado para guiar y asesorar a los afiliados de la Caja de Compensación Los Andes en temas relacionados con el seguro de Renta Hospitalaria. Tu función principal es proporcionar información sobre coberturas, requisitos, trámites y cualquier otra consulta específica relacionada con este seguro. Si la consulta realizada no está vinculada con tu rol o con las pólizas de Renta Hospitalaria, debes responder de manera clara y educada: 'Lamento informarte que no estoy capacitado para responder esa pregunta. Sin embargo, estaré encantado de ayudarte con cualquier consulta relacionada con el seguro de Renta Hospitalaria.' [/INST] </s>
    [INST] {input}
            Context: {context}
            Answer: 
    [/INST]
""")

# Rutas generales de endpoints
ENDPOINT_DEV = '/dev'
ENDPOINT_PROD = '/prod'

# Generación de endpoints
EP1 = Endpoint(route=ENDPOINT_DEV + '/test', methods=['POST'])
EP2 = Endpoint(route=ENDPOINT_DEV + "/load/data", methods=['POST'])
EP3 = Endpoint(route=ENDPOINT_DEV + "/assistant", methods=['POST'])

# Generación de rutas con los endpoints desarrollados
@app.route(EP1.route, methods=EP1.methods)
def test():
    """
    Endpoint para pruebas en el entorno de desarrollo.
    Recibe un JSON con una clave 'test' y responde con el modelo LLM configurado previamente.
    """
    EP1.info()
    if not request.is_json:
        return jsonify({'error': 'Se esperaba una estructura de tipo JSON'}), 400
    json_body = request.json
    test = json_body.get("test")
    response = LLM.invoke(test)
    if response is None:
        return jsonify({'error': 'No es posible recuperar la data'}), 400
    return jsonify({"response": response})

@app.route(EP2.route, methods=EP2.methods)
def loadData():
    """
    Endpoint para cargar un archivo PDF y crear una base de datos vectorial.
    """
    # Revisamos si viene el archivo 'data'
    EP2.info()
    if "data" not in request.files:
        return jsonify({'error': 'No se ha proporcionado un archivo'}), 400
    pdf_data = request.files["data"]

    # Revisamos si el archivo es un pdf
    if not pdf_data.filename.endswith('.pdf'):
        return jsonify({'error': 'El archivo debe ser un PDF'}), 400
    pdf_name = pdf_data.filename
    pdf_path = "pdf/" + pdf_name
    pdf_data.save(pdf_path)
    logger.info(f"Cargando archivo: {pdf_name}")

    # Obtenemos los documentos y creamos los chunks
    pdf_plumber = PDFPlumberLoader(pdf_path)
    pdf_docs = pdf_plumber.load_and_split()
    logger.info(f"Documentos cargados: {len(pdf_docs)}")
    chunks = TEXT_SPLITTER.split_documents(pdf_docs)
    logger.info(f"Chunks Totales: {len(chunks)}")

    # Creamos la base de datos vectorial y la persistimos (la persistencia es automática)
    vector_db = Chroma.from_documents(documents=chunks, embedding=EMBEDDING, persist_directory=DB_PATH)
    response = {"status": "Archivo cargado correctamente", "filename": pdf_name, "total_docs": len(pdf_docs), "chunks": len(chunks)}
    return jsonify(response)

@app.route(EP3.route, methods=EP3.methods)
def assistant():
    """
    Endpoint para realizar consultas basadas en la base de datos vectorial.
    """

    # Revisamos si el cuerpo de la solicitud es un json
    EP3.info()
    if not request.is_json:
        return jsonify({'error': 'Se esperaba una estructura de tipo JSON'}), 400
    
    # Obtenemos el prompt del usuario y revisamos que tenga contenido
    json_body = request.json
    user_prompt = json_body.get("user_prompt")
    if not user_prompt:
        return jsonify({'error': 'No se ha proporcionado una consulta'}), 400
    logger.info(f"Consulta del usuario: {user_prompt}")

    try:
        # Leémos la base de datos lectorial, para responder acorde
        vector_db = Chroma(persist_directory=DB_PATH, embedding_function=EMBEDDING)
        
        # Configuramos el recuperador, además de de específicar el modelo LLM, con plantilla básica, para finalmente crear la cadena
        retrieve = vector_db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 3, "score_threshold": 0.1})
        document_chain = create_stuff_documents_chain(LLM, RAW_PROMPT)
        chain = create_retrieval_chain(retrieve, document_chain)

        # Realizamos la consulta con el contexto de la cadena y obtenemos la respuesta
        result = chain.invoke({"input": user_prompt})
        logger.info(f'Resultado de consulta: {result}')
        response = {"respuesta": result['answer'].replace("<s>[INST]", "").replace("[/INST]</s>", "").strip()}        
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error en el endpoint /assistant: {e}")
        return jsonify({'error': 'Ha ocurrido un error en el servidor'}), 500

# Función para iniciar la APP
def startApp():
    """
    Inicia la aplicación Flask.
    """
    app.run(host="0.0.0.0", port=8080, debug=True)

# Verificar la variable especial de python
if __name__ == "__main__":
    startApp()