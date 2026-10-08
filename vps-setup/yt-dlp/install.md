apt update && apt install -y python3 python3-venv python3-pip curl pipx p7zip-full ffmpeg

export PATH="/usr/local/bin:$PATH" 

echo 'export PATH="/usr/local/bin:$PATH"' >> /root/.bashrc 

pipx ensurepath
source /root/.bashrc

pipx install "yt-dlp[default]"
pipx inject yt-dlp yt-dlp-ejs

curl -fsSL https://deno.land/x/install/install.sh | sh
sudo mv ~/.deno/bin/deno /usr/local/bin/

sudo mkdir -p /root/yt-cookies
sudo mkdir -p /root/downloads/yt
