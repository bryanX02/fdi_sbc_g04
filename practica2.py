from pathlib import Path
import click
class Regla:
    def __init__(self, cons, resto):
        self.cons = cons
        self.resto = resto
    
def leer_base(fichero):
    reglas = []
    texto = fichero.read_text()
    for line in texto.split("\n"):
        if line.startswith("#") or not line:
            continue
        cons, resto = line.split(":-")
        cons = cons.strip()
        reglas.append(Regla(cons,resto))
    return reglas
            
@click.command()
@click.argument("base")
def main(base: Path):
    fichero = Path(base)
    reglas = leer_base(fichero)
    print(reglas[0].cons,reglas[0].resto)


if __name__ == "__main__":
    main()
