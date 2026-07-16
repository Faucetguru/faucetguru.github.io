#!/usr/bin/env python3
"""Generar token OAuth para Google Search Console API (GSC) - flujo PKCE.

Uso:
  uv run python tools/get-gsc-token.py            -> imprime URL de auth (guarda verifier)
  uv run python tools/get-gsc-token.py exchange  -> lee tools/_gsc_code.txt y guarda token

El usuario abre la URL, autoriza, pega el codigo en tools/_gsc_code.txt
(y avisa), y se corre el exchange. El verifier se guarda en tools/_gsc_verifier.txt.
"""
import os, sys, pickle, base64, hashlib, json, urllib.parse, urllib.request

SCOPES = ['https://www.googleapis.com/auth/webmasters']
CREDENTIALS_FILE = 'tools/credentials.json'
TOKEN_FILE = 'tools/token_gsc.pickle'
VERIFIER_FILE = 'tools/_gsc_verifier.txt'
CODE_FILE = 'tools/_gsc_code.txt'
REDIRECT_URI = 'http://localhost'


def gen_url():
    c = json.load(open(CREDENTIALS_FILE))['installed']
    verifier = base64.urlsafe_b64encode(os.urandom(64)).rstrip(b'=').decode('ascii')
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b'=').decode()
    open(VERIFIER_FILE, 'w').write(verifier)
    params = {
        'response_type': 'code', 'client_id': c['client_id'], 'redirect_uri': REDIRECT_URI,
        'scope': SCOPES[0], 'prompt': 'consent', 'access_type': 'offline',
        'code_challenge': challenge, 'code_challenge_method': 'S256',
    }
    url = 'https://accounts.google.com/o/oauth2/auth?' + urllib.parse.urlencode(params)
    open('tools/_gsc_auth_url.txt', 'w').write(url)
    print("=== AUTORIZACION REQUERIDA ===")
    print(url)
    print("\nPega el codigo (o URL de redireccion) en tools/_gsc_code.txt y avisa.")


def do_exchange():
    c = json.load(open(CREDENTIALS_FILE))['installed']
    verifier = open(VERIFIER_FILE).read().strip()
    raw = open(CODE_FILE).read().strip()
    if 'code=' in raw:
        raw = raw.split('code=', 1)[1].split('&')[0]
    data = {
        'code': raw, 'client_id': c['client_id'], 'client_secret': c['client_secret'],
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code', 'code_verifier': verifier,
    }
    req = urllib.request.Request(
        'https://oauth2.googleapis.com/token',
        urllib.parse.urlencode(data).encode(),
        {'Content-Type': 'application/x-www-form-urlencoded'})
    r = json.loads(urllib.request.urlopen(req).read())
    from google.oauth2.credentials import Credentials
    creds = Credentials(
        token=r['access_token'], refresh_token=r.get('refresh_token'),
        token_uri='https://oauth2.googleapis.com/token', client_id=c['client_id'],
        client_secret=c['client_secret'], scopes=SCOPES)
    pickle.dump(creds, open(TOKEN_FILE, 'wb'))
    os.chmod(TOKEN_FILE, 0o600)
    print(f"Token GSC guardado en {TOKEN_FILE}; refresh: {bool(r.get('refresh_token'))}")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'exchange':
        do_exchange()
    else:
        gen_url()
