#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HERMES_HOME_DIR="$REPO_ROOT/hermes/alexma-clone"

echo "Alexma Clone Hermes setup"
echo "Repo: $REPO_ROOT"
echo "HERMES_HOME: $HERMES_HOME_DIR"

if ! command -v hermes >/dev/null 2>&1; then
  echo "Hermes is not installed."
  echo "Install from official docs:"
  echo "  curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash"
  exit 20
fi

mkdir -p "$HERMES_HOME_DIR/skills"

if [[ ! -f "$HERMES_HOME_DIR/.env" ]]; then
  if [[ -f "$REPO_ROOT/.env" ]]; then
    {
      grep -E '^(ALEX_CLONE_TELEGRAM_BOT_TOKEN|TELEGRAM_BOT_TOKEN)=' "$REPO_ROOT/.env" || true
      echo "TELEGRAM_ALLOWED_USERS="
      echo "ALEX_MIND_VAULT_DIR=/Users/alex/Documents/Alex-Clone/Alex-Mind"
      echo "ALEX_CLONE_GROUPS_CONFIG=$REPO_ROOT/config/groups.json"
      echo "ALEX_CLONE_STATE_DIR=$REPO_ROOT/.alex-clone-state"
    } > "$HERMES_HOME_DIR/.env"
    chmod 600 "$HERMES_HOME_DIR/.env"
    echo "Created local Hermes .env from project .env. Add TELEGRAM_ALLOWED_USERS before running gateway."
  else
    echo "No project .env found. Create $HERMES_HOME_DIR/.env manually."
  fi
fi

echo
echo "Next commands:"
echo "  export HERMES_HOME=\"$HERMES_HOME_DIR\""
echo "  hermes skills list"
echo "  hermes gateway setup"
echo "  hermes gateway"

