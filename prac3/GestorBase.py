from pathlib import Path
import re


class GestorBase:
    def __init__(self):
        # Diccionario para almacenar el contenido de las bases de conocimiento
        self.contenido_bases = {}

    def cargar_base(self, ruta_base):
        base_path = Path(ruta_base)
        tripletas = []
        sujeto_actual = None

        with base_path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue  # Ignorar líneas vacías o comentarios

                # Concatenar líneas que continúan en la siguiente
                while not line.endswith("."):
                    next_line = next(file).strip()
                    line += " " + next_line

                # Remover el punto final y dividir en segmentos por ';'
                line = line.rstrip(".")
                segmentos = line.split(";")

                for i, segmento in enumerate(segmentos):
                    segmento = segmento.strip()
                    if not segmento:
                        continue

                    partes = re.findall(r'".*?"|\S+', segmento)

                    # Si es el primer segmento y contiene un sujeto, actualizar sujeto_actual
                    if i == 0 and ":" in partes[0]:
                        sujeto_actual = partes[0]
                        partes = partes[1:]  # Eliminar el sujeto de las partes

                    # Procesar pares predicado-objeto
                    for j in range(0, len(partes), 2):
                        if j + 1 < len(partes):
                            predicado = partes[j]
                            objeto = partes[j + 1]
                            tripletas.append((sujeto_actual, predicado, objeto))
                        else:
                            print(f"Advertencia: Predicado sin objeto en línea: {line}")

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
        return [
            triple
            for contenido in self.contenido_bases.values()
            for triple in contenido
        ]

    def agregar_triple(self, sujeto, predicado, objeto):
        # Asumimos que todas las entradas van a la base principal, aquí podría ser más específico
        base_principal = (
            list(self.contenido_bases.keys())[0]
            if self.contenido_bases
            else "base_default"
        )
        if base_principal not in self.contenido_bases:
            self.contenido_bases[base_principal] = []
        self.contenido_bases[base_principal].append((sujeto, predicado, objeto))
        print(
            f"SBC_P3> Triple agregado a '{base_principal}': ({sujeto}, {predicado}, {objeto})"
        )
