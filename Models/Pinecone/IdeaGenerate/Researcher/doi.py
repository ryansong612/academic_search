import requests
import re

# from WebCralwer import crawl_page
def DOISniffer(url):
    try:
        # webpage_content = crawl_page(url)
        doi_pattern = r"(?i)\b(10[.][0-9]{4,}(?:[.][0-9]+)*\/[-._;()/:a-zA-Z0-9]+\b)"
        dois_found = re.findall(doi_pattern, url)
        dois_found = dois_found[0]
        return dois_found
    except:
        return None

