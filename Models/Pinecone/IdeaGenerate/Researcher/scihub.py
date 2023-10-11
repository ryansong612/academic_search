import requests, re, sys, os
import concurrent.futures
from bs4 import BeautifulSoup
# from .WebCralwer import crawl_page, scraperapi
from .pdf import extract_paragraphs_from_pdf
import time
import random
from scidownl import scihub_download  
import logging
logging.getLogger("scidownl").setLevel(logging.WARNING)
logging.getLogger("scihub_download").setLevel(logging.WARNING)



# from WebCralwer import crawl_page, scraperapi
# from pdf import extract_paragraphs_from_pdf

pdfsLocation = "pdfs/"
source_Essay = "doi: {doi}, page: {page}"

def Brain_DOI(urls, trust=False):
    # Create a StringIO buffer to catch the output

    urls_ = [DOISniffer(url) for url in urls]
    if trust:
        urls_ = urls

    contents = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(ScihubDownloader, urls_)
        successful = []
        for result in results:
            try:
                if result:
                    successful.append(result["doi"])
                    contents += result["data"]
            except requests.exceptions.RequestException as e:
                print("An error occurred:", str(e))


    print("... Log -->")
    print("Successful extraction:")
    for item in successful:
        print("   ", item)
    print("Errors:")
    for item in urls_:
        if not item in successful:
            if item:
                print("   ", item)

    return contents

def DOISniffer(url):
    try:
        doi_pattern = r"(?i)\b(10[.][0-9]{4,}(?:[.][0-9]+)*\/[-._;()/:a-zA-Z0-9]+\b)"
        dois_found = re.findall(doi_pattern,url)
        dois_found = dois_found[0]
        return dois_found
    except:
        return None
    

def ScihubDownloader(doi):
    if doi:
        paper = doi
        paper_type = "doi"
        fileName = paper.replace("/", "_")
        fileName += ".pdf"
        out = "pdfs/" + fileName
        scihub_download(paper, paper_type=paper_type, out=out)

        if not os.path.exists(out):
            print(f"{doi} download failed.")
            return None
        paragraphs = extract_paragraphs_from_pdf(out)
        paragraphs_ = []
        for paragraph in paragraphs:
            paragraph_ = paragraph
            paragraph_["source"] = source_Essay.format(
                doi=doi,
                page=paragraph_["page_number"]
            )
            paragraphs_.append(paragraph_)
        data = {
            "data": paragraphs_,
            "doi": doi
        }
        return data
    else:
        return None

def DOI2Content(doi_string):
    if doi_string:
        fileName = SCIHUB_Download(doi_string, pdfsLocation)
        if fileName:
            pdfsLocation_ = pdfsLocation + fileName
            paragraphs = extract_paragraphs_from_pdf(pdfsLocation_)
            paragraphs_ = []
            for paragraph in paragraphs:
                paragraph_ = paragraph
                paragraph_["source"] = source_Essay.format(
                    doi=doi_string,
                    page=paragraph_["page_number"]
                )
                paragraphs_.append(paragraph_)
            return paragraphs_
        else:
            return None
    else:
        return None

def DOIDownload(url, doi, pdfLocation):
    fileName = doi.replace("/", "_")
    fileName += ".pdf"
    response = scraperapi(url)

    if response.status_code == 200:
        fileLocation = pdfLocation + fileName
        with open(fileLocation, 'wb') as file:
            file.write(response.content)
        # print("PDF downloaded successfully!")
    else:
        print("Failed to download PDF. Status code:", response.status_code)

    return fileName



def SCIHUB_Download(doi, folder):
    # Construct the Sci-Hub URL with the DOI
    link = open("Researcher/scihub.link", "r").read()
    link = link.split("\n")

    attempt = 0
    while attempt < 3:
        link = random.choice(link)
        url = link + doi
        sleep_random_duration()
        try:
            content = crawl_page(url)
            # Check if the request was successful
            if content:
                # Parse the HTML content
                try:
                    soup = BeautifulSoup(content, 'html.parser')
                except requests.exceptions.RequestException as e:
                    print("An error occurred:", str(e))
                    continue                
                # Find the embed element containing the PDF URL
                embeds = soup.find_all(['embed', 'iframe', 'button'])
                for embed in embeds:
                    try:
                        pdf_url = embed['src']
                        if pdf_url.find(".pdf") != -1:
                            fileName = DOIDownload(pdf_url, doi, folder)
                            return fileName
                    except Exception as e:
                        pass
                print(f"PDF not found for DOI {doi} from {link}")
            else:
                pass
        except requests.exceptions.RequestException as e:
            print("An error occurred:", str(e))

        attempt += 1
    print(f"PDF cannot be found for {doi}.")
    return None

def sleep_random_duration():
    random_duration = random.uniform(0, 1)
    time.sleep(random_duration)
# SCIHUB_Download("10.1021/bc800051c", pdfLocation)
# DOIDownload("https://sci.bban.top/pdf/10.1021/bc800051c.pdf", "abc.py", "../pdfs/")

# content = Brain_DOI(["https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.91.015502"])
# print(content)