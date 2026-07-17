import sys, json, pickle
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/blogger"]
flow = InstalledAppFlow.from_client_secrets_file(
    "tools/credentials.json", SCOPES, redirect_uri="http://localhost"
)
# restaurar el code_verifier para PKCE
try:
    with open("tools/.oauth_verifier.json") as f:
        verifier = json.load(f).get("verifier")
    flow.code_verifier = verifier
except Exception as e:
    print("NO_VERIFIER", e); sys.exit(1)

code = sys.argv[1] if len(sys.argv) > 1 else ""
if not code:
    print("USO: python3 tools/_gen_token_v.py <CODIGO>"); sys.exit(1)
flow.fetch_token(code=code)
with open("tools/token.pickle", "wb") as f:
    pickle.dump(flow.credentials, f)
print("TOKEN_OK")
