import requests
import json

from HTTP_response_codes import responses
import keys

integration_token = keys.integration_token
database_id = keys.database_id

# https://prettystatic.com/notion-api-python/ got me started

headers = {
    "Authorization": "Bearer " + integration_token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16"
}


def mapResponse(code: int, message: str = 'short'):
    if message not in ['short', 'long']:
        print('Specify if you either want a "long" or "short" response message.')

    if message == 'short':
        return responses[code][0]
    else:
        return responses[code][1]


def readDatabase(databaseId, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)
    # print(res.text)

    with open('./db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)


def createPage(databaseId, headers):
    createUrl = 'https://api.notion.com/v1/pages'

    newPageData = {
        "parent": {"database_id": databaseId},
        "properties": {
            "Description": {
                "title": [
                    {
                        "text": {
                            "content": "Review"
                        }
                    }
                ]
            },
            "Value": {
                "rich_text": [
                    {
                        "text": {
                            "content": "Amazing"
                        }
                    }
                ]
            },
            "Status": {
                "rich_text": [
                    {
                        "text": {
                            "content": "Active"
                        }
                    }
                ]
            }
        }
    }

    data = json.dumps(newPageData)
    # print(str(uploadData))

    res = requests.request("POST", createUrl, headers=headers, data=data)

    print(res.status_code)
    print(res.text)


def createDatabaseEntry(database_id, headers):
    url = 'https://api.notion.com/v1/pages'

    data = {
        'parent': {'database_id': database_id},
        'properties': {
            'Name': {
                'type': 'title',
                'title': [{'type': 'text', 'text': {'content': 'Hoi'}}]
            },
            'Test': {
                'type': 'number',
                'number': 20
            }
        }
    }

    data = json.dumps(data)
    response = requests.request('POST', url, headers=headers, data=data)

    print(mapResponse(response.status_code))
    print(response.text)


def updatePage(pageId, headers):
    updateUrl = f"https://api.notion.com/v1/pages/{pageId}"

    updateData = {
        "properties": {
            "Value": {
                "rich_text": [
                    {
                        "text": {
                            "content": "Pretty Good"
                        }
                    }
                ]
            }
        }
    }

    data = json.dumps(updateData)

    response = requests.request("PATCH", updateUrl, headers=headers, data=data)

    print(response.status_code)
    print(response.text)


# createPage(database_id, headers)
createDatabaseEntry(database_id, headers)

# curl -X POST https://api.notion.com/v1/pages \
#   -H "Authorization: Bearer $NOTION_KEY" \
#   -H "Content-Type: application/json" \
#   -H "Notion-Version: 2021-08-16" \
#   --data "{
#     \"parent\": { \"database_id\": \"$NOTION_DATABASE_ID\" },
#     \"properties\": {
#       \"title\": {
#         \"title\": [
#           {
#             \"text\": {
#               \"content\": \"Yurts in Big Sur, California\"
#             }
#           }
#         ]
#       }
#     }
#   }"

# 'Grocery item': {
#     'type': 'title',
#     'title': [{'type': 'text', 'text': {'content': 'Tomatoes'}}]
# },
# 'Price': {
#     'type': 'number',
#     'number': 1.49
# },
# 'Last ordered': {
#     'type': 'date',
#     'date': {'start': '2021-05-11'}
# }