import re
from GestorBase import GestorBase

def realizar_consulta(gestor_base, consulta):
    # Usamos una expresión regular para dividir la consulta en SELECT y WHERE
    patron = r"select\s+(.*?)\s+where\s*\{(.*?)\}"
    match = re.search(patron, consulta, re.DOTALL)
    if not match:
        print("Consulta no válida. Asegúrate de usar el formato correcto.")
        return

    # Extraemos las variables y las cláusulas WHERE
    variables = [v.strip() for v in match.group(1).split(",")]
    clausulas = [c.strip() for c in match.group(2).strip().split(".") if c.strip()]

    # Obtenemos el contenido (triples) desde la base de conocimiento
    contenido = gestor_base.obtener_contenido()

    # Evaluamos las cláusulas WHERE
    resultados = backtracking(clausulas, contenido, {}, 0)

    # Mostramos los resultados como tabla
    if resultados:
        encabezado = " | ".join(variables)
        print(encabezado)
        print("-" * len(encabezado))
        for resultado in resultados:
            fila = " | ".join(resultado.get(var, "") for var in variables)
            print(fila)
    else:
        print("No se encontraron resultados.")


def backtracking(clausulas, triples, mapeo_actual, indice):
    if indice == len(clausulas):  # Si hemos evaluado todas las cláusulas
        return [mapeo_actual]

    clausula = clausulas[indice]
    partes = clausula.split()
    if len(partes) != 3:
        print(f"Cláusula inválida: {clausula}")
        return []

    sujeto, predicado, objeto = partes
    soluciones = []

    for triple in triples:
        nuevo_mapeo = mapeo_actual.copy()
        if evaluar_clausula(triple, sujeto, predicado, objeto, nuevo_mapeo):
            soluciones += backtracking(clausulas, triples, nuevo_mapeo, indice + 1)

    return soluciones


def evaluar_clausula(triple, sujeto, predicado, objeto, mapeo):
    # Verificamos si el triple coincide con la cláusula WHERE
    sujeto_t, predicado_t, objeto_t = triple

    if not coincidir_valor(sujeto, sujeto_t, mapeo):
        return False
    if not coincidir_valor(predicado, predicado_t, mapeo):
        return False
    if not coincidir_valor(objeto, objeto_t, mapeo):
        return False

    return True


def coincidir_valor(variable, valor, mapeo):
    if variable.startswith("?"):  # Si es una variable
        if variable in mapeo:  # Si ya está mapeada
            return mapeo[variable] == valor
        else:  # Mapear la variable al valor actual
            mapeo[variable] = valor
            return True
    else:  # Si no es variable, debe coincidir exactamente
        return variable.strip('"') == valor.strip('"')

