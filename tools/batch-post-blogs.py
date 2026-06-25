import os
import subprocess
import sys

# Mapping for sorting based on Trust Score analysis
trust_scores = {
    "freebitcoin-reseña.md": 4.9,
    "vie-faucet-reseña.md": 4.9,
    "cointiply-reseña.md": 4.9,
    "rollercoin-reseña.md": 4.7,
    "tronpayu-io-reseña.md": 4.6,
    "faucetcrypto-reseña.md": 4.5,
    "easytrx-io-reseña.md": 4.4,
    "faucetwallet-reseña.md": 4.3,
    "keran-usdt-reseña.md": 4.2,
    "bnbfaucet-doge-reseña.md": 4.1,
    "gamehag-reseña.md": 3.9,
    "scalevance-reseña.md": 3.8,
    "earncrypto-reseña.md": 3.7,
    "grass-reseña.md": 3.6,
    "cashmonster-reseña.md": 3.5,
    "litecoin-farm-online-reseña.md": 3.5,
    "freebtcco-reseña.md": 3.2,
    "litecoin-farm--alerta--reseña.md": 1.5,
}

def get_score(filename):
    return trust_scores.get(filename, 0) # General guides get 0

def post_all(blog_id):
    files = [f for f in os.listdir("blog/markdown") if f.endswith(".md")]
    files.sort(key=get_score, reverse=True)
    
    for filename in files:
        path = os.path.join("blog/markdown", filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Clean up title
        title = filename.replace("-reseña.md", "").replace(".md", "").replace("-", " ").title()
        
        print(f"Posting {title}...")
        
        # Call the existing tool
        # We need to ensure tools/post-to-blogger.py is configured correctly
        # Assuming credentials are already set up and token.pickle exists
        try:
            subprocess.run(["python3", "tools/post-to-blogger.py", blog_id, title, content], check=True)
            print(f"Posted {title} successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to post {title}: {e}")
            # Continue to next if one fails

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 batch-post-blogs.py <blog_id>")
        sys.exit(1)
    post_all(sys.argv[1])
