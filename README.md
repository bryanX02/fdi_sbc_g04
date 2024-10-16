# Práctica 2 - Sistemas Basados en Conocimiento (SBC)

### Estudiantes:
- Bryan Quilumba
- Jesús Rodríguez

### Notas:
El commit realizado por el usuario `maritrib` fue en realidad realizado por `jesrod06`, quien tenía una sesión de Git desconocida en su terminal.

## Descripción del Proyecto

En este repositorio se desarrolla la Práctica 2 de la asignatura de Sistemas Basados en Conocimiento. Se ha implementado un motor que analiza una consulta basada en hechos y reglas recogidos en una base de conocimiento, y que calcula el grado de verdad utilizando un sistema basado en lógica difusa.

## Ejecución

Para ejecutar el proyecto, es necesario emplear la herramienta `uv` de Python en la terminal de Linux de la siguiente manera:

```bash
uv run main.py <base_conocimiento.txt>
```

## Estructura del Proyecto
El proyecto contiene los siguientes archivos:

- `base_laboral.txt` y `base_laboral_2.txt`: Archivos de texto que contienen las bases de conocimiento con las que el motor realiza las consultas.
- `lectura.py`: Módulo encargado de leer y procesar los archivos de la base de conocimiento.
- `motor.py`: Módulo principal del motor de inferencia.
- `main.py`: Script principal para ejecutar el programa.
- `Regla.py`: Módulo que define la estructura y comportamiento de las reglas en el sistema.
- `README.md`: Documento con la descripción y guía de uso del proyecto.
- `pyproject.toml`: Archivo de configuración del proyecto. (aún no implementado)
- `uv.lock`: Archivo de bloqueo generado por la herramienta `uv`.


