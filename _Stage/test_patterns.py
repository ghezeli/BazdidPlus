from utils import load_json, fetch_html_tree
from data_extractor import PatternValidator, process_linked_pages
from lxml import html, etree
import pytest

class TestPatternValidation:
    """
    A class to test pattern validation functionality.
    """
    @pytest.fixture
    def setup_data(self):
        """
        Load configuration and pattern data for testing.

        Returns:
            tuple: Config and patterns data.
        """
        config = load_json('config.json')
        patterns = load_json('html_patterns.json')
        return config, patterns

    def test_config_and_patterns(self, setup_data):
        """
        Test the configuration and patterns against defined websites.
        """
        config, patterns = setup_data

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

                    validator = PatternValidator(page_patterns, 'list')
                    results = validator.validate(element_tree)
                    if results:
                        print(f"    داده‌های استخراج‌شده از صفحه اصلی:")

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