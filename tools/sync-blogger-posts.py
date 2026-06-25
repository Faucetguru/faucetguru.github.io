#!/usr/bin/env python3
"""
Sincronizar posts de Blogger API con archivos locales.
Lee posts de Blogger, compara con archivos locales y actualiza los incompletos.
"""

import os
import pickle
import re
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/blogger']
CREDENTIALS_FILE = 'tools/credentials.json'
TOKEN_FILE = 'tools/token.pickle'
BLOG_ID = os.getenv('BLOGGER_BLOG_ID', 'G-F7ZG182KN2')
POSTS_DIR = 'blog/posts'

TRANSLATIONS = {
    'ready wallet': 'Ready Wallet',
    'backpack wallet': 'Backpack Wallet',
    'wipter': 'Wipter',
    'makeyoutask': 'MakeYouTask',
    'coinpayu': 'Coinpayu',
    'freebtcco': 'FreeBTCCO',
    'litecoin farm': 'Litecoin Farm',
    'ltcminer': 'LTCMiner',
    'cashmonster': 'CashMonster',
    'easytrx': 'EasyTrx',
    'freetron': 'FreeTRON',
    'bnbfaucet': 'BNBfaucet',
    'keran': 'Keran',
    'luckywatch': 'LuckyWatch',
    'earncrypto': 'EarnCrypto',
    'autofaucet dutchycorp': 'Autofaucet DutchyCorp',
    'faucetcrypto': 'FaucetCrypto',
    'faucetpay': 'FaucetPay',
    'faucetwallet': 'FaucetWallet',
    'freebitco': 'FreeBitco.in',
    'gamehag': 'Gamehag',
    'grass': 'Grass',
    'multiminer': 'Multiminer',
    'my cwallet': 'My CWallet',
    'realix': 'Realix',
    'rollercoin': 'RollerCoin',
    'scalevance': 'Scalevance',
    'top69': 'TOP69',
    'tronpayu': 'Tronpayu',
    'vie faucet': 'Vie Faucet',
}

def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            flow.redirect_uri = 'http://localhost'
            auth_url, _ = flow.authorization_url(prompt='consent')
            print(f"URL de autorización:\n{auth_url}\n")
            print("Ingresa el código de autorización aquí: ")
            code = input().strip()
            creds = flow.fetch_token(code=code)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def extract_title(html):
    match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
    return match.group(1).strip() if match else None

def extract_keywords(html):
    match = re.search(r'<meta[^>]*name=["\']keywords["\'][^>]*content=["\']([^"\']+)["\']', html, re.IGNORECASE)
    return match.group(1) if match else None

def extract_description(html):
    match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', html, re.IGNORECASE)
    return match.group(1) if match else None

def generate_keywords(title, content):
    keywords = ['cripto argentina', 'faucet', 'criptomonedas', 'crypto']
    title_lower = title.lower()
    for key, translation in TRANSLATIONS.items():
        if key in title_lower:
            keywords.append(translation.lower())
    if 'bitcoin' in title_lower or 'btc' in title_lower:
        keywords.extend(['bitcoin', 'btc'])
    if 'ethereum' in title_lower:
        keywords.append('ethereum')
    if 'tron' in title_lower or 'trx' in title_lower:
        keywords.extend(['tron', 'trx'])
    if 'wallet' in title_lower:
        keywords.extend(['wallet', 'billetera cripto'])
    if 'testnet' in title_lower or 'prueba' in title_lower:
        keywords.extend(['testnet', 'tokens gratis'])
    return ', '.join(set(keywords))

def generate_description(title, content):
    text = re.sub(r'<[^>]+>', '', content)
    text = re.sub(r'\s+', ' ', text).strip()
    desc = text[:150] + '...' if len(text) > 150 else text
    return desc

def update_post(service, post_id, title, keywords, description):
    try:
        post = service.posts().get(blogId=BLOG_ID, postId=post_id).execute()
        updated = False
        if not post.get('labels') or len(post.get('labels', [])) < 3:
            post['labels'] = keywords.split(', ')[:3]
            updated = True
        if not post.get('searchMetadata', {}).get('searchDescription'):
            if 'searchMetadata' not in post:
                post['searchMetadata'] = {}
            post['searchMetadata']['searchDescription'] = description
            updated = True
        if updated:
            service.posts().update(blogId=BLOG_ID, postId=post_id, body=post).execute()
            return True
    except Exception as e:
        print(f"  Error actualizando {post_id}: {e}")
    return False

def main():
    creds = get_credentials()
    if not creds:
        return
    
    service = build('blogger', 'v3', credentials=creds)
    
    print("Leyendo posts de Blogger API...")
    posts = service.posts().list(blogId=BLOG_ID, maxResults=500).execute()
    
    updated_count = 0
    for post in posts.get('items', []):
        post_id = post.get('id')
        title = post.get('title', '')
        
        keywords = post.get('labels', [])
        description = post.get('searchMetadata', {}).get('searchDescription', '')
        
        if not keywords or len(keywords) < 3 or not description:
            print(f"Post ID {post_id}: {title}")
            print(f"  Keywords actuales: {keywords}")
            print(f"  Description actual: {description[:50] if description else 'N/A'}...")
            
            html_file = None
            for f in os.listdir(POSTS_DIR):
                if f.replace('.html', '').lower().replace(' ', '-').replace('¿', '').replace('?', '') in title.lower():
                    html_file = os.path.join(POSTS_DIR, f)
                    break
            
            if not html_file:
                for f in os.listdir(POSTS_DIR):
                    if f.endswith('.html'):
                        html_file = os.path.join(POSTS_DIR, f)
                        break
            
            if html_file and os.path.exists(html_file):
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                new_keywords = generate_keywords(title, content)
                new_description = generate_description(title, content)
                
                if update_post(service, post_id, title, new_keywords, new_description):
                    print(f"  ✓ Actualizado")
                    updated_count += 1
                else:
                    print(f"  - Sin cambios necesarios")
    
    print(f"\nTotal actualizados: {updated_count}")

if __name__ == "__main__":
    main()