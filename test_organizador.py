from pathlib import Path

import pytest

import organizador as org


def crear(carpeta: Path, *nombres: str) -> None:
    for nombre in nombres:
        (carpeta / nombre).write_text(nombre)


def listar(carpeta: Path) -> set:
    return {p.relative_to(carpeta).as_posix() for p in carpeta.rglob("*") if p.is_file()}


@pytest.mark.parametrize("nombre,esperada", [
    ("a.jpg", "Imágenes"),
    ("a.PNG", "Imágenes"),
    ("a.pdf", "Documentos"),
    ("a.docx", "Documentos"),
    ("a.mp4", "Videos"),
    ("a.zip", "Comprimidos"),
    ("a.xyz", "Otros"),
    ("sinextension", "Otros"),
])
def test_clasificar(nombre, esperada):
    assert org.clasificar(Path(nombre)) == esperada


def test_dry_run_no_mueve_nada(tmp_path, capsys):
    crear(tmp_path, "foto.jpg", "doc.pdf")
    antes = listar(tmp_path)
    assert org.main([str(tmp_path), "--dry-run"]) == 0
    assert listar(tmp_path) == antes
    assert "[dry-run]" in capsys.readouterr().out


def test_ejecucion_real_mueve_a_subcarpetas(tmp_path):
    crear(tmp_path, "foto.jpg", "doc.pdf", "peli.mkv", "x.zip", "raro.abc")
    assert org.main([str(tmp_path)]) == 0
    assert listar(tmp_path) == {
        "Imágenes/foto.jpg", "Documentos/doc.pdf", "Videos/peli.mkv",
        "Comprimidos/x.zip", "Otros/raro.abc",
    }


def test_conflicto_no_sobrescribe(tmp_path):
    (tmp_path / "Imágenes").mkdir()
    (tmp_path / "Imágenes" / "foto.jpg").write_text("original")
    (tmp_path / "foto.jpg").write_text("nueva")
    org.main([str(tmp_path)])
    assert (tmp_path / "Imágenes" / "foto.jpg").read_text() == "original"
    assert (tmp_path / "Imágenes" / "foto (1).jpg").read_text() == "nueva"


def test_conflicto_dentro_del_mismo_plan(tmp_path):
    # Dos archivos distintos que acabarían con el mismo nombre de destino.
    destinos = [d for _, d in _plan_con_duplicados(tmp_path)]
    assert len(set(destinos)) == len(destinos)


def _plan_con_duplicados(tmp_path):
    (tmp_path / "Imágenes").mkdir()
    (tmp_path / "Imágenes" / "a.jpg").write_text("x")
    crear(tmp_path, "a.jpg", "a.JPG")
    return org.planificar(tmp_path)


def test_ignora_subcarpetas_y_temporales(tmp_path):
    (tmp_path / "MiCarpeta").mkdir()
    (tmp_path / "MiCarpeta" / "dentro.jpg").write_text("x")
    crear(tmp_path, "descarga.crdownload", "otra.part", "t.tmp")
    antes = listar(tmp_path)
    assert org.planificar(tmp_path) == []
    org.main([str(tmp_path)])
    assert listar(tmp_path) == antes


def test_idempotente(tmp_path):
    crear(tmp_path, "foto.jpg", "doc.pdf")
    org.main([str(tmp_path)])
    despues_primera = listar(tmp_path)
    org.main([str(tmp_path)])
    assert listar(tmp_path) == despues_primera


def test_carpeta_invalida(tmp_path, capsys):
    assert org.main([str(tmp_path / "noexiste")]) == 1
    assert "Error" in capsys.readouterr().err
