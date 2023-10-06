from .ApiData import A

__url__ = 'https://data.shuvtai.cn/MobAI/API/URL/data.txt'


class URL(A):
    def __init__(self, _url):
        A.__init__(
            self,
            {
                'chat': _url + '/chat',
                'new': _url + '/new',
                'records': _url + '/records',
                'check': _url + '/check',
                'exist': _url + '/exist',
                'apply': _url + '/apply',
            }
        )
        self.chat = _url + '/chat'
        self.new = _url + '/new'
        self.records = _url + '/records'
        self.check = _url + '/check'
        self.exist = _url + '/exist'
        self.apply = _url + '/apply'
