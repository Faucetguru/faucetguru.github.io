#!/usr/bin/env python3
"""
Generar token OAuth para Google Search Console API (GSC) - sin navegador.

Requiere:
  - tools/credentials.json  (OAuth client, tipo 'installed')
  - google-auth-oauthlib instalado en el venv de research

Uso:
  source .venv-research/bin/activate
  python3 tools/get-gsc-token.py
  -> imprime URL de autorizacion -> abrir en navegador -> pegar codigo -> token guardado

El token se guarda en tools/token_gsc.pickle (chmod 600). Luego research-topics.py
puede leerlo para consultar la Search Console API (searchanalytics).

NOTA: el usuario debe autorizar en el navegador (flujo OAuth). El script solo
prepara la URL y guarda el token; no puede completar el consentimiento solo.
"""
import os
import pickle

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    raise SystemExit("Instala: uv pip install --python .venv-research google-auth-oauthlib")

# Scope de SOLO LECTURA de Search Console (suficiente para searchanalytics)
SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
CREDENTIALS_FILE = 'tools/credentials.json'
TOKEN_FILE = 'tools/token_gsc.pickle'
REDIRECT_URI = 'http://localhost'


def main():
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
    flow.redirect_uri = REDIRECT_URI
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')

    print("=== AUTORIZACION REQUERIDA ===")
    print(f"Abrí esta URL en tu navegador y autoriza el acceso a Search Console:\n\n{auth_url}\n")
    print("Luego pega el codigo de autorizacion (o la URL completa de redireccion) aqui:")
    code = input().strip()

    # Acepta tanto el codigo como la URL completa de redireccion
    if "code=" in code:
        code = code.split("code=", 1)[1].split("&")[0]

    creds = flow.fetch_token(code=code)
    with open(TOKEN_FILE, 'wb') as token:
        pickle.dump(creds, token)
    os.chmod(TOKEN_FILE, 0o600)
    print(f"\nToken GSC guardado en {TOKEN_FILE}")
    print("Ahora research-topics.py puede usar GSC.")


if __name__ == "__main__":
    main()
