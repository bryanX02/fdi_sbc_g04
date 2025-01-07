
# Funcione que se encarga de interpretar el comando add de la consola
# Recibe como parámetro un comando en formato de cadena y devuelve una tupla con la acción y los argumentos.
def interpretar_add(comando):

    partes = comando.split()
    if len(partes) != 3 or not partes[2].startswith("[") or not partes[2].endswith("]"):
        raise ValueError("Formato incorrecto. Use 'add <hecho> [grado_de_verdad]'.")
    hecho = partes[1]
    verdad = float(partes[2][1:-1])  # Extraer valor numérico entre corchetes
    return hecho, verdad
