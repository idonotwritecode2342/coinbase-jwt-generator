import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from coinbase import jwt_generator
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Coinbase JWT Generator")


class JWTRequest(BaseModel):
    method: str
    uri: str


@app.post("/generate-jwt")
async def generate_jwt(request: JWTRequest) -> dict:
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
    return {"message": "Coinbase JWT Generator API is running"}
