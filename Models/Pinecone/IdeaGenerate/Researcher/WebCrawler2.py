import requests
import concurrent.futures
# import pickle
import json
import time
import random
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def scraperapi(url):
    payload = {'api_key': '5f7fd03e3404714cf5ab645471fc6319', 'url': url}
    response = requests.get('http://api.scraperapi.com', params=payload)
    return response

# def crawl_page(url):        
#     response = scraperapi(url)
#     soup = BeautifulSoup(response.content, "html.parser")
#     return soup

def crawl_page(url):    
    response = requests.get(url)
    if response.status_code == 200:
        # Return the content of the web page
        return response.text
    else:
        print(f"Failed to retrieve content from {url}. Status code: {response.status_code}")
        return None
    




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
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Submit the crawl_page function for each URL and retrieve futures
        futures = [executor.submit(crawl_page, url) for url in urls]

        # Iterate over the completed futures as they complete
        results = []
        for future, url in zip(concurrent.futures.as_completed(futures), urls):
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
        
    return results
