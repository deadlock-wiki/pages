import os
import mwclient

class Wiki:
    def __init__(self, username, password):
        self.auth = {
            'user': username,
            'password': password,
        }

        if not self.auth['user']:
            raise Exception('BOT_WIKI_USER env var is required to upload to wiki')

        if not self.auth['password']:
            raise Exception('BOT_WIKI_PASS env var is required to upload to wiki')

        self.site = mwclient.Site('deadlocked.wiki', path='/')
        self.site.login(self.auth['user'], self.auth['password'])

    def _get_namespace_id(self, search_namespace):
        for namespace_id, namespace in self.site.namespaces.items():
            if namespace == search_namespace:
                return namespace_id