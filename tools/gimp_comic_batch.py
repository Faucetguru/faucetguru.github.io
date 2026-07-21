#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GIMP batch script: aplica estilo cómic (líneas + color plano) a una imagen.

Uso desde CLI:
  gimp -i -b '(python-fu-comic-batch "INPUT" "OUTPUT_XCF" "OUTPUT_PNG")' -b '(gimp-quit 0)'

Salidas:
- OUTPUT_XCF: capas separadas (Color, Lineas) con modo Multiply para líneas.
- OUTPUT_PNG: composición final RGB + alpha, 8 bits.
"""

from gimpfu import *

def comic_batch(input_path, output_xcf, output_png):
    img = pdb.gimp_file_load(input_path, input_path)
    base = img.layers[0]
    base.name = "Base"

    # --- Capa Color: color plano tipo cómic ---
    color = base.copy()
    color.name = "Color"
    img.add_layer(color, 0)

    # Desenfoque selectivo (bilateral aproximado con Gaussian)
    pdb.plug_in_gauss(img, color, 2.0, 2.0, 0)

    # Posterizar a 6 niveles (dulce cómic)
    pdb.gimp_drawable_posterize(color, 6)

    # Saturación subida (≈1.2-1.3) usando Hue-Saturation
    pdb.gimp_hue_saturation(img, color, 0, 0, 30, 0)

    # Forzar modo RGB + alpha (si venía en indexado/grayscale)
    pdb.gimp_image_convert_rgb(img)
    if pdb.gimp_drawable_has_alpha(color) == 0:
        pdb.gimp_layer_add_alpha(color)

    # --- Capa Líneas: bordes firmes, negro puro ---
    lines = base.copy()
    lines.name = "Lineas"
    img.add_layer(lines, 0)

    # Desaturar a luma
    pdb.gimp_drawable_desaturate(lines, DESATURATE_LUMINANCE)

    # Detección de bordes tipo cómic: DoG (Diferencia de Gaussianas)
    pdb.plug_in_edge_dog(img, lines, 2.0, 1.0, 0)

    # Invertir para fondo blanco / trazo oscuro
    pdb.gimp_drawable_invert(lines, 0)

    # Umbral para blanco/negro puro (sin grises)
    pdb.gimp_drawable_threshold(lines, 180)

    # Curvas finales para negro de imprenta absoluto
    # En Python-fu no hay Curvas directa simple; usamos Levels:
    # sombras -> 0, medios -> 1, highlights -> 255
    pdb.gimp_levels(lines, HISTOGRAM_VALUE, 0, 255, 1.0, 0, 255)

    # Asegurar alpha en líneas
    if pdb.gimp_drawable_has_alpha(lines) == 0:
        pdb.gimp_layer_add_alpha(lines)

    # Mezcla: líneas en Multiply sobre color
    pdb.gimp_layer_set_mode(lines, MULTIPLY_MODE)

    # Orden visual: Color abajo, Lineas arriba
    img.layers[0].name = "Color"
    img.layers[1].name = "Lineas"

    # --- Guardar XCF editable ---
    pdb.gimp_xcf_save(img, img.layers[0], output_xcf, output_xcf, 0)

    # --- Exportar PNG final (composición) ---
    pdb.file_png_save_defaults(img, img.layers[0], output_png, output_png)

    pdb.gimp_image_delete(img)

register(
    "python-fu-comic-batch",
    "Comic style batch",
    "Apply comic lines + flat color and save PNG+XCF",
    "",
    "",
    "",
    "",
    "",
    [
        (PF_FILE, "input_path", "Input image", ""),
        (PF_FILE, "output_xcf", "Output XCF", ""),
        (PF_FILE, "output_png", "Output PNG", ""),
    ],
    [],
    comic_batch,
    menu="<Image>/File/Batch"
)

main()
