from pathlib import Path

class gestorBase:
    def __init__(self):
        # Creamos un diccionario para almacenar el contenido de las bases de conocimiento
        self.contenido_bases = {}

    def cargar_base(self, ruta_base):
        # Cargamos el archivo y almacenamos cada línea
        base_path = Path(ruta_base)
        with base_path.open("r", encoding="utf-8") as file:
            self.contenido_bases[base_path.name] = [line.strip() for line in file if line.strip()]
        print(f"SBC_P3> Cargando '{base_path.name}'... OK!")

    def mostrar_contenido(self):
        # Mostramos el contenido de cada base de conocimiento cargada
        for nombre, contenido in self.contenido_bases.items():
            print(f"\nContenido de {nombre}:")
            for linea in contenido:
                print(linea)
            print("-" * 40)

    def obtener_contenido(self):
        # Retornamos el contenido de todas las bases para las consultas
        return [linea for contenido in self.contenido_bases.values() for linea in contenido]
