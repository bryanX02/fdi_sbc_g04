from pathlib import Path
import click

# Vamos a implentar un sistema de interpretación de consultas al esitilo de Wikidata Query Service
@click.command()
@click.argument("base")
def main(base: Path):

    # Variables
    fichero = Path(base)  # Archivo que contiene la base

if __name__ == "__main__":
    main()
