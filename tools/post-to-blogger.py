#!/usr/bin/env python3
import os
import pickle
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Configuration
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
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def post_to_blogger(blog_id, title, content):
    creds = get_credentials()
    service = build('blogger', 'v3', credentials=creds)

    post_body = {
        'kind': 'blogger#post',
        'title': title,
        'content': content
    }

    # Execute request
    result = service.posts().insert(blogId=blog_id, body=post_body).execute()
    print(f"Post created successfully! Post ID: {result['id']}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 post-to-blogger.py <blog_id> '<title>' '<body>'")
        sys.exit(1)
    
    blog_id = sys.argv[1]
    title = sys.argv[2]
    content = sys.argv[3]
    
    post_to_blogger(blog_id, title, content)
