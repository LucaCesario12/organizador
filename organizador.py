#!/usr/bin/env python3
"""Organiza una carpeta (por defecto Descargas) moviendo archivos a subcarpetas por tipo."""

import argparse
import shutil
import sys
from pathlib import Path

CATEGORIAS = {
    "Imágenes": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".heic"},
    "Documentos": {
        ".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx",
        ".ppt", ".pptx", ".odt", ".csv",
    },
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".webm"},
    "Comprimidos": {".zip", ".rar", ".7z", ".tar", ".gz"},
}
CATEGORIA_POR_DEFECTO = "Otros"
EXTENSIONES_IGNORADAS = {".crdownload", ".part", ".tmp"}


def clasificar(archivo: Path) -> str:
    """Devuelve el nombre de la categoría según la extensión (sin distinguir mayúsculas)."""
    ext = archivo.suffix.lower()
    for categoria, extensiones in CATEGORIAS.items():
        if ext in extensiones:
            return categoria
    return CATEGORIA_POR_DEFECTO


def destino_libre(destino: Path, reservados: set = frozenset()) -> Path:
    """Si destino existe (o ya está reservado), devuelve 'nombre (1).ext', 'nombre (2).ext', ..."""
    candidato = destino
    n = 1
    while candidato.exists() or candidato in reservados:
        candidato = destino.with_name(f"{destino.stem} ({n}){destino.suffix}")
        n += 1
    return candidato


def planificar(carpeta: Path) -> list:
    """Calcula la lista de (origen, destino) sin tocar el disco."""
    carpeta = Path(carpeta)
    script = Path(__file__).resolve()
    plan = []
    reservados = set()
    for item in sorted(carpeta.iterdir()):
        if not item.is_file():
            continue
        if item.suffix.lower() in EXTENSIONES_IGNORADAS:
            continue
        if item.resolve() == script:
            continue
        destino = destino_libre(carpeta / clasificar(item) / item.name, reservados)
        reservados.add(destino)
        plan.append((item, destino))
    return plan


def ejecutar(plan: list) -> None:
    """Mueve los archivos del plan, creando las subcarpetas necesarias."""
    for origen, destino in plan:
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(origen), str(destino))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "carpeta", nargs="?", type=Path, default=Path.home() / "Downloads",
        help="carpeta a organizar (por defecto: ~/Downloads)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="muestra qué se movería sin mover nada",
    )
    args = parser.parse_args(argv)

    if not args.carpeta.is_dir():
        print(f"Error: {args.carpeta} no es una carpeta válida.", file=sys.stderr)
        return 1

    plan = planificar(args.carpeta)
    if not plan:
        print("No hay archivos para organizar.")
        return 0

    prefijo = "[dry-run] " if args.dry_run else ""
    for origen, destino in plan:
        print(f"{prefijo}{origen.name} -> {destino.relative_to(args.carpeta)}")

    if args.dry_run:
        print(f"\n{len(plan)} archivo(s) se moverían. No se movió nada.")
    else:
        ejecutar(plan)
        print(f"\n{len(plan)} archivo(s) movidos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
