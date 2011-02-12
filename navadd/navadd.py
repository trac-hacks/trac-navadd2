from trac.core import *
from trac.web.api import IRequestFilter
from trac.web.chrome import INavigationContributor
from trac.util import Markup

from genshi.builder import tag

class NavAdd(Component):
    """ Allows to add items to main and meta navigation bar"""
    implements(INavigationContributor, IRequestFilter)

    # INavigationContributor methods
    def get_active_navigation_item(self, req):
        return ''
    
    def get_navigation_items(self, req):
        add = self.env.config.getlist('navadd', 'add_items', [])
        
        for a in add:
            title = self.env.config.get('navadd', '%s.title' % a)
            url = self.env.config.get('navadd', '%s.url' % a)
            perm = self.env.config.get('navadd', '%s.perm' % a)
            target = self.env.config.get('navadd', '%s.target' % a)
            forusers = self.env.config.getlist('navadd', '%s.forusers' % a, [])

            if perm and not req.perm.has_permission(perm):
                continue

            if forusers and req.authname not in forusers:
                continue

            if target not in ('mainnav', 'metanav'):
                target = 'mainnav'

            yield (target, a, tag.a(title, href=url))

    # IRequestFilter methods
    def pre_process_request(self, req, handler):
        add = self.env.config.getlist('navadd', 'add_items', [])

        for a in add:
            url = self.env.config.get('navadd', '%s.url' % a)
            perm = self.env.config.get('navadd', '%s.perm' % a)
            target = self.env.config.get('navadd', '%s.target' % a)
            forusers = self.env.config.getlist('navadd', '%s.forusers' % a, [])
            setactive = self.env.config.getbool('navadd', '%s.setactive' % a, True)

            if perm and not req.perm.has_permission(perm):
                continue

            if forusers and req.authname not in forusers:
                continue

            if not req.environ['PATH_INFO'].startswith(url):
                continue

            if target not in ('mainnav', 'metanav'):
                target = 'mainnav'

            items = req.chrome.get('nav', {}).get(target, [])

            if not items:
                continue

            for i in items:
                if i.get('name', '') == a:
                    # We first disable all items
                    for j in items:
                        j['active'] = False

                    # We enable our item
                    i['active'] = True

                    break

            break

        return handler

    def post_process_request(req, template, content_type):
        return (template, content_type)

    def post_process_request(req, template, data, content_type):
        return (template, data, content_type)
