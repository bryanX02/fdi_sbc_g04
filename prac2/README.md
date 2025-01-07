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

conocimiento           # Nuevos módulos relacionados con lógica de conocimiento
- `Reglas.py`          # Módulo que define la estructura y comportamiento de las reglas en el sistema.
- `Motor.py`           # Módulo principal del motor de inferencia.

utils                  # Módulos genéricos no específicos
- `Lectura.py`         # Funciones de lectura y carga de base de 
- `Procesador.py`      # Procesamiento de comandos 

`main.py`                # Script principal que usa a los demas módulos

`base_laboral.txt`   # Base del enunciado
`base_laboral_2.txt` # Base de la formula 1
`base_musical.txt`   # Base con información musical

`pyproject.toml`         # Configuración del proyecto para herramientas de Python

`uv.lock`: Archivo de bloqueo generado por la herramienta `uv`.

`README.md`              # Documentación principal

