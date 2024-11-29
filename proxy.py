from flask import Flask, redirect, request, jsonify, session
import requests
from flask_cors import CORS
from base64 import b64encode
import hashlib
import secrets
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clé secrète pour les sessions
CORS(app)

CLIENT_ID = "test-client"
CLIENT_SECRET = "test-secret"
REDIRECT_URI = "http://localhost:5000/callback"
OAUTH_BASE_URL = "http://localhost:3000"

def generate_code_verifier():
    return secrets.token_urlsafe(64)[:128]

def generate_code_challenge(verifier):
    sha256 = hashlib.sha256(verifier.encode('utf-8')).digest()
    return b64encode(sha256).decode('utf-8').replace('+', '-').replace('/', '_').rstrip('=')

@app.route("/oauth")
def oauth():
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    session['code_verifier'] = code_verifier
    
    auth_url = f"{OAUTH_BASE_URL}/auth?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=openid%20profile%20email&code_challenge={code_challenge}&code_challenge_method=S256"
    return redirect(auth_url)

@app.route("/callback", methods=["GET"])
def callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Code manquant"}), 400

    code_verifier = session.get('code_verifier')
    
    token_url = f"{OAUTH_BASE_URL}/token"
    headers = {
        'Authorization': 'Basic ' + b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    }
    
    token_response = requests.post(
        token_url,
        headers=headers,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "code_verifier": code_verifier
        }
    )

    if token_response.status_code != 200:
        return jsonify({"error": "Erreur token", "details": token_response.text}), 500

    tokens = token_response.json()
    access_token = tokens.get("access_token")

    userinfo_url = f"{OAUTH_BASE_URL}/userinfo"
    userinfo_response = requests.get(userinfo_url, headers={"Authorization": f"Bearer {access_token}"})

    if userinfo_response.status_code != 200:
        return jsonify({"error": "Erreur userinfo"}), 500

    return jsonify(userinfo_response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)