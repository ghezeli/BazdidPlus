import json
import requests
from lxml import html

def load_json(file_path):
    """
    بارگذاری داده‌ها از یک فایل JSON.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"خطا در بارگذاری فایل {file_path}: {e}")
        return {}

def validate_patterns(page_url, patterns):
    """
    بررسی الگوها بر روی یک صفحه خاص.
    """
    try:
        response = requests.get(page_url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            print(f"خطا در دریافت صفحه {page_url}: {response.status_code}")
            return None

        tree = html.fromstring(response.content)  # تبدیل محتوای صفحه به درخت HTML با استفاده از lxml
        extracted_data = {}

        for key, details in patterns.items():
            xpath = details.get("xpath")
            attribute = details.get("attribute")

            if not xpath or not attribute:
                print(f"الگوی {key} ناقص است.")
                continue

            # استخراج داده‌ها با استفاده از XPath
            elements = tree.xpath(xpath)

            if elements:
                if attribute == "text":
                    extracted_data[key] = elements[0].text.strip() if elements[0].text else ""
                else:
                    extracted_data[key] = elements[0].get(attribute)
            else:
                extracted_data[key] = None

        return extracted_data
    except Exception as e:
        print(f"خطا در پردازش صفحه {page_url}: {e}")
        return None

def test_config_and_patterns():
    """
    تست فایل‌های config.json و html_patterns.json بر روی صفحات تعریف‌شده.
    """
    config = load_json('config.json')
    patterns = load_json('html_patterns.json')

    websites = config.get("websites", [])
    html_patterns = {site["site_id"]: site["patterns"] for site in patterns.get("websites", [])}

    for site in websites:
        site_id = site.get("site_id")
        site_url = site.get("url")
        pages = site.get("pages", [])

        if not site_id or site_id not in html_patterns:
            print(f"  الگو برای سایت {site_url} با site_id={site_id} پیدا نشد.")
            continue

        print(f"در حال بررسی سایت: {site_url} (site_id: {site_id})")
        for page in pages:
            page_url = page.get("url")
            print(f"  بررسی صفحه: {page_url}")
            page_patterns = html_patterns[site_id]

            results = validate_patterns(page_url, page_patterns)
            if results:
                print(f"    داده‌های استخراج‌شده:")
                for key, value in results.items():
                    print(f"      {key}: {value}")
            else:
                print(f"    خطا در استخراج داده از {page_url}")
        print('-' * 50)

if __name__ == "__main__":
    test_config_and_patterns()
