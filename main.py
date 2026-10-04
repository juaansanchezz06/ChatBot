from groq_client import AIClient

def main():
    # Instanciar el cliente de IA desde nuestro módulo personalizado
    ai = AIClient()
    
    # Historial de conversación inicial con un mensaje de sistema opcional
    messages = [
        {"role": "system", "content": "Eres un asistente de IA útil, amable y conciso."}
    ]

    print("=" * 50)
    print("  Chatbot de Groq iniciado (Escribe 'salir' para terminar)")
    print("=" * 50)

    while True:
        # Capturar la entrada del usuario
        user_input = input("\nTú: ").strip()

        # Opción para finalizar el bucle
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("\n¡Hasta luego!")
            break

        # Si el usuario no escribe nada, continuar el bucle
        if not user_input:
            continue

        # Agregar el mensaje del usuario al historial
        messages.append({"role": "user", "content": user_input})

        try:
            # Obtener la respuesta de la IA llamando al método de la clase
            bot_reply = ai.get_response(messages)
            print(f"\nBot: {bot_reply}")

            # Guardar la respuesta del bot para mantener la memoria del chat
            messages.append({"role": "assistant", "content": bot_reply})

        except Exception as e:
            print(f"\nOcurrió un error en la comunicación con la API: {e}")

if __name__ == "__main__":
    main()
