from pathlib import Path
import re

class GestorBase:
    def __init__(self):
        # Diccionario para almacenar el contenido de las bases de conocimiento
        self.contenido_bases = {}

    def cargar_base(self, ruta_base):
        # Cargamos el archivo y procesar los triples
        base_path = Path(ruta_base)
        tripletas = []  # Lista para almacenar los triples procesados
        sujeto_actual = None

        with base_path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue  # Ignoramos líneas vacías y comentarios
                
                # Procesamos las líneas que terminan con ';' o '.'
                if line.endswith("."):
                    partes = re.findall(r'".*?"|\S+', line[:-1])

                    if len(partes) == 3:
                        tripletas.append(tuple(partes))
                elif line.endswith(";"):
                    partes = re.findall(r'".*?"|\S+', line[:-1])
                    if len(partes) == 3:
                        sujeto_actual, predicado, objeto = partes
                        tripletas.append((sujeto_actual, predicado, objeto))
                    elif len(partes) == 2 and sujeto_actual:
                        predicado, objeto = partes
                        tripletas.append((sujeto_actual, predicado, objeto))

        self.contenido_bases[base_path.name] = tripletas

        print(f"SBC_P3> Cargando '{base_path.name}'... OK!")

    def mostrar_contenido(self):
        # Mostramos el contenido de cada base cargada
        for nombre, contenido in self.contenido_bases.items():
            print(f"\nContenido de {nombre}:")
            for triple in contenido:
                print(triple)
            print("-" * 40)

    def obtener_contenido(self):
        # Retornamos todos los triples almacenados
        return [triple for contenido in self.contenido_bases.values() for triple in contenido]
