from pathlib import Path
import click
from Consultas import realizar_consulta
from GestorBase import *

# Implementar el sistema de interpretación de consultas al estilo de Wikidata Query Service
@click.command()
@click.argument("base")
@click.option("--script", type=click.Path(exists=True), help="Archivo con comandos a ejecutar en secuencia")
def main(base, script):
    # Variables


    baseGestor = GestorBase()
    baseGestor.cargar_base(base)


    # Función para ejecutar comandos
    def ejecutar_comando(comando):
        if comando.startswith("load "):
            # Cargar un archivo adicional
            _, ruta_base = comando.split(" ", 1)
            baseGestor.cargar_base(ruta_base.strip())
        elif comando == "mostrar":
            baseGestor.mostrar_contenido()
        elif comando == "salir":
            print("Saliendo de la interfaz interactiva.")
            return False
        else:
            realizar_consulta(baseGestor, comando)
        return True
# select ?asignatura, ?email where { ?profe t0:profesor ?asignatura . ?profe t0:email ?email . }
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
        print("No script")
        # Interfaz interactiva para ingresar comandos manualmente
        print("Interfaz interactiva. Escribe 'mostrar' para ver el contenido, 'load <archivo>' para cargar más datos, o 'salir' para terminar.")
        while True:
            comando = input(">> ")
            if not ejecutar_comando(comando):
                break


if __name__ == "__main__":
    main()



