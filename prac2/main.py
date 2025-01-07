from pathlib import Path
from utils.Lectura import leer_base
from conocimiento.Motor import backward_chain
from conocimiento.Reglas import Regla
from utils.Interpretador import interpretar_add
import click

# NOTAS: En este modulo principal se implementan las funciones necesarias para resolver el problema
# Es una nueva version para subir puntos en cuando a la calidad del codigo. Nos aseguramos
# de que el codigo este bien organizado en modulos y mejor diseño de la arquitectura.

# Interfaz interactiva para resolver consultas y manejar hechos.
#Args:
#        reglas (list): Lista de reglas cargadas.
#        hechos (dict): Diccionario inicial de hechos conocidos.   
def ejecutar_interfaz(reglas, hechos):
    
    while True:
        comando = input("> ").strip()
        if comando.lower() == "salir":
            break
        elif comando == "print":
            for regla in reglas:
                print(regla)
        elif comando.startswith("add"):
            try:
                hecho, verdad = interpretar_add(comando)
                nueva_regla = Regla(hecho, [], verdad)
                reglas.append(nueva_regla)
                hechos[hecho] = verdad
                print(f"Hecho '{hecho}' añadido con grado de verdad {verdad}")
            except ValueError as e:
                print(f"Error: {e}")
        elif comando.endswith("?"):
            consulta = comando[:-1].strip()
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
        else:
            print("Comando no reconocido. Usa 'print', 'add' o consultas con '?'. Use 'salir' para terminar.")


@click.command()
@click.argument("base", type=Path)
def main(base):
    """
    Punto de entrada principal para cargar una base de conocimiento.

    Args:
        base (Path): Archivo con la base de conocimiento.
    """
    reglas = leer_base(base)
    hechos = {regla.cons: regla.verdad for regla in reglas if regla.es_hecho()}
    ejecutar_interfaz(reglas, hechos)


if __name__ == "__main__":
    main()