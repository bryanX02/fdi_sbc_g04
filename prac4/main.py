# Implementacion de la practica 4 de SBC. El objetivo esta en implementar un
# asistente virtual, que emplee un TLL como interpretador de las bases.
# Basicamente le introduciremos la informacion al TLL Ollama para que tenga
# "memoria" y sea capaz de responder consultas en lenjuage natural tambien

# Hemos traducido nuestra base del conocimiento de la formula 1 al Ingles y su
# estructura es la del lenguaje natural.

import click
import os
from pathlib import Path
import ollama

# Función principal
@click.command()
@click.argument("knowledge_dir", type=click.Path(exists=True))
@click.option("--model", default="llama3.2:1b", help="Modelo de lenguaje a utilizar con Ollama.")
def main(knowledge_dir, model):
    """
    Aplicación principal del asistente virtual.
    """
    with open(knowledge_dir, 'r') as f:
        context = [linea for linea in f.readlines() if linea != "\n"]

    print("Virtual Assistant ready. Type 'exit' to quit.")

    # Bucle interactivo para recibir consultas del usuario
    while True:
        user_query = input("\nAsk your question (in English): ")
        if user_query.lower() in ["exit", "quit"]:
            print("Exiting Virtual Assistant. Goodbye!")
            break

        messages = [
            {
                'role': 'system' ,
                'content': 'You are a Formula 1 knowledge assistant.'
            },
            {
                'role': 'system' ,
                'content': f"""answer the user's questions based only on the following information:\n{context}\n"""
            },
            {
                'role': 'user' ,
                'content': user_query
            }

        ]
        

        # Enviamos la consulta al modelo usando Ollama
        try:
            print("\nProcessing your question...")
            response = ollama.chat(model=model, messages=messages)
            print(f"\nAssistant: {response["message"]["content"]}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

