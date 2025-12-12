"""
Utility to mint a test JWT for local runs.

Usage (PowerShell):
  python scripts/generate_jwt.py --sub user-1 --role Developer --key keys/dev-jwt.key

Defaults:
  alg: RS256
  exp: now + 24h
"""

import argparse
import datetime as dt
import jwt
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sub", required=True, help="Subject / user id")
    parser.add_argument("--role", required=True, help="Role claim e.g. Developer/ScrumMaster/Admin")
    parser.add_argument("--name", default=None, help="Optional display name")
    parser.add_argument("--key", default="keys/dev-jwt.key", help="Path to RSA private key (PEM)")
    parser.add_argument("--hours", type=int, default=24, help="Expiry in hours from now")
    args = parser.parse_args()

    key_path = Path(args.key)
    if not key_path.exists():
        raise SystemExit(f"Private key not found at {key_path}. Generate one with openssl first.")

    private_key = key_path.read_text(encoding="utf-8")

    now = dt.datetime.utcnow()
    payload = {
        "sub": args.sub,
        "role": args.role,
        "name": args.name,
        "iat": int(now.timestamp()),
        "exp": int((now + dt.timedelta(hours=args.hours)).timestamp()),
    }

    token = jwt.encode(payload, private_key, algorithm="RS256")
    print(token)


if __name__ == "__main__":
    main()
