import base64
import json
import requests
import yaml

# ۱. لینک ساب اصلی خود (لینک عادی VLESS/Base64) را اینجا بگذارید
MAIN_SUB_URL = "https://ap1o50xfxh2ijvi0h.panel1-cc4.workers.dev/ArsenVPN68/sub/raw?app=xray#%F0%9F%92%A6%20BPB%20Raw"

# ۲. نام برند اختصاصی
BRAND_NAME = "𝔸𝕣𝕤𝕖𝕟𝕍ℙℕ𓄂𓆃 ❻❽"

def process_sub():
    headers = {'User-Agent': 'v2rayNG/1.8.5'}
    
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

        lines = [line.strip() for line in decoded_data.strip().splitlines() if line.strip()]
        
        new_vless_lines = []
        clash_proxies = []
        json_outbound_list = []

        counter = 1
        for line in lines:
            if "#" in line:
                config_link = line.split("#")[0]
            else:
                config_link = line

            server_name = f"{BRAND_NAME} - {counter:02d}"
            
            # ۱. ساخت لینک برای V2Ray (sub.txt)
            new_vless_lines.append(f"{config_link}#{server_name}")
            
            # ۲. جهت آماده‌سازی برای Clash و JSON
            clash_proxies.append({
                'name': server_name,
                'type': 'vless',
                # نیازمند پارسر لینک برای تبدیل کامل به پروکسی‌های Clash
            })

            counter += 1

        # --- ۱. ذخیره ساب معمولی (sub.txt) ---
        final_configs = "\n".join(new_vless_lines)
        encoded_sub = base64.b64encode(final_configs.encode('utf-8')).decode('utf-8')
        with open("sub.txt", "w", encoding="utf-8") as f:
            f.write(encoded_sub)

        # --- ۲. ذخیره ساب کلش (clash.yaml) ---
        # نمونه پیکربندی پایه Clash
        clash_config = {
            'port': 7890,
            'socks-port': 7891,
            'allow-lan': True,
            'mode': 'rule',
            'log-level': 'info',
            'proxies': clash_proxies,
            'proxy-groups': [
                {
                    'name': 'PROXIES',
                    'type': 'select',
                    'proxies': [p['name'] for p in clash_proxies]
                }
            ]
        }
        with open("clash.yaml", "w", encoding="utf-8") as f:
            yaml.dump(clash_config, f, allow_unicode=True, sort_keys=False)

        # --- ۳. ذخیره ساب جیسون (sub.json) ---
        json_config = {
            "remarks": BRAND_NAME,
            "outbounds": json_outbound_list
        }
        with open("sub.json", "w", encoding="utf-8") as f:
            json.dump(json_config, f, ensure_ascii=False, indent=2)

        print("هر ۳ فایل sub.txt و clash.yaml و sub.json ساخته شدند!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    process_sub()
