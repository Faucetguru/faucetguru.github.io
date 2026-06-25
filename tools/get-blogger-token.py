#!/usr/bin/env python3
"""
Generar token OAuth para Blogger API - sin navegador
"""

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/blogger']
CREDENTIALS_FILE = 'tools/credentials.json'
TOKEN_FILE = 'tools/token.pickle'
REDIRECT_URI = 'http://localhost'

def main():
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
    flow.redirect_uri = REDIRECT_URI
    auth_url, _ = flow.authorization_url(prompt='consent')
    
    print(f"URL de autorización:\n{auth_url}\n")
    print("Ingresa el código de autorización aquí: ")
    code = input().strip()
    
    creds = flow.fetch_token(code=code)
    with open(TOKEN_FILE, 'wb') as token:
        pickle.dump(creds, token)
    print(f"Token guardado en {TOKEN_FILE}")

if __name__ == "__main__":
    main()