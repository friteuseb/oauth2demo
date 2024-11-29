# OAuth 2.0 Demo with OIDC Provider

This demo showcases OAuth 2.0 and OpenID Connect authentication flow with three components:
- OIDC Provider (NodeJS)
- Proxy Server (Python/Flask)
- Client Application (PHP)

## Prerequisites

- Node.js (v14+)
- Python 3.10+
- PHP 7.4+
- npm or yarn

## Installation

1. Install OIDC Provider dependencies:
```bash
npm install oidc-provider
```

2. Install Python dependencies:
```bash
pip install flask flask-cors requests
```

3. Configure PHP:
- Ensure you have PHP's built-in server or Apache/Nginx configured

## Configuration

All servers use default configurations:
- OIDC Provider: http://localhost:3000
- Proxy Server: http://localhost:5000
- PHP Client: http://localhost:8000

## Running the Demo

1. Start the OIDC Provider:
```bash
node server.mjs
```

2. Start the Proxy Server:
```bash
python proxy.py
```

3. Start the PHP Client:
```bash
php -S localhost:8000
```

4. Access http://localhost:8000 in your browser

## Flow

1. Client redirects to proxy (/oauth)
2. Proxy initiates PKCE flow with OIDC Provider
3. User authenticates
4. Provider redirects back with auth code
5. Proxy exchanges code for tokens
6. Client displays user information

## Troubleshooting

- Ensure all servers are running
- Check port availability
- Verify client_id and client_secret match in server.mjs and proxy.py
- Clear browser cookies if authentication fails
