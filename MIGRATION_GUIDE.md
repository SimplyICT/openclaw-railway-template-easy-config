# Migration Plan: Railway to VPS (aiagent user)

## 1. Prepare Environment (as root)
sudo loginctl enable-linger aiagent

## 2. Sync Files (as aiagent)
cd /data/workspace
git pull origin main
mkdir -p /home/aiagent/.openclaw
cp openclaw.vps.json /home/aiagent/.openclaw/openclaw.json

## 3. Install Service (as aiagent)
mkdir -p ~/.config/systemd/user
cp openclaw-gateway.vps.service ~/.config/systemd/user/openclaw-gateway.service
systemctl --user daemon-reload
systemctl --user enable --now openclaw-gateway

## 4. Verification
systemctl --user status openclaw-gateway
# Access via: http://<SDWAN_IP>:18789
