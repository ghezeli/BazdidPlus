import requests
from lxml import html
import json

def fetch_html_tree(url):
    """
    دریافت محتوای HTML صفحه و تبدیل آن به یک درخت برای پردازش با XPath.
    """
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the page: {url}")
    return html.fromstring(response.content)

def auto_generate_patterns(tree):
    """
    تولید خودکار الگوهای XPath برای فیلدهای متداول.
    """
    patterns = {}

    # جستجوی عنوان
    title_element = tree.xpath("//h1 | //h2 | //title")
    if title_element:
        patterns["title"] = {"xpath": tree.getroottree().getpath(title_element[0]), "attribute": "text"}

    # جستجوی URL
    url_element = tree.xpath("//a[contains(@href, 'http')]")
    if url_element:
        patterns["url"] = {"xpath": tree.getroottree().getpath(url_element[0]), "attribute": "href"}

    # جستجوی خلاصه
    summary_element = tree.xpath("//meta[@name='description']/@content | //p")
    if summary_element:
        patterns["summary"] = {"xpath": tree.getroottree().getpath(summary_element[0]), "attribute": "text"}

    # جستجوی محتوا
    content_element = tree.xpath("//div[contains(@class, 'content') or contains(@id, 'content')]")
    if content_element:
        patterns["content"] = {"xpath": tree.getroottree().getpath(content_element[0]), "attribute": "html"}

    # جستجوی تصویر
    image_element = tree.xpath("//img[contains(@src, 'http')]")
    if image_element:
        patterns["image"] = {"xpath": tree.getroottree().getpath(image_element[0]), "attribute": "src"}

    return patterns

def save_patterns_to_config(site_id, patterns, config_file="config.json"):
    """
    ذخیره الگوهای شناسایی‌شده در فایل config.json.
    """
    try:
        with open(config_file, "r", encoding="utf-8") as file:
            config = json.load(file)
    except FileNotFoundError:
        raise Exception(f"Configuration file {config_file} not found.")

    # به‌روزرسانی الگوها برای سایت مشخص‌شده
    for site in config["websites"]:
        if site["site_id"] == site_id:
            site["patterns"] = patterns
            break

    with open(config_file, "w", encoding="utf-8") as file:
        json.dump(config, file, ensure_ascii=False, indent=2)

def process_sites_from_config(config_file="config.json"):
    """
    پردازش تمامی سایت‌های تعریف‌شده در فایل config.json و تولید الگوها.
    """
    try:
        with open(config_file, "r", encoding="utf-8") as file:
            config = json.load(file)
    except FileNotFoundError:
        raise Exception(f"Configuration file {config_file} not found.")

    for site in config["websites"]:
        site_id = site["site_id"]
        url = site.get("url")
        if not url:
            print(f"Skipping {site_id}: No URL provided.")
            continue

        print(f"Processing {site_id}...")
        try:
            tree = fetch_html_tree(url)
            patterns = auto_generate_patterns(tree)
            save_patterns_to_config(site_id, patterns, config_file)
            print(f"Patterns for {site_id} saved successfully.")
        except Exception as e:
            print(f"Failed to process {site_id}: {e}")

if __name__ == "__main__":
    process_sites_from_config()
