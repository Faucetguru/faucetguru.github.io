from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/blogger"]

# redirect_uri registrado en credentials.json es "http://localhost"
flow = InstalledAppFlow.from_client_secrets_file(
    "tools/credentials.json", SCOPES, redirect_uri="http://localhost"
)
auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
print("AUTH_URL:" + auth_url)
print("REDIRECT_ESPERADO:http://localhost")
