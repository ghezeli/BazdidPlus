from utils import fetch_html_tree, is_valid_data, log_error
from urllib.parse import urljoin

def validate_patterns(tree, patterns, source):
    extracted_data = {}
    for key, details in patterns.items():
        xpath = details.get("xpath")
        attribute = details.get("attribute")

        if details.get("source") != source:
            continue

        if not xpath or not attribute:
            log_error(f"الگوی {key} ناقص است.")
            continue

        elements = tree.xpath(xpath)
        if elements:
            if attribute == "text":
                extracted_data[key] = elements[0].text.strip() if elements[0].text else ""
            elif attribute == "html":
                extracted_data[key] = elements[0].text_content().strip() if elements[0].text_content() else ""
            else:
                extracted_data[key] = elements[0].get(attribute)

            if not is_valid_data(extracted_data[key]):
                log_error(f"داده نامعتبر برای {key}: {extracted_data[key]}")
                extracted_data[key] = None
        else:
            log_error(f"داده‌ای برای {key} پیدا نشد.")
            extracted_data[key] = None

    return extracted_data

def process_linked_pages(linked_urls, linked_patterns, base_url):
    linked_data = []
    for url in linked_urls:
        full_url = urljoin(base_url, url)
        print(f"  پردازش صفحه لینک‌شده: {full_url}")
        tree = fetch_html_tree(full_url)
        if tree is not None:
            data = validate_patterns(tree, linked_patterns, 'linked_page')
            linked_data.append(data)
        else:
            log_error(f"    خطا در بارگذاری صفحه لینک‌شده: {full_url}")
    return linked_data