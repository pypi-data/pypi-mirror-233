# *----------------------------------------------------------------
# * MobAI.API.ApiData
# * Write by MoYeRanQianZhi
# * 2023.7.26
# *----------------------------------------------------------------

import json


class A:
    def __init__(self, _data):
        self._data = _data
        self.reply = None
        self.error = None
        self.id = None
        self.password = None
        self.message_id = None
        self.finish = None
        self.records = None
        self.message = None
        self.role = None

    def __str__(self):
        return json.dumps(self._data, indent=4)

    def __repr__(self):
        return json.dumps(self._data, indent=4)

    def dict(self):
        return self._data


class ChatData(A):
    def __init__(self, _data):
        A.__init__(self, _data)
        self.time = _data['time']
        self.state = _data['state']
        if _data['state'] == 'success':
            self.data = A(_data['data'])
            self.data.message_id = _data['data']['message_id']
            self.data.reply = _data['data']['reply']
            self.data.finish = _data['data']['finish']
        else:
            self.data = A(_data['data'])
            self.data.error = _data['data']['error']


class NewData(A):
    def __init__(self, _data):
        A.__init__(self, _data)
        self.time = _data['time']
        self.state = _data['state']
        if _data['state'] == 'success':
            self.data = A(_data['data'])
            self.data.id = _data['data']['chat_id']
            self.data.password = _data['data']['password']
            self.data.reply = _data['data']['reply']
        else:
            self.data = A(_data['data'])
            self.data.error = _data['data']['error']


class RecordsData(A):
    def __init__(self, _data):
        A.__init__(self, _data)
        self.time = _data['time']
        self.state = _data['state']
        if _data['state'] == 'success':
            self.data = A(_data['data'])
            self.data.records = []
            for _record in _data['data']['records']:
                record = A(_record)
                record.time = _record['time']
                record.role = _record['role']
                record.message = _record['message']
                self.data.records.append(record)
        else:
            self.data = A(_data['data'])
            self.data.error = _data['data']['error']
