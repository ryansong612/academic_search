from .crossRefRetriever import search_journal_doi
from .Brain_Tools import TokenCheck, SplitParagraph, punctuationPercentage
from .Relevance import ParagraphsRank
from .scihub import Brain_DOI

import json
import time


def CrossRef_Search(query, row, budget):
    query = query.replace("'", "")
    query = query.replace('"', "")

    time1 = time.time()
    dois = search_journal_doi(query, row)
    content = Brain_DOI(dois, True)
    time2 = time.time()
    detlaT = time2 - time1
    print(f"... Web content fetched ({detlaT:.2f} s)")

    content = SplitParagraph(content)
    for item in content: # making sure there are not too many puncturations in the paragraph
        if punctuationPercentage(item["content"]) > 0.90:
            content.remove(item)
    content = ParagraphsRank(query, content)
    time3 = time.time()
    detlaT = time3 - time2
    print(f"... Content filterred ({detlaT:.2f} s)")

    # Fit resulted data into budget
    total_tokens = 0
    dataList = []
    for item_ in content:
        item = {
            "content": item_["content"],
            "origin": item_["source"]
        }
        item_token_count = TokenCheck(item)
        if total_tokens + item_token_count > budget:
            break
        dataList.insert(0, item)
        total_tokens += item_token_count
    return dataList

# query = "ring opening polymerization catalyst"
# result = CrossRef_Search(query, 5, 10000)
# result = json.dumps(result, indent=4)
# print(result)