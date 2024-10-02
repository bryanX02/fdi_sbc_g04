from pathlib import Path

#def backward_chain(consulta):
class Regla:
    def __init__(self, cons, resto):
        self.cons = cons
        self.resto = resto

    def leer_base(fichero):
        texto = fichero.read_text()
        for line in texto.split("\n"):
            if line.startswith("#") or not line:
                continue
            cons, resto = line.split(":-")
            cons = cons.strip()
            antecedentes = resto.split(",")
            print(line)
