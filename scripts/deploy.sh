#!/usr/bin/env bash
# Deploy Jyotish AI to a VPS
# Usage: ssh your-vps 'bash -s' < scripts/deploy.sh
#    or: scp this to VPS and run there

set -euo pipefail

REPO="https://github.com/master12coder/vedic-ai-framework.git"
APP_DIR="$HOME/jyotish"

echo "═══ Jyotish AI — VPS Deployment ═══"

# 1. Install Docker if missing
if ! command -v docker &>/dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker "$USER"
    echo "Docker installed. Log out and back in, then re-run this script."
    exit 0
fi

# 2. Install Docker Compose plugin if missing
if ! docker compose version &>/dev/null; then
    echo "Installing Docker Compose plugin..."
    sudo apt-get update && sudo apt-get install -y docker-compose-plugin
fi

# 3. Clone or update repo
if [ -d "$APP_DIR" ]; then
    echo "Updating existing installation..."
    cd "$APP_DIR"
    git pull origin main
else
    echo "Cloning repository..."
    git clone "$REPO" "$APP_DIR"
    cd "$APP_DIR"
fi

# 4. Check .env exists
if [ ! -f .env ]; then
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env with your tokens:"
    echo "    nano $APP_DIR/.env"
    echo ""
    echo "  Required:"
    echo "    TELEGRAM_BOT_TOKEN=your_botfather_token"
    echo "    TELEGRAM_CHAT_ID=your_chat_id"
    echo ""
    echo "  Optional:"
    echo "    GROQ_API_KEY=your_groq_key"
    echo ""
    echo "Then re-run: cd $APP_DIR && docker compose up -d"
    exit 0
fi

# 5. Save Manish's chart if not exists
mkdir -p charts
if [ ! -f charts/manish.json ]; then
    echo "Computing and saving chart..."
    docker compose run --rm --entrypoint python bot -m jyotish_app.cli.main save \
        --name "Manish Chaurasia" --dob "13/03/1989" --tob "12:17" \
        --place "Varanasi" --gender Male -o charts/manish.json
fi

# 6. Build and start
echo "Building Docker images..."
docker compose build

echo "Starting services..."
docker compose up -d

echo ""
echo "═══ Deployment Complete ═══"
echo ""
echo "Services running:"
docker compose ps
echo ""
echo "Logs: docker compose logs -f"
echo "Stop: docker compose down"
echo ""
echo "Bot: open Telegram, message your bot with /daily"
echo "Scheduler: daily message at 5:30 AM IST"
