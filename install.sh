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

CONFIG_DIR="${HOME:?}/.config/x-api"
BIN_DIR="${HOME}/.local/bin"
SYSTEMD_USER_DIR="${HOME}/.config/systemd/user"
SCHEDULER_NAME="obsidian-growth-kit-post"
SERVICE_FILE="${SYSTEMD_USER_DIR}/${SCHEDULER_NAME}.service"
TIMER_FILE="${SYSTEMD_USER_DIR}/${SCHEDULER_NAME}.timer"
CRON_BLOCK_START="# BEGIN_OBSIDIAN_GROWTH_KIT_DAILY_POSTING"
CRON_BLOCK_END="# END_OBSIDIAN_GROWTH_KIT_DAILY_POSTING"

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
mkdir -p "$CONFIG_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$SYSTEMD_USER_DIR"
echo -e "${GREEN}  Config directories created.${RESET}"

# Install tools
echo ""
echo -e "${CYAN}Installing CLI tools...${RESET}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for tool in xpost xqueue xanalytics xscout xgrowth xcron xrecord xmiddleware xcleanup xmeme; do
  if [ -f "$SCRIPT_DIR/tools/$tool" ]; then
    cp "$SCRIPT_DIR/tools/$tool" "$BIN_DIR/$tool"
    chmod +x "$BIN_DIR/$tool"
    echo -e "  ${GREEN}✓${RESET} $tool installed"
  else
    echo -e "  ${DIM}⊘ $tool not found in tools/${RESET}"
  fi
done

# Check if the local bin directory is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
  echo ""
  echo -e "${BOLD}Add this to your shell profile (\$HOME/.bashrc or \$HOME/.zshrc):${RESET}"
  echo '  export PATH="$HOME/.local/bin:$PATH"'
fi

# API key setup
echo ""
echo -e "${CYAN}Setting up X API credentials...${RESET}"
KEYS_FILE="$CONFIG_DIR/keys.env"
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
      cp "$tmpl" "$CONFIG_DIR/$basename"
      echo -e "  ${GREEN}✓${RESET} $basename"
    fi
  done
fi

SCHEDULE_COMMAND="PATH=\"$BIN_DIR:/usr/local/bin:/usr/bin:/bin\" X_QUEUE_FILE=\"$CONFIG_DIR/queue.json\" X_KEYS_FILE=\"$KEYS_FILE\" xqueue next >/dev/null 2>&1"

install_systemd_timer() {
  cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=Obsidian Growth Kit scheduled posting

[Service]
Type=oneshot
ExecStart=/bin/sh -lc 'PATH="$BIN_DIR:/usr/local/bin:/usr/bin:/bin"; export PATH X_QUEUE_FILE="$CONFIG_DIR/queue.json" X_KEYS_FILE="$KEYS_FILE"; exec xqueue next'
EOF

  cat > "$TIMER_FILE" <<EOF
[Unit]
Description=Obsidian Growth Kit scheduled posting timer

[Timer]
OnCalendar=*-*-* 09:00:00 America/New_York
OnCalendar=*-*-* 18:00:00 America/New_York
Persistent=true
Unit=${SCHEDULER_NAME}.service

[Install]
WantedBy=timers.target
EOF

  systemctl --user daemon-reload
  systemctl --user enable --now "${SCHEDULER_NAME}.timer"
}

install_crontab_schedule() {
  local current_crontab
  local filtered_crontab
  current_crontab="$(mktemp)"
  filtered_crontab="$(mktemp)"

  if ! crontab -l > "$current_crontab" 2>/dev/null; then
    : > "$current_crontab"
  fi

  awk -v start="$CRON_BLOCK_START" -v end="$CRON_BLOCK_END" '
    $0 == start { skip=1; next }
    $0 == end { skip=0; next }
    !skip { print }
  ' "$current_crontab" > "$filtered_crontab"

  {
    cat "$filtered_crontab"
    printf "%s\n" "$CRON_BLOCK_START"
    printf "%s\n" "CRON_TZ=America/New_York"
    printf "%s\n" "0 9,18 * * * $SCHEDULE_COMMAND"
    printf "%s\n" "$CRON_BLOCK_END"
  } | crontab -

  rm -f "$current_crontab" "$filtered_crontab"
}

echo ""
echo -e "${CYAN}Configuring scheduled posting...${RESET}"
if command -v systemctl >/dev/null 2>&1; then
  if install_systemd_timer; then
    echo -e "  ${GREEN}✓${RESET} systemd timer installed at 9:00 AM and 6:00 PM ET"
  else
    echo -e "  ${DIM}systemd timer setup failed, falling back to crontab${RESET}"
    if command -v crontab >/dev/null 2>&1; then
      install_crontab_schedule
      echo -e "  ${GREEN}✓${RESET} crontab installed at 9:00 AM and 6:00 PM ET"
    else
      echo -e "  ${DIM}No systemctl or crontab found. Skipping scheduler setup.${RESET}"
    fi
  fi
elif command -v crontab >/dev/null 2>&1; then
  install_crontab_schedule
  echo -e "  ${GREEN}✓${RESET} crontab installed at 9:00 AM and 6:00 PM ET"
else
  echo -e "  ${DIM}No systemctl or crontab found. Skipping scheduler setup.${RESET}"
fi

echo ""
echo -e "${DIM}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${GREEN}${BOLD}Installation complete!${RESET}"
echo ""
echo -e "Next steps:"
echo -e "  1. Edit ${BOLD}$KEYS_FILE${RESET} with your X API credentials"
echo -e "  2. Run ${BOLD}xpost whoami${RESET} to verify connection"
echo -e "  3. Read ${BOLD}docs/QUICKSTART.md${RESET} to get started"
echo -e "  4. Run ${BOLD}xqueue add \"your first tweet\"${RESET} to queue a post"
echo ""
echo -e "${PURPLE}⚫ Obsidian Growth Kit${RESET} — ${DIM}https://jadye527.github.io/obsidian-trading${RESET}"
echo ""
