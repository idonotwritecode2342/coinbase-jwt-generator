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
