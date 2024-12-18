import json
import requests
import logging
from lxml import html, etree

logging.basicConfig(filename='errors.log', level=logging.ERROR)

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        log_error(f"خطا در بارگذاری فایل {file_path}: {e}")
        return {}

def fetch_html_tree(url):
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
    if not data or len(data) < 5:
        return False
    if any(char.isdigit() for char in data):
        return True
    return False

def log_error(message):
    logging.error(message)