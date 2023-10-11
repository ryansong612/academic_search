from .Brain_Search import Brain_Search
from .Brain_Tools import TokenCheck

def LinkSearch(query, num_results, budget):
    query = query.replace("'", "")
    query = query.replace('"', "")
    result = Brain_Search(query, num_results)

    total_tokens = 0
    message_list = []
    for item_ in result:
        item = {
            "source": item_["source"],
	    "content": item_["content"],
        }
        item_token_count = TokenCheck(item)
        item = {"source": item_["source"],"content": [item_["content"]]}
        if total_tokens + item_token_count > budget:
            break
        
        message_list.insert(0, item)
        total_tokens += item_token_count
    return message_list