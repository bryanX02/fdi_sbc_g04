from pathlib import Path
import click


class Regla:

    # Cada objero Regla requerirá de un consecuente, una lista de antecedentes
    # y un grado de verdad, que por defecto sera 1
    def __init__(self, cons, antecedentes=None, verdad=1.0):
        self.cons = cons
        self.antecedentes = antecedentes or []
        self.verdad = verdad

    # Funcion booleana respecto al tipo de Regla
    def es_hecho(self):
        return len(self.antecedentes) == 0

    # FUncion que devuelve una impresion de la regla formateada
    def __str__(self):

        if self.es_hecho():
            return f"{self.cons} [{self.verdad}]"
        else:
            antecedentes_str = ", ".join(self.antecedentes)
            mensaje = f"{self.cons} :- {antecedentes_str} [{self.verdad}]"

        return mensaje

# Funcion que se encarga de leer, interpretar y cargar la base del conocimiento
def leer_base(fichero):

    # Array donde se guardaran los objetos Regla
    reglas = []

    # Realizamos la lectura del fichero e interpretamos
    texto = fichero.read_text()
    for line in texto.split("\n"):

        # Si no es un comentario y contiene algo (no es linea vacia)
        if not line.startswith("#") and line.strip():
            
            # Separamos entre cons y antecedentes
            ants = line.split(":-") 
            cons = ants[0].strip() 
            
            # Es un hecho
            if len(ants) == 1:  
                antecedentes = []
                # Buscamos el grado de verdad si está especificado entre corchetes
                verdad = float(cons.split("[")[1].replace("]", "").strip()) if "[" in cons else 1.0
                # Dejamos solo el nombre del hecho
                cons = cons.split("[")[0].strip()
            
            # Es una regla
            else:
                # Separamos los antecedentes en una lista, eliminando espacios extra
                antecedentes = ants[1].split("[")[0].strip().split(",")
                antecedentes = [a.strip() for a in antecedentes] # Eliminamos espacios de cada antecedente
                # Extraemos el grado de verdad si está especificado
                verdad = float(ants[1].split("[")[1].replace("]", "").strip()) if "[" in ants[1] else 1.0
            reglas.append(Regla(cons, antecedentes, verdad))

    return reglas
            
# FUncion que implementa el algoritmo de vuelta atras para consultar la veracidad de una regla
# Recibe como parámetros:
#   - consulta (string): El término que se quiere comprobar (cons) como desarrollador por ej.
#   - reglas (lists): La lista de objetos Regla que componen la base de conocimiento.
#   - hechos (diccionario): Un diccionario de hechos ya conocidos, donde las 
#     claves son los nombres de los hechos y los valores son sus grados de verdad.
# Devuel el grado de verdad con un valor entre 0 y 1, si se cumple, o un none cuando
# la base del conocimineto no es capaz de responder la consulta 
def backward_chain(consulta, reglas, hechos=None):
    
    # Inicialización del diccionario con los hechos
    if hechos is None:
        hechos = {}
    
    # Si el hecho ya está en la base de conocimientos, devolvemos su grado de verdad
    if consulta in hechos:
        return hechos[consulta]
    
    # Para cada regla en la base de conocimiento 
    for regla in reglas:

        # Buscamos coincidencias entre su consecuente y la consulta
        if regla.cons == consulta:
           
            # Calculamos el grado de verdad de los antecedentes
            grado_minimo = 1.0 # Buscaremos el mínimo

            for antecedente in regla.antecedentes:

                # Realizamos la llamada recursiva para comprobar cada antecedente de la regla.
                grado_verdad = backward_chain(antecedente, reglas, hechos)
                # Si un antecedente no se puede cumplir, rompemos el bucle y marcamos como None.
                # ** Cambiar por es_valida **
                if grado_verdad is None:
                    grado_minimo = None
                    break

                # Actualizamos el grado mínimo de verdad tomando el mínimo entre el valor actual y el del antecedente.
                grado_minimo = min(grado_minimo, grado_verdad)
            
            # Si se han cumplido todos los antecedentes, se calcula el grado de verdad final de la regla.
            # ** Cambiar por es_solucion **
            if grado_minimo is not None:
                verdad_regla = min(grado_minimo, regla.verdad)
                hechos[consulta] = verdad_regla
                return verdad_regla

    # Si no se encuentra ninguna regla que se cumpla, devolvemos None
    return None


@click.command()
@click.argument("base")
def main(base: Path):

    # Variables
    fichero = Path(base) # Archivo que contiene la base
    reglas = leer_base(fichero) # Reglas extraidas del fichero
    # Diccionario que contiene los hechos conocidos (que extraemos de las reglas)
    hechos = {regla.cons: regla.verdad for regla in reglas if regla.es_hecho()}
    
    # Bucle infinito para recibir los comandos del usuario con click
    while True:

        # Leemos el comando del usuario y eliminamos espacios en blanco
        comando = input("> ").strip()
        if comando.lower() == 'salir':
            break
        # Si el comando es 'print', imprimimos todas las reglas de la base de conocimiento
        elif comando == "print":
            for regla in reglas:
                print(regla)
        # Intentaremos añadir un nuevo hecho
        elif comando.startswith("add"):
            
            try:
                # Dividimos el comando para extraer el consecuente
                partes = comando.split()
                cons = partes[1]
                
                # Extraemos el grado de verdad
                verdad = float(partes[2].replace("[", "").replace("]", ""))
                
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

        # Si el comando termina en '?' corresponde a una consulta
        elif comando.endswith("?"):

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
        
        # Mensaje de ayuda
        else:
            print("Comando no reconocido. Usa 'print', 'add' o consulta con '?'.")


if __name__ == "__main__":
    main()
