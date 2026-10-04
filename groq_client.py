import os
from dotenv import load_dotenv
from groq import Groq

# Cargar las variables del archivo .env a la memoria del sistema
load_dotenv()

class AIClient:
    """
    Clase encargada de gestionar la conexión y comunicación
    con los servicios de la API de Groq.
    """
    
    def __init__(self, model_name: str = "qwen/qwen3.8-27b"):
        # Obtener la API Key guardada en las variables de entorno
        self.api_key = os.environ.get("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError("Error: No se encontró la variable GROQ_API_KEY en el archivo .env")
            
        # Inicializar el objeto cliente de Groq con la clave autenticada
        self.client = Groq(api_key=self.api_key)
        self.model_name = model_name

    def get_response(self, messages: list) -> str:
        """
        Envía la lista de mensajes (historial) al modelo especificado
        y devuelve el texto de la respuesta devuelta por la IA.
        """
        chat_completion = self.client.chat.completions.create(
            messages=messages,
            model=self.model_name,
        )
        
        # Devolver el contenido del mensaje recibido
        return chat_completion.choices[0].message.content