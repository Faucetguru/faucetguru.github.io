import os
import random
import re

blog_dir = 'blog-content-final/'
files = [f for f in os.listdir(blog_dir) if f.endswith('.md')]

reviews = [f for f in files if f.endswith('-reseña.md')]
guides = [f for f in files if f not in reviews and 'Guía' in f or 'Tutorial' in f]
categories = [f for f in files if f not in reviews and f not in guides]

print(f"Reviews: {len(reviews)}")
print(f"Guides: {len(guides)}")
print(f"Categories: {len(categories)}")

def get_title(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        match = re.search(r'^title: "(.*)"', content, re.MULTILINE)
        if match:
            return match.group(1)
        match = re.search(r'^# (.*)', content, re.MULTILINE)
        if match:
            return match.group(1)
    return filepath

def get_natural_link(filename):
    title = get_title(os.path.join(blog_dir, filename))
    # Simplify title for anchor text
    anchor_text = title.replace('Reseña de ', '').replace(':', '').strip()
    return f"[{anchor_text}](./{filename})"

for review in reviews:
    review_path = os.path.join(blog_dir, review)
    
    # Select links
    related_reviews = random.sample([r for r in reviews if r != review], 2)
    main_guide = random.choice(guides)
    category = random.choice(categories)
    
    links = [
        get_natural_link(related_reviews[0]),
        get_natural_link(related_reviews[1]),
        get_natural_link(main_guide),
        get_natural_link(category)
    ]
    
    link_section = "\n### Más contenido recomendado\n\n"
    for link in links:
        link_section += f"- {link}\n"
    link_section += "\n"
    
    # Read and modify
    with open(review_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Inject before "## Registro" if it exists, otherwise at the end
    if "## Registro" in content:
        new_content = content.replace("## Registro", f"{link_section}## Registro")
    else:
        new_content = content + link_section
        
    with open(review_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

print("Done.")
