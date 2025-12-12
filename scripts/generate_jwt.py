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


def prompt_text(label, default=None, required=False):
    """Prompt the user when a flag is missing."""
    prompt = f"{label}"
    if default is not None:
        prompt += f" [{default}]"
    prompt += ": "
    while True:
        value = input(prompt).strip()
        if value:
            return value
        if default is not None:
            return default
        if not required:
            return None
        print("This value is required.")


def prompt_int(label, default=None):
    """Prompt for an integer with optional default."""
    prompt = f"{label}"
    if default is not None:
        prompt += f" [{default}]"
    prompt += ": "
    while True:
        value = input(prompt).strip()
        if not value and default is not None:
            return default
        try:
            return int(value)
        except ValueError:
            print("Please enter a number.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sub", required=False, help="Subject / user id")
    parser.add_argument("--role", required=False, help="Role claim e.g. Developer/ScrumMaster/Admin")
    parser.add_argument("--name", default=None, help="Optional display name")
    parser.add_argument("--key", default=None, help="Path to RSA private key (PEM)")
    parser.add_argument("--hours", type=int, default=None, help="Expiry in hours from now")
    args = parser.parse_args()

    sub = args.sub or prompt_text("Subject / user id", required=True)
    role = args.role or prompt_text("Role", default="Developer", required=True)
    name = args.name if args.name is not None else prompt_text("Display name (optional)")
    hours = args.hours if args.hours is not None else prompt_int("Expiry in hours from now", default=24)
    key_value = args.key or prompt_text("Path to RSA private key (PEM)", default="keys/dev-jwt.key", required=True)

    key_path = Path(key_value)
    if not key_path.exists():
        raise SystemExit(f"Private key not found at {key_path}. Generate one with openssl first.")

    private_key = key_path.read_text(encoding="utf-8")

    now = dt.datetime.utcnow()
    payload = {
        "sub": sub,
        "role": role,
        "name": name,
        "iat": int(now.timestamp()),
        "exp": int((now + dt.timedelta(hours=hours)).timestamp()),
    }

    token = jwt.encode(payload, private_key, algorithm="RS256")
    print(token)


if __name__ == "__main__":
    main()
