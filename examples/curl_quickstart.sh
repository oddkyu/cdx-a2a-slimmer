#!/usr/bin/env bash
# Test CDX A2A Slimmer Proxy via cURL
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hello via CDX Sidecar!"}]
  }'
