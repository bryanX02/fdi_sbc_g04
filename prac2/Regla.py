# Clase cuyos objetos representaran las reglas con sus consultas, antecedentes y grados de verdad 
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