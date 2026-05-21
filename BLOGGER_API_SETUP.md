# Blogger API v3 Setup and Usage

This document outlines the steps to use the modern Google Blogger API v3 with this project, migrating away from deprecated GData-based tools.

## 1. Google Cloud Console Setup

1.  **Create a Project:** In the [Google Cloud Console](https://console.cloud.google.com/), create a new project.
2.  **Enable API:** Search for "Blogger API v3" and enable it for your project.
3.  **OAuth Consent Screen:** Configure the OAuth consent screen (Internal or External).
4.  **Create Credentials:**
    *   Go to **Credentials** -> **Create Credentials** -> **OAuth client ID**.
    *   Select **Desktop app**.
    *   Download the resulting `credentials.json` file.
5.  **Place the file:** Save the downloaded `credentials.json` in the `tools/` folder as `tools/credentials.json`.

## 2. Dependencies

Install the required Google API libraries:

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## 3. Tool Implementation (`tools/post-to-blogger.py`)

The script `tools/post-to-blogger.py` handles authentication and posting to Blogger.

```python
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
```

## 4. Usage

To post to your blog:
1.  Find your `blog_id` from the URL of your Blogger dashboard.
2.  Run the tool:
    ```bash
    python3 tools/post-to-blogger.py YOUR_BLOG_ID 'Post Title' 'Post content here.'
    ```

*Note: On the first run, it will open a browser to complete the OAuth flow. It creates `tools/token.pickle` to securely store credentials for future runs.*
