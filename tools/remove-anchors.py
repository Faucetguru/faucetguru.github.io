#!/usr/bin/env python3
import os
import re
from pathlib import Path

def remove_hrefs_from_html(content):
    pattern = r'<a\s+href="[^"]*"\s*([^>]*)>'
    replacement = '<span\1>'
    return re.sub(pattern, replacement, content, flags=re.IGNORECASE)

def remove_closing_anchors(content):
    return re.sub(r'</a>', '', content, flags=re.IGNORECASE)

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    content = remove_hrefs_from_html(content)
    content = remove_closing_anchors(content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    blog_posts_dir = Path(__file__).parent.parent / 'blog' / 'posts'
    
    if not blog_posts_dir.exists():
        print(f"Directorio no encontrado: {blog_posts_dir}")
        return
    
    modified_count = 0
    for html_file in blog_posts_dir.glob('*.html'):
        # Skip index.html - only process individual posts
        if html_file.name == 'index.html':
            print(f"Saltado: {html_file.name} (index no procesado)")
            continue
        if process_html_file(html_file):
            print(f"Procesado: {html_file.name}")
            modified_count += 1
    
    print(f"\nTotal: {modified_count} archivos modificados")

if __name__ == '__main__':
    main()