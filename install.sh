#!/usr/bin/env bash
# Obsidian Growth Kit — Installer
# Sets up all CLI tools, config directories, and cron templates
set -euo pipefail

PURPLE='\033[1;35m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
DIM='\033[2m'
RESET='\033[0m'
BOLD='\033[1m'

echo ""
echo -e "${PURPLE}⚫ Obsidian Growth Kit${RESET} — Installer"
echo -e "${DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo ""

# Check dependencies
echo -e "${CYAN}Checking dependencies...${RESET}"
missing=()
command -v python3 >/dev/null 2>&1 || missing+=("python3")
command -v pip3 >/dev/null 2>&1 || missing+=("pip3")
command -v git >/dev/null 2>&1 || missing+=("git")

if [ ${#missing[@]} -ne 0 ]; then
  echo -e "\n${BOLD}Missing required tools:${RESET} ${missing[*]}"
  echo "Please install them and re-run this script."
  exit 1
fi
echo -e "${GREEN}  All dependencies found.${RESET}"

# Install Python packages
echo ""
echo -e "${CYAN}Installing Python dependencies...${RESET}"
pip3 install --break-system-packages tweepy asciinema 2>/dev/null || pip3 install tweepy asciinema
echo -e "${GREEN}  Python packages installed.${RESET}"

# Create config directories
echo ""
echo -e "${CYAN}Setting up config directories...${RESET}"
mkdir -p ~/.config/x-api
mkdir -p ~/.local/bin
echo -e "${GREEN}  Config directories created.${RESET}"

# Install tools
echo ""
echo -e "${CYAN}Installing CLI tools...${RESET}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for tool in xpost xqueue xanalytics xscout xgrowth xrecord; do
  if [ -f "$SCRIPT_DIR/tools/$tool" ]; then
    cp "$SCRIPT_DIR/tools/$tool" ~/.local/bin/$tool
    chmod +x ~/.local/bin/$tool
    echo -e "  ${GREEN}✓${RESET} $tool installed"
  else
    echo -e "  ${DIM}⊘ $tool not found in tools/${RESET}"
  fi
done

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
  echo ""
  echo -e "${BOLD}Add this to your shell profile (~/.bashrc or ~/.zshrc):${RESET}"
  echo '  export PATH="$HOME/.local/bin:$PATH"'
fi

# API key setup
echo ""
echo -e "${CYAN}Setting up X API credentials...${RESET}"
KEYS_FILE="$HOME/.config/x-api/keys.env"
if [ -f "$KEYS_FILE" ]; then
  echo -e "  ${DIM}Keys file already exists at $KEYS_FILE${RESET}"
else
  cat > "$KEYS_FILE" << 'KEYS'
# X/Twitter API Credentials
# Get these from https://developer.x.com/en/portal/dashboard
X_API_KEY=your_api_key
X_API_SECRET=your_api_secret
TWITTER_BEARER_TOKEN=your_bearer_token
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
X_USER_HANDLE=YourHandle
KEYS
  echo -e "  ${GREEN}✓${RESET} Template created at $KEYS_FILE"
  echo -e "  ${BOLD}Edit this file with your X API credentials before using the tools.${RESET}"
fi

# Copy templates
echo ""
echo -e "${CYAN}Installing templates...${RESET}"
if [ -d "$SCRIPT_DIR/templates" ]; then
  for tmpl in "$SCRIPT_DIR/templates"/*; do
    if [ -f "$tmpl" ]; then
      basename=$(basename "$tmpl")
      cp "$tmpl" ~/.config/x-api/$basename
      echo -e "  ${GREEN}✓${RESET} $basename"
    fi
  done
fi

echo ""
echo -e "${DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${GREEN}${BOLD}Installation complete!${RESET}"
echo ""
echo -e "Next steps:"
echo -e "  1. Edit ${BOLD}~/.config/x-api/keys.env${RESET} with your X API credentials"
echo -e "  2. Run ${BOLD}xpost whoami${RESET} to verify connection"
echo -e "  3. Read ${BOLD}docs/QUICKSTART.md${RESET} to get started"
echo -e "  4. Run ${BOLD}xqueue add \"your first tweet\"${RESET} to queue a post"
echo ""
echo -e "${PURPLE}⚫ Obsidian Growth Kit${RESET} — ${DIM}https://jadye527.github.io/obsidian-trading${RESET}"
echo ""
