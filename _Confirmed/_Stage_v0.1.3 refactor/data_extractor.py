from utils import fetch_html_tree, is_valid_data, log_error
from urllib.parse import urljoin

class PatternValidator:
    """
    A class to validate patterns and extract data using XPath.
    """
    def __init__(self, patterns, source):
        """
        Initialize the PatternValidator.

        Args:
            patterns (dict): The dictionary of patterns to validate.
            source (str): The source type (e.g., 'list' or 'linked_page').
        """
        self.patterns = patterns
        self.source = source

    def validate(self, tree):
        """
        Validate patterns against an HTML tree and extract data.

        Args:
            tree (lxml.html.HtmlElement): The HTML tree to validate patterns against.

        Returns:
            dict: A dictionary of extracted data.
        """
        extracted_data = {}
        for key, details in self.patterns.items():
            xpath = details.get("xpath")
            attribute = details.get("attribute")

            if details.get("source") != self.source:
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
    """
    Process linked pages and extract data based on linked patterns.

    Args:
        linked_urls (list): A list of URLs to process.
        linked_patterns (dict): The dictionary of patterns for linked pages.
        base_url (str): The base URL to resolve relative links.

    Returns:
        list: A list of dictionaries containing extracted data from linked pages.
    """
    linked_data = []
    for url in linked_urls:
        full_url = urljoin(base_url, url)
        print(f"  پردازش صفحه لینک‌شده: {full_url}")
        tree = fetch_html_tree(full_url)
        if tree is not None:
            validator = PatternValidator(linked_patterns, 'linked_page')
            data = validator.validate(tree)
            linked_data.append(data)
        else:
            log_error(f"    خطا در بارگذاری صفحه لینک‌شده: {full_url}")
    return linked_data