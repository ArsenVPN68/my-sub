import base64
import requests

# ۱. لینک ساب اصلی خود را اینجا بگذارید
MAIN_SUB_URL = "https://ap1o50xfxh2ijvi0h.panel1-cc4.workers.dev/ArsenVPN68/sub/normal?app=clash#%F0%9F%92%A6%20BPB%20Normal"

# ۲. پیشوند و پسوند دلخواه خود را تنظیم کنید
PREFIX = "⚡ MyBrand | "  # پیشوند (قبل از اسم سرور)
SUFFIX = " 🚀"           # پسوند (بعد از اسم سرور)

def process_sub():
    response = requests.get(MAIN_SUB_URL)
    if response.status_code != 200:
        print("خطا در دریافت لینک ساب اصلی")
        return

    # رمزگشایی لینک ساب اصلی (Base64)
    raw_data = response.text.strip()
    try:
        decoded_data = base64.b64decode(raw_data).decode('utf-8')
    except Exception:
        decoded_data = raw_data # اگر از قبل Base64 نبود

    lines = decoded_data.strip().splitlines()
    new_lines = []

    for line in lines:
        if "#" in line:
            # جدا کردن لینک کانفیگ از اسم فعلی آن
            config_link, old_name = line.split("#", 1)
            # ساخت اسم جدید
            new_name = f"{PREFIX}{old_name}{SUFFIX}"
            new_lines.append(f"{config_link}#{new_name}")
        else:
            new_lines.append(line)

    # تبدیل مجدد به Base64
    final_configs = "\n".join(new_lines)
    encoded_sub = base64.b64encode(final_configs.encode('utf-8')).decode('utf-8')

    # ذخیره در فایل
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write(encoded_sub)

if __name__ == "__main__":
    process_sub()
