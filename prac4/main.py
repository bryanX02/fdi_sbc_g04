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

# Clase para manejar la base de conocimiento
class KnowledgeBaseManager:
    def __init__(self):
        self.knowledge_base = ""

    def load_base(self, directory):
        """
        Cargamos la base de conocimiento desde un directorio dado.
        Leemos todos los archivos .txt y concatenamos su contenido.
        """
        self.knowledge_base = ""  # Reiniciamos la base actual
        for file in Path(directory).glob("*.txt"):
            with open(file, "r", encoding="utf-8") as f:
                self.knowledge_base += f.read() + "\n"

    def get_context(self):
        """
        Retornamos el contenido de la base de conocimiento actual.
        """
        return self.knowledge_base

# Función principal
@click.command()
@click.argument("knowledge_dir", type=click.Path(exists=True))
@click.option("--model", default="llama2", help="Modelo de lenguaje a utilizar con Ollama.")
def main(knowledge_dir, model):
    """
    Aplicación principal del asistente virtual.
    """
    # Instanciamos el gestor de la base de conocimiento
    kb_manager = KnowledgeBaseManager()
    # Ahora cargamos la base de conocimiento desde el directorio proporcionado
    kb_manager.load_base(knowledge_dir)

    # Inicializamos el cliente de Ollama
    client = Ollama()

    print("Virtual Assistant ready. Type 'exit' to quit.")

    # Bucle interactivo para recibir consultas del usuario
    while True:
        user_query = input("\nAsk your question (in English): ")
        if user_query.lower() in ["exit", "quit"]:
            print("Exiting Virtual Assistant. Goodbye!")
            break

        # Preparamos el contexto para la consulta
        context = kb_manager.get_context()

        # Creamos el prompt para el modelo
        prompt = f"""
        You are a Formula 1 knowledge assistant. Answer the user's questions based on the following information:
        \n{context}\n
        User's question: {user_query}
        Provide a concise and accurate response.
        """

        # Enviamos la consulta al modelo usando Ollama
        try:
            print("\nProcessing your question...")
            response = client.generate(model=model, prompt=prompt)
            print(f"\nAssistant: {response}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

