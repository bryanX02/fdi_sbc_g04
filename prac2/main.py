from pathlib import Path
from utils.Lectura import leer_base
from conocimiento.Motor import backward_chain
from conocimiento.Reglas import Regla
from utils.Interpretador import interpretar_add
import click

# NOTAS: En este modulo principal se implementan las funciones necesarias para resolver el problema
# Es una nueva version para subir puntos en cuanto a la calidad del código. Nos aseguramos
# de que el codigo este bien organizado en modulos y la arquitectura tenga mejor diseño.

# Tambien se ha añadido una nueva base del conocimiento siguiendo la rubrica (base_musical.txt)
# Ejemplo de ejecución:
"""
bryan@bryanSpace:~/sbc_repo/fdi_sbc_g04/prac2$ uv run main.py base_musical.txt
> print
compositor :- creatividad, teoria_musical [1.0]
productor :- grabacion, mezcla, creatividad [0.9]
ingeniero_sonido :- grabacion, mezcla, mantenimiento_equipos [1.0]
cantante :- tecnica_vocal, interpretacion [1.0]
musico :- instrumento, teoria_musical [1.0]
director_orquesta :- teoria_musical, liderazgo, musico [0.8]
arreglista :- teoria_musical, creatividad [1.0]
manager :- gestion, soft_skills, networking [1.0]
creatividad :- inspiracion, improvisacion [0.8]
teoria_musical :- armonia, composicion [0.9]
grabacion :- microfonia, software_grabacion [0.7]
mezcla :- software_grabacion, ecualizacion [0.8]
instrumento :- guitarra, piano [0.7]
instrumento :- violin, bateria [0.6]
tecnica_vocal :- respiracion, afinacion [0.9]
interpretacion :- expresion, presencia_escenica [0.8]
liderazgo :- gestion, motivacion [0.7]
gestion :- planificacion, organizacion [0.8]
networking :- relaciones_publicas, comunicacion [0.7]
> creatividad?
creatividad: No
> add inspiracion [0.8]
Hecho 'inspiracion' añadido con grado de verdad 0.8
> add improvisacion [0.8]
Hecho 'improvisacion' añadido con grado de verdad 0.8
> creatividad?
creatividad: Sí, mucho (0.80)
> salir
"""


# Interfaz interactiva para resolver consultas y manejar hechos.
# Args:
#        reglas (list): Lista de reglas cargadas.
#        hechos (dict): Diccionario inicial de hechos conocidos.
def ejecutar_interfaz(reglas, hechos):

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
            try:
                hecho, verdad = interpretar_add(comando)
                nueva_regla = Regla(hecho, [], verdad)
                reglas.append(nueva_regla)
                hechos[hecho] = verdad
                print(f"Hecho '{hecho}' añadido con grado de verdad {verdad}")
            except ValueError as e:
                print(f"Error: {e}")
        # Si el comando termina en '?' corresponde a una consulta
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
        # Mensaje de ayuda
        else:
            print(
                "Comando no reconocido. Usa 'print', 'add' o consultas con '?'. Use 'salir' para terminar."
            )


# Funcion principal que llama a la lectura y ejecuta la interfaz
@click.command()
@click.argument("base", type=Path)
def main(base):

    reglas = leer_base(base)
    hechos = {regla.cons: regla.verdad for regla in reglas if regla.es_hecho()}
    ejecutar_interfaz(reglas, hechos)


if __name__ == "__main__":
    main()
