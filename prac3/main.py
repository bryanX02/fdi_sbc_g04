from pathlib import Path
import click

# Implementar el sistema de interpretación de consultas al estilo de Wikidata Query Service
@click.command()
@click.argument("bases", nargs=-1, type=click.Path(exists=True))
def main(bases):
    # Variables
    bases_paths = [Path(base) for base in bases]  # Lista de archivos que contienen las bases de conocimiento

    # Cargar el contenido de los archivos en memoria
    contenido_bases = {}
    for base_path in bases_paths:
        with base_path.open("r", encoding="utf-8") as file:
            contenido_bases[base_path.name] = [line.strip() for line in file if line.strip()]

    # Iniciar la interfaz interactiva
    print("Lista de comandos:  'mostrar', 'salir'")
    
    while True:
        comando = input(">> ").strip().lower()
        
        if comando == "mostrar":
            for nombre, contenido in contenido_bases.items():
                print(f"\nContenido de {nombre}:")
                for linea in contenido:
                    print(linea)
                print("-" * 40)
        elif comando == "salir":
            print("Saliendo de la interfaz interactiva.")
            break
        else:
            print("Comando no reconocido. Usa 'mostrar' para ver el contenido o 'salir' para terminar.")

if __name__ == "__main__":
    main()


