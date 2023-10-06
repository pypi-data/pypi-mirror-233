class ApiKeyType(Exception):
    def __init__(self, _type):
        self.value = f'The API key is {_type}, should be str.'

    def __str__(self):
        return repr(self.value)

    __module__ = 'builtins'
