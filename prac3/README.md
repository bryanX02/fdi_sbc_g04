# Práctica 3 - Sistemas Basados en Conocimiento (SBC)

### Estudiantes:
- Bryan Quilumba
- Jesús Rodríguez

## Descripción del Proyecto

En este repositorio se desarrolla la Práctica 2 de la asignatura de Sistemas Basados en Conocimiento. Se ha implementado sistema capaz de representar y consultar redes semánticas usando un subconjunto simplificado de RDF y SPARQL.

## Ejecución

Para ejecutar el proyecto, es necesario emplear la herramienta `uv` de Python en la terminal de Linux de la siguiente manera:

```bash
uv run main.py <base_conocimiento.tll>
```

## Estructura del Proyecto
El proyecto contiene los siguientes archivos:

- `base_conocimiento.tll`, `base_conocimiento_2.tll`, `base_conocimiento_3.tll`: Archivos que contienen las bases de conocimiento con las que el motor realiza las consultas.
- `Consultas.py`: Módulo encargado de leer y procesar ls consultas.
- `GestorBase.py`: Módulo principal del que gestiona la base del conocimiento.
- `Visualizador.py`: Módulo encargado de representar los grafos.
- `comandos.txt`: Archivo que contiene comandos preestablecidos para lanzar al inicio del programa.
- `README.md`: Documento con la descripción y guía de uso del proyecto.
- `pyproject.toml`: Archivo de configuración del proyecto.
- `uv.lock`: Archivo de bloqueo generado por la herramienta `uv`.
