import os
import hashlib
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from coinbase import jwt_generator
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="AI Trading Helpers API",
    description="A collection of helper APIs for AI trading workflows.",
    version="1.0.0",
)

# -----------------------------------------------------------------------------
# Data Models
# -----------------------------------------------------------------------------

class JWTRequest(BaseModel):
    method: str
    uri: str


# -----------------------------------------------------------------------------
# Auth & Helpers
# -----------------------------------------------------------------------------

def require_api_key(x_api_key: str | None = Header(default=None)):
    """Check API key against SERVICE_API_KEY."""
    expected = os.getenv("SERVICE_API_KEY")
    if not expected:
        raise HTTPException(status_code=500, detail="SERVICE_API_KEY not configured on server")
    if not x_api_key or x_api_key != expected:
        raise HTTPException(status_code=401, detail="Unauthorized: invalid or missing x-api-key")


# -----------------------------------------------------------------------------
# API Endpoints
# -----------------------------------------------------------------------------

@app.post(
    "/generate-jwt",
    tags=["Coinbase"],
    summary="Generate Coinbase JWT",
    description="Generates a JWT token for authenticating with Coinbase Advanced Trade API.",
)
async def generate_jwt(request: JWTRequest, x_api_key: str | None = Header(default=None)) -> dict:
    # Enforce simple API key auth via header
    require_api_key(x_api_key)
    """Generate a Coinbase JWT token for the given method and URI."""
    try:
        api_key = os.getenv("COINBASE_API_KEY")
        api_secret = os.getenv("COINBASE_API_SECRET")

        if not api_key or not api_secret:
            raise HTTPException(
                status_code=500,
                detail="Missing COINBASE_API_KEY or COINBASE_API_SECRET environment variables",
            )

        # Convert escaped newlines (\n) to actual newlines
        api_secret = api_secret.replace("\\n", "\n")

        jwt_uri = jwt_generator.format_jwt_uri(request.method, request.uri)
        jwt_token = jwt_generator.build_rest_jwt(jwt_uri, api_key, api_secret)

        return {"jwt": jwt_token}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate JWT: {str(e)}",
        )


@app.get(
    "/get-sha256",
    tags=["Zerodha"],
    summary="Calculate Zerodha Checksum",
    description="Calculates SHA-256 checksum of KITE_API_KEY + REQUEST + KITE_API_SECRET.",
)
async def get_sha256(x_api_key: str | None = Header(default=None)) -> dict:
    require_api_key(x_api_key)
    try:
        kite_api_key = os.getenv("KITE_API_KEY")
        request_token = os.getenv("REQUEST")
        kite_api_secret = os.getenv("KITE_API_SECRET")

        if not kite_api_key or not request_token or not kite_api_secret:
            raise HTTPException(
                status_code=500,
                detail="Missing KITE_API_KEY, REQUEST, or KITE_API_SECRET environment variables",
            )
        
        # Checksum = SHA256(api_key + request_token + api_secret)
        data = f"{kite_api_key}{request_token}{kite_api_secret}"
        checksum = hashlib.sha256(data.encode("utf-8")).hexdigest()

        return {"checksum": checksum}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate checksum: {str(e)}",
        )


@app.get("/", tags=["Health"], summary="Health Check")
async def root() -> dict:
    """Health check endpoint."""
    return {"message": "AI Trading Helpers API is running"}
