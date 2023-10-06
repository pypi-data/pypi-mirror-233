# *----------------------------------------------------------------
# * MobAI.API.api
# * Write by MoYeRanQianZhi
# * 2023.7.26
# *----------------------------------------------------------------

import requests
import json

from .ApiData import ChatData, NewData, RecordsData
from . import common
from .error import ApiKeyType

_api_key = None
url = common.URL(
    requests.get(common.__url__).text
)


class ChatAPI:
    def __init__(self, _id, password, question, api_key=None):
        self.id = _id
        self.password = password
        self.question = question

        if api_key is not None:
            self.api_key = api_key
        elif _api_key is not None:
            self.api_key = _api_key
        else:
            raise ApiKeyType('None')

    def ask(self):
        for chunk in requests.post(
                url=url.chat,
                json={
                    'key': self.api_key,
                    'id': self.id,
                    'password': self.password,
                    'question': self.question,
                },
                stream=True,
        ).iter_content(10 * 1024):
            for message in chunk.decode('utf-8').splitlines():
                yield ChatData(json.loads(message))


class CreateNewAPI(NewData):
    def __init__(self, model, api_key=None):
        self.model = model

        if api_key is not None:
            self.api_key = api_key
        elif _api_key is not None:
            self.api_key = _api_key
        else:
            raise ApiKeyType('None')

        NewData.__init__(self, self.create())

    def create(self):
        return requests.post(
            url=url.new,
            json={
                'key': self.api_key,
                'model': self.model,
            }
        ).json()


class RecodesAPI(RecordsData):
    def __init__(self, _id, password, api_key=None):
        self.id = _id
        self.password = password

        if api_key is not None:
            self.api_key = api_key
        elif _api_key is not None:
            self.api_key = _api_key
        else:
            raise ApiKeyType('None')

        RecordsData.__init__(self, self.records())

    def records(self):
        return requests.post(
            url=url.records,
            json={
                'key': self.api_key,
                'id': self.id,
                'password': self.password,
            }
        ).json()


def check(_id, password, api_key=None):
    if api_key is not None:
        pass
    elif _api_key is not None:
        api_key = _api_key
    else:
        raise ApiKeyType('None')

    return requests.post(
        url=url.check,
        json={
            'key': api_key,
            'id': _id,
            'password': password,
        }
    ).json()['state'] == 'success'


def exist(_id, api_key=None):
    if api_key is not None:
        pass
    elif _api_key is not None:
        api_key = _api_key
    else:
        raise ApiKeyType('None')

    return requests.post(
        url=url.exist,
        json={
            'key': api_key,
            'id': _id,
        }
    ).json()['state'] == 'success'


def apply(email):
    return requests.post(
        url.apply,
        json={'mail': email}
    )
