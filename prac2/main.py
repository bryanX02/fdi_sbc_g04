from pathlib import Path
from Regla import Regla
from lectura import leer_base
from motor import backward_chain
import click


def consultar(comando, reglas, hechos):

    consulta = comando[:-1].strip()  # Quitamos la '?' al final

    # Llamamos al algoritmo de vuelta atras que corroborara la consulta
    resultado = backward_chain(consulta, reglas, hechos)

    # Interpretamos el resultado
    if resultado is not None:
        if resultado >= 0.7:
            print(f"{consulta}: Sí, mucho ({resultado:.2f})")
        elif resultado > 0.4:
            print(f"{consulta}: Sí, un poco ({resultado:.2f})")
        else:
            print(f"{consulta}: Sí, pero apenas ({resultado:.2f})")
    else:
        print(f"{consulta}: No")


def aniadir_hecho(comando, reglas, hechos):
    try:

        cons, verdad = procesar_command(comando)

        # Creamos una nueva regla como hecho (sin antecedentes) y la añadimos a la lista
        nueva_regla = Regla(cons, [], verdad)
        reglas.append(nueva_regla)

        # Añadimos el hecho al diccionario y lo notificamos (no lo pide el profe)
        hechos[cons] = verdad
        print(f"Hecho '{cons}' añadido con grado de verdad {verdad}")

    # Si ocurre un error en el try, mostramos un mensaje de error
    except Exception as e:
        print("Error al agregar el hecho. Formato: add hecho [grado_de_verdad]")
        print(e)


def procesar_command(comando):
    # Dividimos el comando para extraer el consecuente
    partes = comando.split()
    cons = partes[1]

    # Extraemos el grado de verdad
    verdad = float(partes[2].replace("[", "").replace("]", ""))

    return cons, verdad


def resoler_problema(fichero, reglas, hechos):

    # Bucle infinito para recibir los comandos del usuario con click
    while True:

        # Leemos el comando del usuario y eliminamos espacios en blanco
        comando = input("> ").strip()
        if comando.lower() == "salir":
            break
        # Si el comando es 'print', imprimimos todas las reglas de la base de conocimiento
        elif comando == "print":
            for regla in reglas:
                print(regla)
        # Intentaremos añadir un nuevo hecho
        elif comando.startswith("add"):

            aniadir_hecho(comando, reglas, hechos)

        # Si el comando termina en '?' corresponde a una consulta
        elif comando.endswith("?"):

            consultar(comando, reglas, hechos)

        # Mensaje de ayuda
        else:
            print("Comando no reconocido. Usa 'print', 'add' o consulta con '?'.")


@click.command()
@click.argument("base")
def main(base: Path):

    # Variables
    fichero = Path(base)  # Archivo que contiene la base
    reglas = leer_base(fichero)  # Reglas extraidas del fichero
    # Diccionario que contiene los hechos conocidos (que extraemos de las reglas)
    hechos = {regla.cons: regla.verdad for regla in reglas if regla.es_hecho()}
    resoler_problema(fichero, reglas, hechos)


if __name__ == "__main__":
    main()
