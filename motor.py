from Regla import Regla

def buscar_grado_minimo(regla, reglas, hechos):

    # Calculamos el grado de verdad de los antecedentes
    grado_minimo = 1.0 # Buscaremos el mínimo

    antecedentes = regla.antecedentes
    valided = True # para el bucle
    i = 0

    while i < len(antecedentes) and valided:
        
        # Realizamos la llamada recursiva para comprobar cada antecedente de la regla.
        grado_verdad = backward_chain(antecedentes[i], reglas, hechos)
        # Si un antecedente no se puede cumplir, rompemos el bucle y marcamos como None.
        if es_valida(grado_verdad):
            grado_minimo = None
            valided = False
        else:
            # Actualizamos el grado mínimo de verdad tomando el mínimo entre el valor actual y el del antecedente.
            grado_minimo = min(grado_minimo, grado_verdad)
            i += 1

    return grado_minimo

def es_valida(grado):
    return grado is None

def es_solucion(grado):
    return grado is not None

# FUncion que implementa el algoritmo de vuelta atras para consultar la veracidad de una regla
# Recibe como parámetros:
#   - consulta (string): El término que se quiere comprobar (cons) como desarrollador por ej.
#   - reglas (lists): La lista de objetos Regla que componen la base de conocimiento.
#   - hechos (diccionario): Un diccionario de hechos ya conocidos, donde las 
#     claves son los nombres de los hechos y los valores son sus grados de verdad.
# Devuel el grado de verdad con un valor entre 0 y 1, si se cumple, o un none cuando
# la base del conocimineto no es capaz de responder la consulta 
def backward_chain(consulta, reglas, hechos=None):
    
    # Si no se encuentra ninguna regla que se cumpla, devolvemos None
    resultado = None

    # Inicialización del diccionario con los hechos
    if hechos is None:
        hechos = {}
    
    # Si el hecho ya está en la base de conocimientos, devolvemos su grado de verdad
    if consulta in hechos:
        resultado = hechos[consulta]
    else:
        # Para cada regla en la base de conocimiento 
        for regla in reglas:

            # Buscamos coincidencias entre su consecuente y la consulta
            if regla.cons == consulta:
            
                # Calculamos el grado de verdad de los antecedentes
                grado_minimo = buscar_grado_minimo(regla, reglas, hechos) # Buscaremos el mínimo
                
                # Si se han cumplido todos los antecedentes, se calcula el grado de verdad final de la regla.
                # ** Cambiar por es_solucion **
                if es_solucion(grado_minimo):
                    verdad_regla = min(grado_minimo, regla.verdad)
                    hechos[consulta] = verdad_regla
                    resultado = verdad_regla

    return resultado
