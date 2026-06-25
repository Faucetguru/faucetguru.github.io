#!/usr/bin/env python3
"""
Actualizar un post existente en Blogger.
"""
import os
import pickle
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/blogger']
CREDENTIALS_FILE = 'tools/credentials.json'
TOKEN_FILE = 'tools/token.pickle'

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

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 update-blogger-post.py <blog_id> <post_id> '<title>' '<content>'")
        sys.exit(1)
    
    blog_id = sys.argv[1]
    post_id = sys.argv[2]
    title = sys.argv[3]
    content = sys.argv[4]
    
    creds = get_credentials()
    service = build('blogger', 'v3', credentials=creds)
    
    post = service.posts().get(blogId=blog_id, postId=post_id).execute()
    post['title'] = title
    post['content'] = content
    
    result = service.posts().update(blogId=blog_id, postId=post_id, body=post).execute()
    print(f"Post actualizado: {result['url']}")

if __name__ == "__main__":
    main()