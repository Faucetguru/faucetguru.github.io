#!/usr/bin/env python3
"""
Validar posts HTML según SEO best practices.
Requisitos:
- Título H1 presente
- Meta description (70-160 caracteres)
- Meta keywords (mínimo 3 palabras)
- Contenido mínimo 300 caracteres
- Imágenes con alt text
"""

import re
import sys
from pathlib import Path

MIN_CONTENT_CHARS = 300
MIN_KEYWORDS = 3
MIN_KEYWORD_LENGTH = 3

def validate_post(html_path):
    errors = []
    warnings = []
    
    content = html_path.read_text(encoding='utf-8')
    
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    if not h1_match:
        errors.append("Falta título H1")
    
    desc_match = re.search(r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*name=["\']description["\']', content, re.IGNORECASE)
    if not desc_match:
        desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
    if not desc_match:
        errors.append("Falta meta description")
    else:
        desc_len = len(desc_match.group(1))
        if desc_len < 70:
            warnings.append(f"Meta description muy corta ({desc_len} chars, mínimo 70)")
        elif desc_len > 160:
            warnings.append(f"Meta description muy larga ({desc_len} chars, máximo 160)")
    
    kw_match = re.search(r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*name=["\']keywords["\']', content, re.IGNORECASE)
    if not kw_match:
        kw_match = re.search(r'<meta[^>]*name=["\']keywords["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
    if not kw_match:
        errors.append("Falta meta keywords")
    else:
        keywords = [k.strip() for k in kw_match.group(1).split(',')]
        keywords = [k for k in keywords if len(k) >= MIN_KEYWORD_LENGTH]
        if len(keywords) < MIN_KEYWORDS:
            errors.append(f"Meta keywords insuficientes ({len(keywords)} palabras, mínimo {MIN_KEYWORDS})")
    
    content_text = re.sub(r'<[^>]+>', '', content)
    content_text = re.sub(r'\s+', ' ', content_text).strip()
    if len(content_text) < MIN_CONTENT_CHARS:
        errors.append(f"Contenido muy corto ({len(content_text)} chars, mínimo {MIN_CONTENT_CHARS})")
    
    images = re.findall(r'<img[^>]*>', content, re.IGNORECASE)
    images_without_alt = [img for img in images if not re.search(r'alt=["\'][^"\']+["\']', img, re.IGNORECASE)]
    if images_without_alt:
        warnings.append(f"{len(images_without_alt)} imágenes sin alt text")
    
    return errors, warnings

def main():
    posts_dir = Path(__file__).parent.parent / 'blog' / 'posts'
    
    if len(sys.argv) > 1:
        html_file = Path(sys.argv[1])
        errors, warnings = validate_post(html_file)
    else:
        errors = []
        warnings = []
        for html_file in posts_dir.glob('*.html'):
            e, w = validate_post(html_file)
            if e or w:
                print(f"\n{html_file.name}:")
                for err in e:
                    print(f"  ❌ {err}")
                for warn in w:
                    print(f"  ⚠️  {warn}")
                errors.extend(e)
                warnings.extend(w)
    
    if not errors and not warnings:
        print("✅ Todos los posts pasan validación SEO")
    elif not errors:
        print(f"⚠️  {len(warnings)} advertencias")
    else:
        print(f"❌ {len(errors)} errores, {len(warnings)} advertencias")
        sys.exit(1)

if __name__ == '__main__':
    main()