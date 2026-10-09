#!/usr/bin/env bash
# -------------------------------------------------
# 1️⃣ نمط البحث عن الملفات
#    أي ملف في الدليل الحالي (أو في شجرة الدليل) يحتوي على "ia_"
#    استخدم glob أو find حسب الحاجة
# -------------------------------------------------

# مثال باستخدام glob (يعمل إذا كان عدد الملفات ليس كبيرًا)
for src in *ia-url*; do
    # تخطى إذا لم يُعثر على أي ملف (glob يُعيد النص نفسه عندما لا يوجد تطابق)
    [[ -e "$src" ]] || continue

    # 2️⃣ اسم الملف الناتج – نضيف اللاحقة "_encoded" قبل الامتداد
    base="${src%.*}"          # الجزء قبل الامتداد
    ext="${src##*.}"          # الامتداد
    dst="${base}_encoded.${ext}"

    # 3️⃣ النصوص التي تُضاف في البداية والنهاية لكل سطر (يمكن تعديلها)
    prefix='<link itemprop="associatedMedia" href="https://archive.org/download/'
    suffix='">'

    # 4️⃣ تحويل كل سطر داخل الملف إلى URL‑encoded ثم إضافة البادئة/اللاحقة
    while IFS= read -r line; do
        encoded=$(python3 -c "import urllib.parse, sys; \
print(urllib.parse.quote(sys.argv[1], safe='/'''))" "$line")
        echo "${prefix}${encoded}${suffix}"
    done < "$src" > "$dst"

    echo "تمت المعالجة: $src → $dst"
done
