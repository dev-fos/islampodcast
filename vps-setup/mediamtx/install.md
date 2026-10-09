sudo apt update && sudo apt upgrade -y

sudo apt install -y wget tar ffmpeg

cd /tmp

wget https://github.com/bluenviron/mediamtx/releases/download/v1.21.1/mediamtx_v1.21.1_linux_amd64.tar.gz

tar -xzf mediamtx_v1.21.1_linux_amd64.tar.gz

sudo mv mediamtx /usr/local/bin/

sudo mkdir -p /etc/mediamtx

sudo mv mediamtx.yml /etc/mediamtx/


sudo chmod +x /usr/local/bin/mediamtx


sudo tee /etc/systemd/system/mediamtx.service > /dev/null <<'EOF'
[Unit]
Description=MediaMTX streaming server
After=network.target

[Service]
ExecStart=/usr/local/bin/mediamtx
Restart=on-failure
User=root
WorkingDirectory=/etc/mediamtx

[Install]
WantedBy=multi-user.target
EOF


sudo systemctl daemon-reload
sudo systemctl enable mediamtx
sudo systemctl start mediamtx

sudo systemctl status mediamtx
