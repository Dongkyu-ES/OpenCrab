#!/usr/bin/env bash
# Serve the OpenCrab HTTP API + MCP endpoint (/mcp), bound to the Tailscale
# address only — reachable from the tailnet, invisible to the LAN/internet.
#
# Usage: scripts/serve_mcp_http.sh [port]   (default 8001)
# Requires: OPENCRAB_API_KEY in .env (Bearer auth is fail-closed without it).
set -euo pipefail
cd "$(dirname "$0")/.."

PORT="${1:-8001}"

TAILSCALE_BIN="$(command -v tailscale || echo /Applications/Tailscale.app/Contents/MacOS/Tailscale)"
HOST=""
if [[ -x "$TAILSCALE_BIN" ]]; then
  # At login the LaunchAgent can start before Tailscale is up — wait for it.
  for _ in $(seq 1 30); do
    HOST="$("$TAILSCALE_BIN" ip -4 2>/dev/null | head -1)" && [[ -n "$HOST" ]] && break
    sleep 2
  done
fi
if [[ -n "$HOST" ]]; then
  echo "binding to tailnet address $HOST:$PORT"
else
  HOST="127.0.0.1"
  echo "WARNING: tailscale not available — binding to $HOST:$PORT (local only)" >&2
fi

echo "MCP endpoint:  http://$HOST:$PORT/mcp"
exec .venv/bin/python -m uvicorn server.api:app --host "$HOST" --port "$PORT"
