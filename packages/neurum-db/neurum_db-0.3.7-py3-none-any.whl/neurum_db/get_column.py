import requests
import json
    

def get_column(column_name:str, notion_token:str, database_id:str, num_pages=None):
    headers = {
            "Authorization": "Bearer " + notion_token,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    url = f"https://api.notion.com/v1/databases/{database_id}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    pages = data["results"]

    for page in pages:
        props=page['properties']
        tweet=props[column_name]['title'][0]['text']['content']
        return tweet