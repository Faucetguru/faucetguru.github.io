#!/usr/bin/env python3
"""Batch CLI: convierte las imágenes de Escritorio/imges/ a estilo cómic.

Uso:
  python tools/comicify_images.py

Requisitos:
  - GIMP 2.10+ instalado
  - Tener imágenes ya copiadas en ~/Escritorio/imges/

Salidas:
  ~/Escritorio/imges/comic_out/*.png   -> composición final
  ~/Escritorio/imges/comic_out/*.xcf   -> editable GIMP

No modifica archivos originales.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

SRC_DIR = Path.home() / "Escritorio" / "imgen"
OUT_DIR = SRC_DIR / "comic"
BACKUP_DIR = SRC_DIR / "originals"
GIMP_BATCH = Path(__file__).with_name("gimp_comic_batch.py")

EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}


def backup(src_file: Path):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    dst = BACKUP_DIR / src_file.name
    shutil.copy2(str(src_file), str(dst))
    return dst


def process_with_gimp(src_file: Path, dst_xcf: Path, dst_png: Path):
    script = str(GIMP_BATCH)
    cmd = [
        "gimp",
        "-i",
        "-b",
        "(python-fu-comic-batch \"%s\" \"%s\" \"%s\")" % (
            str(src_file).replace("\\", "/"),
            str(dst_xcf).replace("\\", "/"),
            str(dst_png).replace("\\", "/"),
        ),
        "-b",
        "(gimp-quit 0)",
    ]
    print("  gimp:", dst_xcf.name)
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise RuntimeError("GIMP failed: " + p.stderr.decode("utf-8", "ignore")[-400:])


def main():
    if not SRC_DIR.exists():
        print("ERROR: no existe %s" % SRC_DIR)
        print("Copiá ahí las imágenes y volvé a correr.")
        sys.exit(1)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    files = sorted(
        p for p in SRC_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in EXTENSIONS
    )
    if not files:
        print("No hay imágenes en %s" % SRC_DIR)
        sys.exit(0)

    print("Imágenes a procesar:", len(files))
    ok, fail = 0, []
    for src in files:
        dst_xcf = OUT_DIR / (src.stem + ".xcf")
        dst_png = OUT_DIR / (src.stem + ".png")
        try:
            backup(src)
            process_with_gimp(src, dst_xcf, dst_png)
            ok += 1
        except Exception as e:
            fail.append((src.name, str(e)[:180]))

    print("\nResultado: %d OK, %d FAIL" % (ok, len(fail)))
    for name, err in fail:
        print("FAIL", name, "->", err)

    print("Entrada :", SRC_DIR)
    print("Salida  :", OUT_DIR)
    print("Backups :", BACKUP_DIR)


if __name__ == "__main__":
    main()
