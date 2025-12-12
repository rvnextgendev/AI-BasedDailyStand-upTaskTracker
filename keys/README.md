# Keys for local testing

The MCP server expects a JWT public key at `keys/jwt.pub` (or via `JWT_PUBLIC_KEY`). For local runs you can generate a throwaway RSA pair and mint a token:

1) Generate RSA key pair (requires OpenSSL):
```
openssl genrsa -out keys/dev-jwt.key 2048
openssl rsa -in keys/dev-jwt.key -pubout -out keys/jwt.pub
```

2) Create a test token (uses pyjwt, already in requirements):
```
python scripts/generate_jwt.py --sub user-1 --role ScrumMaster --name "Dev User" --key keys/dev-jwt.key
```
Copy the printed token and use it as `Authorization: Bearer <token>` when calling MCP tools.

3) Docker Compose will mount `./keys` into the mcp-server container, so `keys/jwt.pub` is picked up automatically by `JWT_PUBLIC_KEY_PATH=/keys/jwt.pub`.

Keep private keys out of production; use real issuer/JWKS there.
