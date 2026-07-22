import base64
import json
import os
import requests

BRAND_DEFAULT = "𝔸𝕣𝕤𝕖𝕟𝕍ℙℕ𓄂𓆃 ❻❽"

def ensure_directories():
    """ایجاد پوشه‌های جداگانه برای هر کلاینت"""
    os.makedirs("v2ray", exist_ok=True)
    os.makedirs("clash", exist_ok=True)

def process_single_sub(sub_info):
    sub_id = sub_info.get("id", "default").strip()
    brand_name = sub_info.get("name", BRAND_DEFAULT).strip()
    main_url = sub_info.get("url", "").strip()

    if not main_url or not sub_id:
        return

    # پاک‌سازی لینک اصلی از علامت #
    clean_main_url = main_url.split("#")[0] if "#" in main_url else main_url

    headers = {'User-Agent': 'v2rayNG/1.8.5'}
    
    try:
        # --- ۱. دریافت ساب اصلی و تغییر اسم سرورها ---
        res = requests.get(clean_main_url, headers=headers, timeout=15)
        if res.status_code != 200:
            print(f"❌ خطا در دریافت ساب {sub_id}: کد وضعیت {res.status_code}")
            return

        raw_data = res.text.strip()
        try:
            decoded_data = base64.b64decode(raw_data).decode('utf-8')
        except Exception:
            decoded_data = raw_data

        lines = [l.strip() for l in decoded_data.strip().splitlines() if l.strip()]
        v2ray_lines = [f"#profile-title: {brand_name}"]

        counter = 1
        for line in lines:
            if line.startswith("#"):
                continue

            config_link = line.split("#")[0] if "#" in line else line
            server_name = f"{brand_name} - {counter:02d}"
            v2ray_lines.append(f"{config_link}#{server_name}")
            counter += 1

        # --- ۲. ذخیره در پوشه v2ray ---
        plain_v2ray = "\n".join(v2ray_lines)
        encoded_v2ray = base64.b64encode(plain_v2ray.encode('utf-8')).decode('utf-8')
        
        v2ray_path = os.path.join("v2ray", f"{sub_id}.txt")
        with open(v2ray_path, "w", encoding="utf-8") as f:
            f.write(encoded_v2ray)

        print(f"✅ ساب V2Ray برای [{sub_id}] ذخیره شد در: {v2ray_path}")

        # --- ۳. تبدیل و ذخیره در پوشه clash ---
        subconverter_url = f"https://sub.v1.mk/sub?target=clash&url={requests.utils.quote(clean_main_url)}&insert=true"
        clash_res = requests.get(subconverter_url, headers={'User-Agent': 'ClashMeta'}, timeout=20)
        
        if clash_res.status_code == 200:
            clash_path = os.path.join("clash", f"{sub_id}.yaml")
            with open(clash_path, "w", encoding="utf-8") as f:
                f.write(clash_res.text)
            print(f"✅ ساب Clash برای [{sub_id}] ذخیره شد در: {clash_path}")
        else:
            print(f"⚠️ خطا در تبدیل کلش برای [{sub_id}]")

    except Exception as e:
        print(f"❌ خطا در پردازش {sub_id}: {e}")

def main():
    ensure_directories()
    if os.path.exists("subs.json"):
        with open("subs.json", "r", encoding="utf-8") as f:
            subs = json.load(f)
            for sub in subs:
                process_single_sub(sub)
    else:
        print("فایل subs.json یافت نشد!")

if __name__ == "__main__":
    main()
