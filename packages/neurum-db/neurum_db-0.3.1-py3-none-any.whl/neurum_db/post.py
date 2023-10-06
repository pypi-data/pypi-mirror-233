import requests
import json

class DB():
    notion_token:str
    database_id:str
headers = {
    "Authorization": "Bearer " + DB.notion_token,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def post(column_name:str, content:str):
    create_url = "https://api.notion.com/v1/pages"
    data = {
        column_name: {"title": [{"text": {"content": content}}]},
    }

    payload = {"parent": {"database_id": DB.database_id}, "properties": data}

    requests.post(create_url, headers=headers, json=payload)

