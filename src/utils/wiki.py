import mwclient
import sys
import os
# Import parents
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from src.utils.constants import SITE_URL

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

        self.site = mwclient.Site(SITE_URL, path='/')
        self.site.login(self.auth['user'], self.auth['password'])

    def _get_namespace_id(self, search_namespace):
        """ 
        Retrieve the namespace id from a namespace name
        Namespace is used for site.allpages[] dict
        """
        for namespace_id, namespace in self.site.namespaces.items():
            if namespace == search_namespace:
                return namespace_id
            
        raise Exception(f'Namespace {search_namespace} not found')
    
    def get_prefixed_page_names(self, prefix, namespace):
        """
        Retrieve all page names under a specific namespace and have a prefix.
        prefix should not contain the namespace, e.g. 'DeadBot/blueprints/'
        """
        
        namespace_id = self._get_namespace_id(namespace)

        # Blueprint pages are all subpages of User:DeadBot/blueprints/
        page_names = []
        
        # Retrieve all subpages
        page_objs = self.site.allpages(prefix=prefix, 
                                                 namespace=namespace_id)
        for page in page_objs:
            page_names.append(page.name)

        return page_names