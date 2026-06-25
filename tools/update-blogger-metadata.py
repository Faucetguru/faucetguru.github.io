#!/usr/bin/env python3
"""
Actualizar posts de Blogger con metadatos SEO.
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
            auth_url, _ = flow.authorization_url(prompt='consent')
            print(f"URL de autorización:\n{auth_url}")
            return None
    return creds

def get_post_metadata(title):
    keywords_map = {
        'my cwallet': 'my cwallet, billetera cripto, faucet wallet, argentina, crypto',
        'realix': 'realix, inversiones cripto, riesgo alto, argentina, crypto',
        'rollercoin': 'rollercoin, simulador minería, bitcoin, ethereum, juegos gratis',
        'scalevance': 'scalevance, ganar cripto, faucet, tareas diarias, argentina',
        'top 10 faucets': 'top 10 faucets, trust score, bitcoin, ethereum, cripto argentina',
        'top69': 'top69, casinos cripto, apuestas cripto, bitcoin, argentina',
        'tronpayu': 'tronpayu, tron, trx, inversiones cripto, estafa',
        'ganar bitcoin gratis desde celular': 'ganar bitcoin gratis, celular, android, faucet, cripto',
        'vie faucet': 'vie faucet, faucet argentina, bitcoin gratis, shortlinks, criptomonedas',
        'wipter': 'wipter, ganar cripto, tareas online, encuestas crypto, argentina'
    }
    
    title_lower = title.lower()
    for key, kw in keywords_map.items():
        if key in title_lower:
            return kw
    return 'criptomonedas, bitcoin, ethereum, argentina, faucet, reseña'

def main():
    creds = get_credentials()
    if not creds:
        print("Autenticación requerida. Usa el script anterior para obtener el token.")
        return
    
    service = build('blogger', 'v3', credentials=creds)
    
    posts = service.posts().list(blogId=BLOG_ID, maxResults=500).execute()
    
    for post in posts.get('items', []):
        title = post.get('title', '')
        post_id = post.get('id')
        labels = post.get('labels', [])
        
        keywords = get_post_metadata(title)
        
        if not labels or len(labels) < 3:
            print(f"Actualizando: {title}")
            post['labels'] = [keywords.split(', ')[0], 'crypto', 'argentina']
            service.posts().update(blogId=BLOG_ID, postId=post_id, body=post).execute()
            print(f"  -> Etiquetas actualizadas: {post['labels']}")
        else:
            print(f"OK: {title} (etiquetas: {labels})")

if __name__ == "__main__":
    main()