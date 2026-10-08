# لتحويل معدل ملفات الصوت الى بت 128 كيلوبت في الثانية
shopt -s globstar

for src in **/*.{webm,m4a}; do
    [ -e "$src" ] || continue

    tmp="$(mktemp --suffix=.mp3)"
    ffmpeg -y -loglevel error -i "$src" \
           -c:a libmp3lame -b:a 128k -f mp3 "$tmp"

    if [ $? -eq 0 ]; then
        mv -f "$tmp" "${src%.*}.mp3"
        rm -f "$src"
        echo "✅ تم التحويل: $src → ${src%.*}.mp3"
    else
        echo "❌ فشل التحويل: $src" >&2
        rm -f "$tmp"
    fi
done
