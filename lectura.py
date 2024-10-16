from Regla import Regla

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