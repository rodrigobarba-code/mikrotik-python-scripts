import os
import requests
from jose import jwt
from dotenv import load_dotenv
from jose.exceptions import JWTError
from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException
from starlette.status import HTTP_403_FORBIDDEN

load_dotenv()

AUTH0_DOMAIN = os.getenv("DOMAIN")
API_AUDIENCE = os.getenv("API_AUDIENCE")
ISSUER = os.getenv("ISSUER")
ALGORITHMS = os.getenv("ALGORITHMS")

security = HTTPBearer()

def get_auth0_jwks():
    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    jwks = requests.get(jwks_url).json()
    return jwks

def verify_jwt(token: str = Depends(security)):
    jwks = get_auth0_jwks()

    try:
        unverified_header = jwt.get_unverified_header(token.credentials)
        rsa_key = {}

        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }

        if rsa_key:
            payload = jwt.decode(
                token.credentials,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/"
            )
            return payload

        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )

    except JWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Invalid token"
        )
