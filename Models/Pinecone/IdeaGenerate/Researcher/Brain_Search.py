import time

from .WebCralwer import Crawler
from .Search import GoogleSearch
from .Brain_Tools import SplitParagraph
from .Relevance import ParagraphsRank
from .scihub import Brain_DOI


# from WebCralwer import Crawler
# from Search import GoogleSearch
# from Brain_Tools import SplitParagraph
# from Relevance import ParagraphsRank
# from doi import DOISniffer
# from scihub import SCIHUB_Download
# from pdf import extract_paragraphs_from_pdf



def Brain_Search(query, num_results):
    time1 = time.time()
    urls = GoogleSearch(query, num_results)
    contents = Crawler(urls)
    content1= Brain_DOI(urls)
    contents += content1
    time2 = time.time()
    detlaT = time2 - time1
    print(f"... Web content fetched ({detlaT:.2f} s)")

    content_split = SplitParagraph(contents)
    content_rank = ParagraphsRank(query, content_split)
    time3 = time.time()
    detlaT = time3 - time2
    print(f"... Content filterred ({detlaT:.2f} s)")
    return content_rank


# write a function that takes a list of urls and returns a list of paragraphs



# content = DOI2Content("https://pubs.acs.org/doi/10.1021/bc800051c")
# log = open("draft.json", "w")
# log.write(json.dumps(content, indent=4))


    