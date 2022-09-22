import requests
import json

from HTTP_response_codes import responses
import keys


class Request():
    integration_token = keys.integration_token
    database_id = keys.database_id
    url = 'https://api.notion.com/v1/pages'

    headers = {
        "Authorization": "Bearer " + integration_token,
        "Content-Type": "application/json",
        "Notion-Version": "2021-08-16"
    }

    data = {
        'parent': {'database_id': database_id},
        'properties': {}
    }

    def mapResponse(self, code: int, message: str = 'short'):
        if message not in ['short', 'long']:
            print('Specify if you either want a "long" or "short" response message.')

        if message == 'short':
            return responses[code][0]
        else:
            return responses[code][1]

    def addProperty(self, name: str, type: str, val):
        self.data['properties'][name] = {
            'type': type,
            type: val
        }

    def viewData(self):
        print(self.data)

    def createDatabaseEntry(self):
        data = json.dumps(self.data)
        return requests.request('POST', self.url, headers=self.headers, data=data)


r = Request()
r.addProperty('Name', 'title', [{'type': 'text', 'text': {'content': 'Hoi'}}])
r.viewData()
response = r.createDatabaseEntry()

print(r.mapResponse(response.status_code))
print(response.text)