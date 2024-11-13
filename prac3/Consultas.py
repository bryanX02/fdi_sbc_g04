import re
from GestorBase import GestorBase

def realizar_consulta(gestor_base, consulta):
    # Extraemos las variables y la cláusula WHERE de la consulta pseudo-SPARQL
    patron = r"select\s+(.*?)\s+where\s*\{(.*?)\}"
    match = re.search(patron, consulta, re.DOTALL)
    if not match:
        print("Consulta no válida.")
        return

    variables = match.group(1).split(",")
    clausula = match.group(2).strip()
    resultados = []

    # Obtenemos el contenido de las bases
    contenido = gestor_base.obtener_contenido()
    clausulas = [cl.strip() for cl in clausula.split(".") if cl.strip()]

    # Buscamos en el contenido las líneas que cumplen las cláusulas
    for linea in contenido:
        cumple = True
        for c in clausulas:
            if c not in linea:
                cumple = False
                break
        if cumple:
            resultados.append(linea)

    # Mostramos los resultados en formato de tabla
    print(" | ".join(variables) + "\n" + "-" * (len(variables) * 10))
    for resultado in resultados:
        columnas = [col.strip() for col in resultado.split()]
        print(" | ".join(columnas))
