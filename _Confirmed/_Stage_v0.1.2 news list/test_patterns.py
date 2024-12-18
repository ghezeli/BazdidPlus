import json
import requests
from urllib.parse import urljoin
from lxml import html, etree


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


def fetch_html_tree(url):
    """
    دریافت محتوای HTML صفحه و تبدیل آن به یک درخت برای پردازش با XPath.
    """
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            print(f"خطا در دریافت صفحه {url}: {response.status_code}")
            return None
        return html.fromstring(response.content)
    except Exception as e:
        print(f"خطا در دریافت صفحه {url}: {e}")
        return None


def validate_patterns(tree, patterns, source):
    """
    بررسی الگوها بر روی یک درخت HTML خاص.
    """
    extracted_data = {}
    for key, details in patterns.items():
        xpath = details.get("xpath")
        attribute = details.get("attribute")

        if details.get("source") != source:
            continue

        if not xpath or not attribute:
            print(f"الگوی {key} ناقص است.")
            continue

        # استخراج داده‌ها با استفاده از XPath
        elements = tree.xpath(xpath)
        if elements:
            if attribute == "text":
                extracted_data[key] = elements[0].text.strip() if elements[0].text else ""
            elif attribute == "html":
                extracted_data[key] = elements[0].text_content().strip() if elements[0].text_content() else ""
            else:
                extracted_data[key] = elements[0].get(attribute)
        else:
            extracted_data[key] = None

        # print(f"******* {key}  : {extracted_data[key]}")

    return extracted_data


def process_linked_pages(linked_urls, linked_patterns, base_url):
    """
    پردازش صفحات لینک شده و استخراج داده‌ها از آن‌ها.
    """
    linked_data = []
    for url in linked_urls:
        full_url = urljoin(base_url, url)  # ترکیب لینک نسبی با آدرس اصلی
        print(f"  پردازش صفحه لینک‌شده: {full_url}")
        tree = fetch_html_tree(full_url)
        if tree is not None:
            data = validate_patterns(tree, linked_patterns, 'linked_page')
            linked_data.append( data)
        else:
            print(f"    خطا در بارگذاری صفحه لینک‌شده: {full_url}")
    return linked_data


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
            tree = fetch_html_tree(page_url)
            if tree is None:
                print(f"    خطا در بارگذاری صفحه {page_url}")
                continue

            page_patterns = html_patterns[site_id]

            news_list_elements = tree.xpath(html_patterns[site_id]["section"]["xpath"])
            for news_element in news_list_elements:
                element_tree = html.fromstring(etree.tostring(news_element))

                results = validate_patterns(element_tree, page_patterns, 'list')
                if results:
                    print(f"    داده‌های استخراج‌شده از صفحه اصلی:")

                    # بررسی لینک‌های استخراج‌شده و پردازش صفحات لینک شده
                    if "url" in results and results["url"]:
                        linked_urls = [results["url"]] if isinstance(results["url"], str) else results["url"]
                        linked_data = process_linked_pages(linked_urls, page_patterns, site_url)
                        print(f"    داده‌های استخراج‌شده از صفحات لینک‌شده:")
                        for data in linked_data:
                            results = results | data
                            print(data)

                    for key, value in results.items():
                        if value:
                            print(f"      {key}: {value[:200]}")

                else:
                    print(f"    خطا در استخراج داده از {page_url}")
        print('-' * 50)


if __name__ == "__main__":
    test_config_and_patterns()
