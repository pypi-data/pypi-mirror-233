import requests
import json

def post(column_name:str, content:str, notion_token:str, database_id:str):
    headers = {
        "Authorization": "Bearer " + notion_token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    create_url = "https://api.notion.com/v1/pages"
    data = {
        column_name: {"title": [{"text": {"content": content}}]},
    }

    payload = {"parent": {"database_id": database_id}, "properties": data}

    requests.post(create_url, headers=headers, json=payload)