import requests

def GoogleSearch(query, num_results):
    api_key = "AIzaSyC0xnc-zf6pFLTa-v94o86M9bOnW6_fvas" 
    cx = "b42aa963114c741a0"
    search_results = []
    
    num_per_request = 10
    num_requests = num_results // num_per_request
    
    for i in range(num_requests):
        start = i * num_per_request + 1
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&cx={cx}&key={api_key}&start={start}&num={num_per_request}"
        
        try:
            response = requests.get(url)
            data = response.json()
            # print(data)
            
            if "items" in data:
                for item in data["items"]:
                    search_results.append(item["link"])
        
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
    
    return search_results[:num_results] 