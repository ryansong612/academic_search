import requests
import concurrent.futures
# import pickle
import json
import time
import random
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import scrapy
from scrapy.crawler import CrawlerProcess

def scraperapi(url):
    payload = {'api_key': '5f7fd03e3404714cf5ab645471fc6319', 'url': url}
    response = requests.get('http://api.scraperapi.com', params=payload)
    return response


def crawl_page(url):        
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        # Set a random user agent
        # user_agent = random.choice(user_agents)
        # page.setUserAgent(user_agent)
        page.goto(url)
        content = page.content()
        browser.close()
        return content

def Crawler(urls):
    '''
    [
        {
            "source": urls,
            "time": time,
            "content": extracted_text
        }
    ]
    '''

    # Function to extract text from the crawled webpage and detect paragraphs
    def extract_text_from_page(content):
        soup = BeautifulSoup(content, "html.parser")
        paragraphs = soup.find_all('p')
        extracted_text = ''
        for paragraph in paragraphs:
            extracted_text += paragraph.get_text(separator=" ").strip() + ' '
        return extracted_text.replace('\n', ' ').strip()

    # Create a ThreadPoolExecutor with a maximum of 5 concurrent workers
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Submit the crawl_page function for each URL and retrieve futures
        futures = [executor.submit(crawl_page, url) for url in urls]

        # Iterate over the completed futures as they complete
        results = []
        for future, url in zip(concurrent.futures.as_completed(futures), urls):
            try:
                content = future.result()
                if content:
                    # Extract text from the crawled webpage and detect paragraphs
                    extracted_text = extract_text_from_page(content)
                    
                    # Create a dictionary with crawled data
                    data = {
                        "source": url,
                        "time": time.strftime('%Y-%m-%d %H:%M:%S'),
                        # "raw_content": content,
                        "content": extracted_text
                    }
                    results.append(data)
            except Exception as e:
                print(f"An error occurred: {str(e)}")
    return results

