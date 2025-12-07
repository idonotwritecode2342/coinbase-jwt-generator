import os
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from coinbase import jwt_generator
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Trading Helpers API")


class JWTRequest(BaseModel):
    method: str
    uri: str


def require_api_key(x_api_key: str | None = Header(default=None)):
    """Check API key against SERVICE_API_KEY."""
    expected = os.getenv("SERVICE_API_KEY")
    if not expected:
        raise HTTPException(status_code=500, detail="SERVICE_API_KEY not configured on server")
    if not x_api_key or x_api_key != expected:
        raise HTTPException(status_code=401, detail="Unauthorized: invalid or missing x-api-key")


@app.post("/generate-jwt")
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


@app.get("/")
async def root() -> dict:
    """Health check endpoint."""
    return {"message": "AI Trading Helpers API is running"}
