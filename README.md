# Organizador de archivos

Script en Python que ordena una carpeta (por defecto, Descargas) moviendo los archivos sueltos a subcarpetas según su tipo:

| Carpeta | Extensiones |
|---|---|
| `Imágenes` | jpg, jpeg, png, gif, bmp, webp, svg, heic |
| `Documentos` | pdf, doc, docx, txt, xls, xlsx, ppt, pptx, odt, csv |
| `Videos` | mp4, mkv, avi, mov, wmv, webm |
| `Comprimidos` | zip, rar, 7z, tar, gz |
| `Otros` | cualquier otra extensión |

## Qué garantiza

- **Nunca sobrescribe.** Si ya existe `Imágenes/foto.jpg`, el archivo nuevo se guarda como `foto (1).jpg`.
- **Solo toca archivos sueltos** del nivel superior. Las subcarpetas existentes y su contenido no se tocan.
- **Ignora descargas en curso** (`.crdownload`, `.part`, `.tmp`) y al propio script.
- **Es idempotente.** Ejecutarlo dos veces seguidas no cambia nada la segunda vez.

## Instalación

Probado con Python 3.14. El script usa solo la biblioteca estándar, así que no hay nada que instalar.

```
git clone <https://github.com/LucaCesario12/organizador>
cd organizador-archivos
```

## Uso

```
python organizador.py [carpeta] [--dry-run]
```

- `carpeta` es opcional. Si no la indicas, se usa `~/Downloads`.
- `--dry-run` muestra qué se movería **sin mover nada**.

Se recomienda ejecutar primero con `--dry-run` y revisar la lista:

```
python organizador.py --dry-run
```

Si todo se ve bien, ejecútalo sin la opción:

```
python organizador.py
```

También puedes apuntar a otra carpeta:

```
python organizador.py "D:\Otra\Carpeta" --dry-run
```

### Ejemplo de salida

```
$ python organizador.py --dry-run
[dry-run] datos.xyz -> Otros\datos.xyz
[dry-run] foto.jpg -> Imágenes\foto.jpg
[dry-run] fotos.zip -> Comprimidos\fotos.zip
[dry-run] informe.pdf -> Documentos\informe.pdf
[dry-run] peli.mkv -> Videos\peli.mkv

5 archivo(s) se moverían. No se movió nada.
```

Sin `--dry-run`, la salida es igual pero sin el prefijo `[dry-run]` y termina con `5 archivo(s) movidos.`

## Tests

Los tests usan [pytest](https://pytest.org), que es la única dependencia externa y solo se necesita para ellos:

```
pip install pytest
pytest
```

Para correr un solo test:

```
pytest test_organizador.py::test_idempotente
```

Los tests trabajan siempre en carpetas temporales. Nunca tocan tus archivos reales.
