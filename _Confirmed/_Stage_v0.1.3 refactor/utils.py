import json
import requests
from lxml import html, etree
from urllib.parse import urljoin
import logging

logging.basicConfig(filename='errors.log', level=logging.ERROR)

def load_json(file_path):
    """
    Load a JSON file and return its content as a dictionary.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The content of the JSON file, or an empty dictionary if an error occurs.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        log_error(f"خطا در بارگذاری فایل {file_path}: {e}")
        return {}

def fetch_html_tree(url):
    """
    Fetch the HTML content of a page and parse it into a tree structure for XPath operations.

    Args:
        url (str): The URL of the page to fetch.

    Returns:
        lxml.html.HtmlElement: The parsed HTML tree, or None if an error occurs.
    """
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            log_error(f"خطا در دریافت صفحه {url}: {response.status_code}")
            return None
        return html.fromstring(response.content)
    except Exception as e:
        log_error(f"خطا در دریافت صفحه {url}: {e}")
        return None

def is_valid_data(data):
    """
    Validate extracted data to ensure it meets basic requirements.

    Args:
        data (str): The extracted data to validate.

    Returns:
        bool: True if the data is valid, False otherwise.
    """
    if not data or len(data) < 5:
        return False
    if any(char.isdigit() for char in data):
        return True
    return False

def log_error(message):
    """
    Log an error message to the error log file.

    Args:
        message (str): The error message to log.
    """
    logging.error(message)

class ErrorHandler:
    """
    A utility class for handling errors in the application.
    """
    @staticmethod
    def log_and_raise(error_message, exception_type=Exception):
        """
        Log an error message and raise an exception.

        Args:
            error_message (str): The error message to log and raise.
            exception_type (Exception): The type of exception to raise.
        """
        log_error(error_message)
        raise exception_type(error_message)