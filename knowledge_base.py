import requests
import json

from HTTP_response_codes import responses
import keys


class Request():
    integration_token = keys.integration_token
    database_id = keys.database_id
    url = 'https://api.notion.com/v1/pages'

    headers = {
        'Authorization': 'Bearer ' + integration_token,
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }

    data = {
        'parent': {'database_id': database_id},
        'properties': {}
    }

    def resetData(self):
        self.data = {
            'parent': {'database_id': self.database_id},
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
        if type == 'title':
            self.data['properties'][name] = {
                'type': type,
                type: [{'type': 'text', 'text': {'content': val}}]
            }
        elif type == 'rich_text':
            self.data['properties'][name] = {
                'type': type,
                type: [{'text': {'content': val}}]
            }
        else:
            self.data['properties'][name] = {
                'type': type,
                type: val
            }

    def viewData(self):
        print(self.data)

    def createDatabaseEntry(self):
        data = json.dumps(self.data)

        self.resetData()
        return requests.request('POST', self.url, headers=self.headers, data=data)

    def retrievePageProperties(self, page_id: str):
        url = f'{self.url}/{page_id}'

        headers = {
            'Authorization': 'Bearer ' + self.integration_token,
            "accept": "application/json",
            "Notion-Version": "2022-06-28"
        }

        return requests.get(url, headers=headers)

    def retrievePageContent(self, page_id: str):
        url = f'https://api.notion.com/v1/blocks/{page_id}/children'

        headers = {
            'Authorization': 'Bearer ' + self.integration_token,
            "accept": "application/json",
            "Notion-Version": "2022-06-28"
        }

        return requests.get(url, headers=headers)

    def getCallouts(self, page_id: str):
        callouts = []
        response = self.retrievePageContent(page_id)
        for block in response.json()['results']:
            if block['type'] == 'callout':
                callouts.append(block['callout']['rich_text'][0]['plain_text'])

        self.callouts = callouts
        return callouts

    def processDefinitions(self):
        self.terms = []
        self.definitions = []
        for d in self.callouts:
            term, definition = d.split(':')
            self.terms.append(term)
            self.definitions.append(definition.strip())
            # print(f'Term: {term}, Definition: {definition}')

    def insertDefinitions(self):
        # into database that is

        for t, d in zip(self.terms, self.definitions):
            print(type(t))
            print(type(d))
            self.addProperty('Term', 'title', t)
            self.addProperty('Definition', 'rich_text', d)

            self.viewData()

            r = self.createDatabaseEntry()
            print(self.mapResponse(r.status_code, 'long'))


r = Request()
# r.addProperty('Term', 'title', 'Testing')
# r.addProperty('Definition', 'rich_text', 'tester')
# r.viewData()
# response = r.createDatabaseEntry()

# print(r.mapResponse(response.status_code))
# print(response.text)

# page = r.retrievePageContent('2ef5d88e5cf94281aaadd7dc43eac6cf')
# print(r.mapResponse(page.status_code))

# with open('./pagecontent.json', 'w', encoding='utf8') as f:
#     json.dump(page.text, f, ensure_ascii=False)

print(r.getCallouts('2ef5d88e5cf94281aaadd7dc43eac6cf'))
r.processDefinitions()
r.insertDefinitions()
