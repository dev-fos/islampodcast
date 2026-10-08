sudo apt update && sudo apt upgrade -y

sudo apt install -y wget tar ffmpeg

cd /tmp
wget https://github.com/bluenviron/mediamtx/releases/download/v1.21.1/mediamtx_v1.21.1_linux_amd64.tar.gz

tar -xzf mediamtx_v1.21.1_linux_amd64.tar.gz

sudo systemctl stop mediamtx

sudo mv mediamtx /usr/local/bin/

sudo systemctl start mediamtx

sudo systemctl status mediamtx
