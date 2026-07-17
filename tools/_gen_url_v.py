import json
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/blogger"]
flow = InstalledAppFlow.from_client_secrets_file(
    "tools/credentials.json", SCOPES, redirect_uri="http://localhost"
)
auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
# flow está en estado "pending" luego de authorization_url; el verifier vive en flow
verifier = getattr(flow, "code_verifier", None)
with open("tools/.oauth_verifier.json", "w") as f:
    json.dump({"verifier": verifier}, f)
print("AUTH_URL:" + auth_url)
