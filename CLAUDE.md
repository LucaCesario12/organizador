# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Comandos

- Ejecutar (simulación, sin mover nada): `python organizador.py [carpeta] --dry-run`
- Ejecutar de verdad: `python organizador.py [carpeta]` (por defecto `~/Downloads`)
- Tests: `pytest` (único test: `pytest test_organizador.py::test_idempotente`)
- No hay build ni linter configurados. El script usa solo la biblioteca estándar; pytest es la única dependencia externa y solo para los tests.

## Arquitectura

Todo el programa vive en `organizador.py`; `test_organizador.py` lo importa como módulo. El diseño separa dos fases:

- `planificar(carpeta)` calcula la lista de `(origen, destino)` **sin tocar el disco**. Aquí van todas las reglas: clasificación por extensión (`CATEGORIAS`, sin distinguir mayúsculas, con `Otros` por defecto), omisión de subcarpetas, de extensiones temporales (`EXTENSIONES_IGNORADAS`) y del propio script, y resolución de conflictos de nombre.
- `ejecutar(plan)` solo mueve los archivos con `shutil.move`.
- `--dry-run` imprime el plan sin llamar a `ejecutar`, por lo que cualquier regla nueva debe ir en `planificar` para que el dry-run la refleje.

Invariantes que los tests protegen:

- Nunca sobrescribir: los conflictos se renombran a `nombre (1).ext`. `destino_libre` también considera los destinos ya reservados dentro del mismo plan, porque en la fase de planificación todavía no existen en disco.
- Solo se procesan archivos del nivel superior (sin recursión), de modo que ejecutar el script dos veces es idempotente.

Los tests usan siempre `tmp_path`; nunca deben apuntar a una carpeta real del usuario.
