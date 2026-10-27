#!/bin/zsh
cd "${0:A:h}"
RUNTIME="${HUNTER_PYTHON:-python3}"
if [[ -z "$HUNTER_PYTHON" && -x "$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3" ]]; then
  RUNTIME="$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
fi
exec "$RUNTIME" backend/server.py
