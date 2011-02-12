from trac.core import *
from trac.web.chrome import INavigationContributor
from trac.util import Markup

from genshi.builder import tag

class NavAdd(Component):
    """ Allows to add items to main and meta navigation bar"""
    implements(INavigationContributor)

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
