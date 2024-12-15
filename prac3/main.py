from pathlib import Path
import click
from Consultas import realizar_consulta
from GestorBase import *
from Visualizador import exportar_grafo


# Implementar el sistema de interpretación de consultas al estilo de Wikidata Query Service
@click.command()
@click.argument("base")
@click.option(
    "--script",
    type=click.Path(exists=True),
    help="Archivo con comandos a ejecutar en secuencia",
)
def main(base, script):
    # Variables

    baseGestor = GestorBase()
    baseGestor.cargar_base(base)
    ultimos_resultados = []

    # Función para ejecutar comandos
    def ejecutar_comando(comando):
        nonlocal ultimos_resultados
        if comando.startswith("load "):
            # Cargar un archivo adicional
            _, ruta_base = comando.split(" ", 1)
            baseGestor.cargar_base(ruta_base.strip())
        elif comando == "mostrar":
            baseGestor.mostrar_contenido()
        elif comando.startswith("draw "):
            match = re.match(r'draw\s+"(.+?)"', comando)
            if match:
                filename = match.group(1)
                exportar_grafo(ultimos_resultados, filename)
            else:
                print('Comando draw no válido. Usa: draw "nombre_archivo.png"')
        elif comando == "salir":
            print("Saliendo de la interfaz interactiva.")
            return False
        else:
            ultimos_resultados = realizar_consulta(baseGestor, comando)
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
        print(
            "Interfaz interactiva. Escribe 'mostrar' para ver el contenido, 'load <archivo>' para cargar más datos, draw para dibujar el grafo o 'salir' para terminar."
        )
        while True:
            comando = input(">> ")
            if not ejecutar_comando(comando):
                break


# CONSULTAS PARA PROBRAR:

# select ?nombre where { ?persona wdt:P31 q1:persona . ?persona t1:nombre ?nombre . }
# select ?nombre where { ?piloto wdt:P31 q1:piloto . ?piloto t1:nombre ?nombre . }

# Equipos en los que ha estado Hamilton (piloto1):
# select ?nombre where { ?equipo wdt:P31 q1:equipo . q1:piloto1 t1:equipos ?equipo . ?equipo t1:nombre ?nombre . }

if __name__ == "__main__":
    main()
