from __future__ import absolute_import

from .api import Api


class Client(object):

    def __init__(self, base_url, api_token):
        self.api = Api(base_url, api_token)

    def get_all_issues(self):
        res = self.api.send(method='get', resource='/issues',
                            params={'page_size': 10, 'page': 1})
        return res
