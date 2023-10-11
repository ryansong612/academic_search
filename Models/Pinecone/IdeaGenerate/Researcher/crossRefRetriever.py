import requests

def search_journal_doi(query, rows=30):
    base_url = "https://api.crossref.org/works"
    params = {
        "query": query,
        "filter": "type:journal-article",
        "rows": rows  # Number of results to retrieve
    }

    try:
        response = requests.get(base_url, params=params)
        response_data = response.json()

        if response.status_code == 200:
            results = response_data.get("message", {}).get("items", [])
            dois = [result.get("DOI") for result in results]
            return dois
        else:
            print("Request failed with status code:", response.status_code)
            return []

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return []
