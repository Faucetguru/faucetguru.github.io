import sys, pickle
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/blogger"]

# Generar flujo (guarda code_verifier internamente para PKCE)
flow = InstalledAppFlow.from_client_secrets_file(
    "tools/credentials.json", SCOPES, redirect_uri="http://localhost"
)
auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
print("AUTH_URL:" + auth_url)
print("PEGÁ_EL_CODIGO_Y_PULSA_ENTER:")
code = sys.stdin.readline().strip()
if not code:
    print("NO_CODE"); sys.exit(1)
flow.fetch_token(code=code)
with open("tools/token.pickle", "wb") as f:
    pickle.dump(flow.credentials, f)
print("TOKEN_OK")
