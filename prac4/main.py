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
import string


KEYWORDS_TO_FILES = {
    "driver": "drivers.txt",
    "team": "teams.txt",
    "car": "teams.txt",
    "circuit": "circuits.txt",
    "race": "history.txt",
    "championship": "history.txt",
    "Ferrari": "teams.txt",
    "Mercedes": "teams.txt",
    "Hamilton": "drivers.txt",
    "Verstappen": "drivers.txt",
    "Monza": "circuits.txt",
    "Silverstone": "circuits.txt",
    "DRS": "technology.txt",
    "ERS": "technology.txt",
    "Pirelli": "technology.txt",
    "rules": "rules.txt",
    "penalty": "rules.txt",
    "safety car": "rules.txt",
}


def extract_keywords(query, keywords_to_files):
    """
    Extrae palabras clave relevantes de la consulta del usuario.
    Limpia puntuación y hace la búsqueda ignorando mayúsculas y minúsculas.
    """
    # Eliminar puntuación de la consulta
    translator = str.maketrans("", "", string.punctuation)
    cleaned_query = query.translate(translator).lower()

    # Separar palabras y buscar palabras clave
    query_words = cleaned_query.split()
    relevant_keywords = [
        word for word in query_words if word in [k.lower() for k in keywords_to_files]
    ]

    # Mapear las palabras clave encontradas a su forma original
    return [k for k in keywords_to_files if k.lower() in relevant_keywords]


# Función para obtener contenido del fichero relevante
def get_context_from_files(keywords, knowledge_dir, keywords_to_files, debug=False):
    """
    Obtiene el contenido relevante de los ficheros en base a las palabras clave detectadas.
    """
    unique_files = set(keywords_to_files[keyword] for keyword in keywords)
    context = []

    if debug:
        print(f"\n[DEBUG] Searching in files: {', '.join(unique_files)}")

    for file in unique_files:
        file_path = os.path.join(knowledge_dir, file)
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                context.extend(f.readlines())
        else:
            print(f"Warning: File {file} not found in knowledge base.")

    return context


# Función principal
@click.command()
@click.argument("knowledge_dir", type=click.Path(exists=True))
@click.option(
    "--model", default="llama3.2:1b", help="Modelo de lenguaje a utilizar con Ollama."
)
@click.option(
    "--debug",
    is_flag=True,
    help="Habilita el modo de depuración para mostrar archivos consultados.",
)
def main(knowledge_dir, model, debug):
    """
    Aplicación principal del asistente virtual.
    """

    print("Virtual Assistant ready. Type 'exit' to quit.")

    # Bucle interactivo para recibir consultas del usuario
    while True:
        user_query = input("\nAsk your question (in English): ")
        if user_query.lower() in ["exit", "quit"]:
            print("Exiting Virtual Assistant. Goodbye!")
            break

        # Extraer palabras clave relevantes
        relevant_keywords = extract_keywords(user_query, KEYWORDS_TO_FILES)
        if relevant_keywords:
            if debug:
                print(f"\n[DEBUG] Keywords detected: {', '.join(relevant_keywords)}")
            context = get_context_from_files(
                relevant_keywords, knowledge_dir, KEYWORDS_TO_FILES, debug
            )
        else:
            if debug:
                print(
                    "\n[DEBUG] No relevant keywords found in your query. Using full knowledge base."
                )
            context = []
            if debug:
                print("\n[DEBUG] Searching in all files:")
            for file in os.listdir(knowledge_dir):
                if file.endswith(".txt"):
                    if debug:
                        print(f"[DEBUG] Reading file: {file}")
                    with open(os.path.join(knowledge_dir, file), "r") as f:
                        context.extend(f.readlines())

        messages = [
            {"role": "system", "content": "You are a Formula 1 knowledge assistant."},
            {
                "role": "system",
                "content": f"""answer the user's questions based only on the following information:\n{context}\n""",
            },
            {"role": "user", "content": user_query},
        ]

        # Enviamos la consulta al modelo usando Ollama
        try:
            print("\nProcessing your question...")
            response = ollama.chat(model=model, messages=messages)
            print(f"\nAssistant: {response["message"]["content"]}")
        except Exception as e:
            print(f"An error occurred: {e}")


# Funcion extra aun sin probar
def chain_of_thought(user_query, context):

    # Pasos intermedios de razonamiento
    reasoning_steps = [
        "Step 1: Identify the user's intent.",
        "Step 2: Locate relevant information in the provided context.",
        "Step 3: Analyze and synthesize the information to form a clear response.",
        "Step 4: Provide the reasoning process and the final answer.",
    ]

    # mensaje con el razonamiento
    reasoning_prompt = "\n".join(reasoning_steps)
    messages = [
        {"role": "system", "content": "You are a Formula 1 knowledge assistant."},
        {
            "role": "system",
            "content": f"Follow the Chain of Thought reasoning steps:\n{reasoning_prompt}\n"
            f"The relevant context is:\n{''.join(context)}",
        },
        {"role": "user", "content": user_query},
    ]

    # Generamos una respuesta usando el modelo Ollama
    try:
        response = ollama.chat(model="llama3.2:1b", messages=messages)
        return response["message"]["content"]
    except Exception as e:
        return f"An error occurred during reasoning: {e}"


if __name__ == "__main__":
    main()
