import requests
import json

def update(column_name:str,cell_name:str,new_name:str, notion_token:str, database_id:str):
    headers = {
        "Authorization": "Bearer " + notion_token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    url = f'https://api.notion.com/v1/databases/{database_id}/query'

    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    payload = {
        "filter": {
            "property": column_name,
            "title": {
                "contains": cell_name
            }
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    pages = response.json()['results']

    if len(pages) > 0:
        page_id = pages[0]['id']
    else:
        print(f'No page found with the name "{cell_name}"')

    url = f'https://api.notion.com/v1/pages/{page_id}'

    payload = {
        "properties": {
            column_name: {
                "title": [
                    {
                        "text": {
                            "content": new_name
                        }
                    }
                ]
            }
        }
    }

    requests.request("PATCH", url, headers=headers, data=json.dumps(payload))