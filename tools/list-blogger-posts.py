#!/usr/bin/env python3
"""
Listar todos los posts de Blogger usando la API.
"""

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/blogger']
CREDENTIALS_FILE = 'tools/credentials.json'
TOKEN_FILE = 'tools/token.pickle'
BLOG_ID = os.getenv('BLOGGER_BLOG_ID', 'G-F7ZG182KN2')
REDIRECT_URI = 'http://localhost'

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
            flow.redirect_uri = REDIRECT_URI
            auth_url, _ = flow.authorization_url(prompt='consent')
            print(f"URL de autorización:\n{auth_url}\n")
            print("Ingresa el código de autorización aquí: ")
            code = input().strip()
            creds = flow.fetch_token(code=code)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def main():
    creds = get_credentials()
    service = build('blogger', 'v3', credentials=creds)
    
    posts = service.posts().list(blogId=BLOG_ID, maxResults=500).execute()
    
    print(f"Total posts en Blogger: {posts.get('totalItems', 0)}\n")
    
    for post in posts.get('items', []):
        print(f"Título: {post.get('title', 'Sin título')}")
        print(f"  ID: {post.get('id')}")
        print(f"  URL: {post.get('url')}")
        print(f"  Etiquetas: {post.get('labels', [])}")
        print(f"  Created: {post.get('created')}")
        print()

if __name__ == "__main__":
    main()