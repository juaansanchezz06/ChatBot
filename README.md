# ChatBot con Groq

## Requisitos previos

Antes de comenzar, necesitas:

- Python instalado.
- Una cuenta en Groq.
- Una API Key de Groq.
- Un proyecto creado en tu equipo.

---

# 1. Generar una API Key

Crea una API Key gratuita desde el panel de control de Groq:

https://console.groq.com/keys

> **Importante:** nunca compartas tu API Key ni la subas a GitHub u otros repositorios públicos.

---

# 2. Configurar el entorno virtual y las credenciales

Crea y activa un entorno virtual en la raíz del proyecto.

## Crear el entorno virtual

```bash
python -m venv .venv
```

## Activar el entorno virtual

### Windows - PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows - CMD

```cmd
.venv\Scripts\activate.bat
```

### macOS / Linux

```bash
source .venv/bin/activate
```

> Si utilizas otro sistema operativo o una terminal diferente, utiliza el comando de activación correspondiente.

## Configurar las credenciales

Crea un archivo llamado `.env` en la raíz del proyecto.

El contenido debe tener el siguiente formato:

```env
GROQ_API_KEY=tu_api_key_aqui
```

Sustituye `tu_api_key_aqui` por la API Key que has generado en Groq.

### Seguridad

Por seguridad, asegúrate de incluir tanto el entorno virtual como el archivo `.env` en `.gitignore`.

Ejemplo de `.gitignore`:

```gitignore
.venv/
.env
__pycache__/
*.pyc
```

---

# 3. Instalación de dependencias

Con el entorno virtual activo, instala las bibliotecas necesarias:

```bash
pip install groq python-dotenv
```

También puedes instalar las dependencias utilizando el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

El contenido de `requirements.txt` es:

```txt
groq
python-dotenv
```

---

# 4. Documentación de archivos

La estructura básica del proyecto será:

```text
ChatBot/
│
├── .venv/
├── .env
├── .gitignore
├── requirements.txt
├── groq_client.py
└── main.py
```

---

# 5. `groq_client.py`

## Descripción general

El archivo `groq_client.py` es el módulo encargado de la comunicación directa con los servidores de Groq.

Su responsabilidad principal es encapsular:

- La autenticación mediante la API Key.
- La configuración del cliente de Groq.
- El envío del historial de conversación.
- La recepción de la respuesta del modelo.

La comunicación se organiza mediante una clase orientada a objetos llamada `AIClient`.

## Componentes y métodos

### `load_dotenv()`

La función `load_dotenv()` carga las variables definidas en el archivo `.env` en las variables de entorno del sistema (`os.environ`).

Esto permite acceder posteriormente a la API Key mediante:

```python
os.getenv("GROQ_API_KEY")
```

### Clase `AIClient`

La clase `AIClient` se encarga de gestionar la conexión con Groq.

Sus principales responsabilidades son:

1. Obtener la API Key.
2. Validar que la API Key exista.
3. Crear el cliente de Groq.
4. Enviar el historial conversacional.
5. Obtener y devolver la respuesta del modelo.

### Obtener la API Key

Extrae la variable `GROQ_API_KEY` del entorno:

```python
api_key = os.getenv("GROQ_API_KEY")
```

### Validar la API Key

Comprueba que la clave exista.

Si no se encuentra, se lanza una excepción para evitar ejecutar el programa sin las credenciales necesarias.

### Crear el cliente de Groq

Se instancia la clase `Groq` utilizando la API Key:

```python
Groq(api_key=api_key)
```

El cliente queda preparado para realizar peticiones al modelo configurado.

### Enviar el historial conversacional

La clase recibe una lista de mensajes que contiene el historial de la conversación.

Por ejemplo:

```python
messages = [
    {
        "role": "user",
        "content": "Hola, ¿cómo estás?"
    },
    {
        "role": "assistant",
        "content": "¡Hola! Estoy bien, ¿en qué puedo ayudarte?"
    }
]
```

Este historial permite que el modelo mantenga el contexto de la conversación.

### Obtener la respuesta

El cliente ejecuta la petición al modelo de Groq, recibe la respuesta generada y extrae el texto correspondiente.

Finalmente, devuelve únicamente el contenido textual de la respuesta.

---

# 6. Descripción de `main.py`

El archivo `main.py` contiene la lógica principal del chatbot.

Su funcionamiento se puede dividir en varias fases.

## 6.1 Inicialización

En esta fase se preparan las herramientas y variables necesarias antes de iniciar el bucle principal del chat.

Se importa e instancia el cliente de IA.

## 6.2 Instanciación

Creamos un objeto activo a partir de la clase `AIClient`:

```python
ai = AIClient()
```

Durante esta inicialización, Python lee la variable `GROQ_API_KEY` del archivo `.env` y deja preparada la conexión con Groq.

## 6.3 Historial conversacional

Se define la estructura base donde se almacenarán las preguntas y respuestas:

```python
messages = []
```

Al definir esta variable antes del bucle, nos aseguramos de que el chatbot tenga un contenedor donde ir añadiendo el contexto de la conversación.

Cada mensaje tendrá una estructura similar a:

```python
{
    "role": "user",
    "content": "Pregunta del usuario"
}
```

o:

```python
{
    "role": "assistant",
    "content": "Respuesta del chatbot"
}
```

---

# 7. Bucle de interacción

El chatbot funciona mediante un bucle que permite mantener una conversación con el usuario.

El flujo es el siguiente:

### 1. Capturar la entrada del usuario

Se utiliza `input()` para obtener el mensaje:

```python
user_input = input("Tú: ")
```

### 2. Evaluar comandos de salida

Se comprueba si el usuario ha escrito alguno de los comandos de salida:

```text
salir
exit
quit
```

Si el usuario introduce alguno de ellos, el programa finaliza.

### 3. Añadir el mensaje del usuario al historial

El mensaje se incorpora a la lista `messages`:

```python
messages.append({
    "role": "user",
    "content": user_input
})
```

### 4. Consultar a la IA

Se envía el historial completo al cliente:

```python
response = ai.get_response(messages)
```

El modelo utiliza el historial para mantener el contexto de la conversación.

### 5. Mostrar la respuesta

La respuesta generada se muestra en la terminal:

```python
print(f"Bot: {response}")
```

### 6. Guardar la respuesta en el historial

Finalmente, la respuesta del chatbot se incorpora también al historial:

```python
messages.append({
    "role": "assistant",
    "content": response
})
```

De esta forma, tanto las preguntas del usuario como las respuestas del chatbot quedan disponibles para las siguientes interacciones.

---

# 8. Gestión de errores

Las llamadas a la API pueden producir diferentes tipos de errores, por ejemplo:

- Problemas de conexión.
- Errores de autenticación.
- API Key incorrecta.
- Problemas con el servicio de Groq.
- Errores relacionados con la petición.

Por este motivo, las llamadas a la API deben estar protegidas mediante bloques `try-except`.

Ejemplo:

```python
try:
    response = ai.get_response(messages)
    print(f"Bot: {response}")

except Exception as e:
    print(f"Error: {e}")
```

Esto permite capturar los errores y mostrar información al usuario sin cerrar inesperadamente el programa.

---

# 9. Archivos de configuración

## `.env`

El archivo `.env` almacena de forma local y aislada la API Key de Groq.

Contenido:

```env
GROQ_API_KEY=tu_api_key_aqui
```

> **Nunca subas este archivo a GitHub ni a ningún repositorio público.**

## `.gitignore`

El archivo `.gitignore` indica a Git qué archivos y carpetas debe ignorar.

Ejemplo:

```gitignore
# Entorno virtual
.venv/

# Variables de entorno y credenciales
.env

# Archivos generados por Python
__pycache__/
*.pyc
```

Esto evita que el entorno virtual y las credenciales sensibles sean rastreados por Git.

## `requirements.txt`

Este archivo declara las dependencias principales del proyecto:

```txt
groq
python-dotenv
```

Para instalar todas las dependencias:

```bash
pip install -r requirements.txt
```

---

# 10. Resumen del funcionamiento

El flujo completo del chatbot es:

```text
                 ┌─────────────────────┐
                 │       Usuario       │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      main.py        │
                 │                     │
                 │  Captura el input   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Historial messages  │
                 │                     │
                 │ user + assistant    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     AIClient        │
                 │                     │
                 │  get_response()     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │       Groq API      │
                 │                     │
                 │  Modelo de lenguaje │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Respuesta del modelo│
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      main.py        │
                 │                     │
                 │ Muestra la respuesta│
                 │ y actualiza historial│
                 └─────────────────────┘
```

---

# 11. Estructura final del proyecto

Al finalizar la configuración, el proyecto debería tener una estructura similar a esta:

```text
ChatBot/
│
├── .venv/                  # Entorno virtual (NO subir a Git)
│
├── .env                    # API Key (NO subir a Git)
│
├── .gitignore              # Archivos ignorados por Git
│
├── requirements.txt        # Dependencias del proyecto
│
├── groq_client.py          # Cliente y comunicación con Groq
│
└── main.py                 # Lógica principal del chatbot
```

---

# 12. Comandos principales

## Crear el entorno virtual

```bash
python -m venv .venv
```

## Activar en Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

## Activar en Windows CMD

```cmd
.venv\Scripts\activate.bat
```

## Activar en macOS / Linux

```bash
source .venv/bin/activate
```

## Instalar dependencias

```bash
pip install groq python-dotenv
```

## Instalar desde `requirements.txt`

```bash
pip install -r requirements.txt
```

## Ejecutar el chatbot

```bash
python main.py
```

## Salir del chatbot

Escribe cualquiera de los siguientes comandos:

```text
salir
exit
quit
```

---

# 13. Resultado

Una vez configurado todo, el chatbot tendrá:

- Un entorno virtual independiente.
- Una API Key almacenada de forma segura en `.env`.
- Las dependencias necesarias instaladas.
- Un cliente `AIClient` encargado de comunicarse con Groq.
- Un historial conversacional para mantener el contexto.
- Un bucle interactivo para conversar desde la terminal.
- Gestión básica de errores.
- Una configuración preparada para utilizar Git sin exponer las credenciales.

---

# 14. Archivos principales

| Archivo | Función |
|---|---|
| `.env` | Almacena la API Key de Groq |
| `.gitignore` | Evita subir archivos sensibles o innecesarios |
| `requirements.txt` | Define las dependencias del proyecto |
| `groq_client.py` | Gestiona la comunicación con Groq |
| `main.py` | Contiene la lógica principal del chatbot |
| `.venv/` | Entorno virtual de Python |