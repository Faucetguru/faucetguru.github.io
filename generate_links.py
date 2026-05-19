
import os
import random

blog_dir = '/home/salmarina/Faucetguru_site/blog-content-final'
files = os.listdir(blog_dir)

reviews = [f for f in files if f.endswith('-reseña.md')]
guides = [f for f in files if not f.endswith('-reseña.md')]

# Map review to a "category" based on filename or just generic "faucet" etc.
# For simplicity, let's just categorize them by "faucets", "mining", "ptc"
def get_category(filename):
    if 'mining' in filename.lower():
        return 'Minería'
    if 'ptc' in filename.lower():
        return 'PTC'
    return 'Faucets'

def get_link_text(filename):
    # Make a nice title from filename
    name = filename.replace('-reseña.md', '').replace('.md', '').replace('-', ' ').title()
    return name

def generate_links(current_file):
    related_reviews = random.sample([r for r in reviews if r != current_file], 2)
    main_guide = random.choice(guides)
    category = get_category(current_file)
    
    links = []
    links.append(f"- Más reseñas relacionadas: [{get_link_text(related_reviews[0])}](/blog-content-final/{related_reviews[0]}) y [{get_link_text(related_reviews[1])}](/blog-content-final/{related_reviews[1]})")
    links.append(f"- Guía recomendada: [{get_link_text(main_guide)}](/blog-content-final/{main_guide})")
    links.append(f"- Ver más en la categoría: {category}")
    
    return "\n".join(links)

for review in reviews:
    print(f"Processing {review}...")
    # Read the file
    # (Since I'm in a shell, I will just print the links and I will use the 'edit' tool later)
    # Actually, the user asked me to "implement" this.
    # I will have to do it file by file with `edit`.
    # Let's print the links I would add.
    print(generate_links(review))
    print("-" * 20)
