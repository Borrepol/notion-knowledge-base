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
        'Notion-Version': '2022-06-28'
    }

    post_headers = {
        **headers,
        'Content-Type': 'application/json',
    }

    get_headers = {
        **headers,
        'accept': 'application/json',
    }

    data = {
        'parent': {'database_id': database_id},
        'properties': {}
    }

    def __init__(self) -> None:
        self.terms, self.definitions = self.parseDatabaseContents()

    def resetData(self) -> None:
        self.data = {
            'parent': {'database_id': self.database_id},
            'properties': {}
        }

    def mapResponse(self, code: int, message: str = 'short') -> str:
        if message not in ['short', 'long']:
            print('Specify if you either want a "long" or "short" response message.')

        if message == 'short':
            return responses[code][0]
        else:
            return responses[code][1]

    def addProperty(self, name: str, type: str, val) -> None:
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

    def viewData(self) -> None:
        print(self.data)

    def createDatabaseEntry(self):
        data = json.dumps(self.data)

        self.resetData()
        return requests.request('POST', self.url, headers=self.headers, data=data)

    def retrieveDatabaseContents(self, database_id: str = ''):
        if database_id == '':
            database_id = self.database_id

        url = f'https://api.notion.com/v1/databases/{database_id}/query'
        payload = {'page_size': 100}

        return requests.post(url, json=payload, headers=self.get_headers)

    def parseDatabaseContents(self, database_id: str = ''):
        terms = []
        definitions = []
        response = self.retrieveDatabaseContents(database_id)

        for row in response.json()['results']:
            properties = row['properties']
            terms.append(properties['Term']['title'][0]['plain_text'])
            definitions.append(properties['Definition']['rich_text'][0]['plain_text'])

        return terms, definitions

    def retrievePageProperties(self, page_id: str):
        url = f'{self.url}/{page_id}'
        return requests.get(url, headers=self.get_headers)

    def retrievePageContent(self, page_id: str):
        url = f'https://api.notion.com/v1/blocks/{page_id}/children'
        return requests.get(url, headers=self.get_headers)

    def retrieveCallouts(self, page_id: str) -> list:
        callouts = []
        response = self.retrievePageContent(page_id)
        for block in response.json()['results']:
            if block['type'] == 'callout':
                callouts.append(block['callout']['rich_text'][0]['plain_text'])

        return callouts

    def processDefinitions(self, page_id: str) -> None:
        callouts = self.retrieveCallouts(page_id)
        for c in callouts:
            term, definition = c.split(':')

            if term in self.terms and definition in self.definitions:
                continue

            self.terms.append(term)
            self.definitions.append(definition.strip())

    def insertDefinitions(self) -> list:
        # into database that is
        responses = []

        for t, d in zip(self.terms, self.definitions):
            # Check if the term-definition pair already exists, if not, create a new entry.
            # You don't have to check if it already exists if you can guarantee that the local lists in this object are always up
            # to date.
            self.addProperty('Term', 'title', t)
            self.addProperty('Definition', 'rich_text', d)

            r = self.createDatabaseEntry()
            responses.append(r)

        return responses
