# AI Trading Helpers

A collection of APIs to assist with AI trading tasks.

## Functionality

### Coinbase JWT Generator
Generates JWT tokens for Coinbase Advanced Trade API.

**Endpoint**: `POST /generate-jwt`

**Headers**:
- `x-api-key`: Service API key

**Body**:
```json
{
  "method": "GET",
  "uri": "/api/v3/brokerage/accounts"
}
```

### Zerodha Kite Checksum
Calculates SHA-256 checksum for Zerodha Kite Connect authentication.

**Endpoint**: `GET /get-sha256`

**Headers**:
- `x-api-key`: Service API key

**Environment Variables Required**:
- `KITE_API_KEY`: Your Zerodha Kite API Key
- `REQUEST`: The request token obtained from the login flow
- `KITE_API_SECRET`: Your Zerodha Kite API Secret

**Response**:
```json
{
  "checksum": "sha256_hash_value"
}
```
