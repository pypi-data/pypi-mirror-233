import requests
import json

NOTION_TOKEN="secret_pUQmH18OKFJzkYv8eXIvSHzHfJAL7TTc4b8jxm8XyHy"
DATABASE_ID="a486f8d8e1694bfc9fc1e30d4b041ed0"
class DB():
    notion_token:str
    database_id:str
headers = {
    "Authorization": "Bearer " + DB.notion_token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def get(column_name:str, cell_name:str, num_pages=None):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    url = f"https://api.notion.com/v1/databases/{DB.database_id}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    pages = data["results"]

    content=[]

    for page in pages:
        props=page['properties']
        tweet=props[column_name]['title'][0]['text']['content']
        content.append(tweet)
    return content

def post(column_name:str, content:str):
    create_url = "https://api.notion.com/v1/pages"
    data = {
        column_name: {"title": [{"text": {"content": content}}]},
    }

    payload = {"parent": {"database_id": DB.database_id}, "properties": data}

    requests.post(create_url, headers=headers, json=payload)

def update(column_name:str,cell_name:str,new_name:str):

    url = f'https://api.notion.com/v1/databases/{DB.database_id}/query'

    headers = {
        "Authorization": f"Bearer {DB.notion_token}",
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

def delete(column_name:str, cell_name:str):
    url = f'https://api.notion.com/v1/databases/{DB.database_id}/query'

    headers = {
        "Authorization": f"Bearer {DB.notion_token}",
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

    payload = {"archived": True}

    requests.patch(url, json=payload, headers=headers)

#creating pages

'''create_page("Tweet", "Stanford")
'''
#getting pages
"""pages = get_pages()

content=[]

for page in pages:
    props=page['properties']
    tweet=props["Tweet"]['title'][0]['text']['content']
    content.append(tweet)
print(content)"""

#updating pages
'''update("", "", "")'''

#deleting pages
'''delete_page("Tweet", "listing")'''