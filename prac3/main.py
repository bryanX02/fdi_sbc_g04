from pathlib import Path
import click

# Implementar el sistema de interpretación de consultas al estilo de Wikidata Query Service
@click.command()
@click.argument("bases", nargs=-1, type=click.Path(exists=True))
@click.option("--script", type=click.Path(exists=True), help="Archivo con comandos a ejecutar en secuencia")
def main(bases, script):
    # Variables
    contenido_bases = {}  # Diccionario para almacenar el contenido de las bases de conocimiento

    # Función para cargar una base de conocimiento
    def cargar_base(ruta_base):
        base_path = Path(ruta_base)
        with base_path.open("r", encoding="utf-8") as file:
            contenido_bases[base_path.name] = [line.strip() for line in file if line.strip()]
        print(f"Base de conocimiento '{base_path.name}' cargada.")

    # Cargar los archivos iniciales
    for base in bases:
        cargar_base(base)

    # Función para ejecutar comandos
    def ejecutar_comando(comando):
        if comando.startswith("load "):
            # Cargar un archivo adicional
            _, ruta_base = comando.split(" ", 1)
            cargar_base(ruta_base.strip())
        elif comando == "mostrar":
            # Mostrar el contenido de las bases cargadas
            for nombre, contenido in contenido_bases.items():
                print(f"\nContenido de {nombre}:")
                for linea in contenido:
                    print(linea)
                print("-" * 40)
        elif comando == "salir":
            print("Saliendo de la interfaz interactiva.")
            return False
        else:
            print(f"Comando no reconocido: {comando}")
        return True

    # Ejecutar comandos desde el archivo si se proporciona
    if script:
        with open(script, "r", encoding="utf-8") as f:
            for line in f:
                comando = line.strip()
                if comando:
                    print(f">> {comando}")
                    if not ejecutar_comando(comando):
                        break
    else:
        # Interfaz interactiva para ingresar comandos manualmente
        print("Interfaz interactiva. Escribe 'mostrar' para ver el contenido, 'load <archivo>' para cargar más datos, o 'salir' para terminar.")
        while True:
            comando = input(">> ").strip()
            if not ejecutar_comando(comando):
                break

if __name__ == "__main__":
    main()



