# API para Asistente de IA sobre Seguro de Renta Hospitalaria

Este proyecto consiste en el desarrollo de una API que configura un Asistente de IA para proporcionar información clara sobre cómo contratar el seguro de Renta Hospitalaria, incluyendo requisitos, coberturas, costos, beneficios y otros detalles relevantes. La API utiliza el modelo llama3 a través de Ollama y está diseñada para ser fácil de configurar y usar.

## Requisitos Previos

Antes de comenzar, asegúrate de tener lo siguiente:

1. WSL (Windows Subsystem for Linux):
- Si estás en Windows, instala WSL para tener un entorno Linux. Sigue [esta guía oficial de Microsoft](https://learn.microsoft.com/en-us/windows/wsl/install/) para instalarlo.
- Comando principal:
```bash
wsl --install
```
- Una vez instalado, abre una terminal de WSL (por defecto, se encuentra en un entorno similar a Ubuntu):
```bash
wsl.exe
```

2. Git
- Instala Git para clonar el repositorio.
- En WSL, ejecuta:
```bash
sudo apt update && sudo apt install git
```

3. Ollama
- Instala Ollama para usar modelos de lenguaje como `llama3`.
- En WSL, ejecuta:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

4. Modelo `llama3`
- Descarga el modelo `llama3` con Ollama.
- En WSL, ejecuta:
```bash
ollama pull llama3
```

5. Python 3 y pip
- Instala Python 3 y pip (gestor de paquetes de Python).
- En WSL, ejecuta:
```bash
sudo apt update && sudo apt install python3 python3-pip
```

6. Entorno Virtual
- Instala el módulo `venv` para crear entornos virtuales.
- En WSL, ejecuta:
```bash
sudo apt install python3-venv
```

## Instalación del Proyecto

Sigue estos pasos para configurar y ejecutar la API:

1. Configurar SSH (opcional pero recomendado):
- Si prefieres clonar el repositorio usando SSH, primero genera una clave SSH:
```bash
ssh-keygen -t ed25519 -C "tu-email@example.com"
```
- Presiona `Enter` para aceptar la ubicación predeterminada y configura una contraseña si lo deseas.
- Luego, copia tu clave pública:
```bash
cat ~/.ssh/id_ed25519.pub
```
- Finalmente, agrégala a tu cuenta de GitHub:
    1. Ve a GitHub SSH Keys.
    2. Haz clic en "New SSH Key".
    3. Pega la clave pública y guarda los cambios.

2. Clonar el Repositorio:
- Clona el repositorio en tu directorio de trabajo dentro de WSL usando SSH:
```bash
git clone git@github.com:g0sd0r0ux/002_api_ollama.git api-ollama
```
```bash
cd api-ollama
```

3. Crear y Activar el Entorno Virtual:
- Crea un entorno virtual para aislar las dependencias del proyecto.
- Ejecuta:
```bash
python3 -m venv myenv
```
```bash
source myenv/bin/activate
```
> **Nota**: Siempre activa el entorno virtual antes de trabajar en el proyecto.

4. Instalar Dependencias:
- Instala las dependencias necesarias desde el archivo `requirements.txt`.
- Ejecuta:
```bash
pip install -r requirements.txt
```

5. Ejecutar la API:
- Inicia la API con el siguiente comando:
```bash
python3 app.py
```
- La API estará disponible en `http://127.0.0.1:8080`.

## Uso de la API

La API tiene los siguientes endpoints:

1. `POST /dev/test`:
- Prueba el modelo `llama3` directamente.
- Ejemplo de solicitud:
```bash
curl -X POST "http://127.0.0.1:8080/dev/test" -d '{"test": "Hola, ¿cómo estás?"}'
```

2. `POST /dev/load/data`:
- Carga un archivo PDF para crear la base de datos vectorial.
- Ejemplo de solicitud:
```bash
curl -X POST -F "data=@ruta-proyecto/pdf/general_rules_02.pdf" http://127.0.0.1:8080/dev/load/data
```

3. `POST /dev/assistant`:
- Realiza consultas basadas en la base de datos vectorial.
- Ejemplo de solicitud:
```bash
curl -X POST "http://127.0.0.1:8080/dev/assistant" -d '{"user_prompt": "¿Cuáles son los requisitos para contratar el seguro?"}'
```

## Configuración Opcional

1. Visual Studio Code (VSCode):
- Si prefieres usar VSCode para editar el código, instala la extensión `Remote - WSL`.
- Esto te permitirá trabajar en el proyecto directamente desde WSL.

2. Postman:
- Para probar la API de manera más interactiva, puedes usar [Postman](https://www.postman.com/).
- Importa la colección de endpoints y realiza pruebas fácilmente.

