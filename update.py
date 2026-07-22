import base64
import requests

# ۱. لینک ساب اصلی خود را دقیقاً بین دو کوتیشن قرار دهید
MAIN_SUB_URL = "https://your-bpb-worker.workers.dev/sub/YOUR_UUID"

# ۲. نام اختصاصی شما همراه با فونت و نمادهای خاص
BRAND_NAME = "𝔸𝕣𝕤𝕖𝕟𝕍ℙℕ𓄂𓆃 ❻❽"

def process_sub():
    headers = {
        'User-Agent': 'v2rayNG/1.8.5'
    }
    
    try:
        response = requests.get(MAIN_SUB_URL, headers=headers, timeout=15)
        if response.status_code != 200:
            print("خطا در دریافت لینک ساب اصلی")
            return

        raw_data = response.text.strip()
        
        try:
            decoded_data = base64.b64decode(raw_data).decode('utf-8')
        except Exception:
            decoded_data = raw_data

        lines = decoded_data.strip().splitlines()
        new_lines = []

        counter = 1
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # جدا کردن لینک کانفیگ و حذف کامل اسم‌های قبلی
            if "#" in line:
                config_link = line.split("#")[0]
            else:
                config_link = line

            # ساخت اسم جدید به فرمت: 𝔸𝕣𝕤𝕖𝕟𝕍ℙℕ𓄂𓆃 ❻❽ - 01
            new_name = f"{BRAND_NAME} - {counter:02d}"
            new_lines.append(f"{config_link}#{new_name}")
            counter += 1

        final_configs = "\n".join(new_lines)
        encoded_sub = base64.b64encode(final_configs.encode('utf-8')).decode('utf-8')

        with open("sub.txt", "w", encoding="utf-8") as f:
            f.write(encoded_sub)
            
        print("فایل با موفقیت آپدیت شد.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    process_sub()
