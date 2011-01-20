from trac.core import Component, implements, TracError
from trac.perm import IPermissionRequestor
from tracrpc.api import IXMLRPCHandler
from projectnotice.web_ui import ProjectNotice

class Commands(Component):
    implements(IXMLRPCHandler)

    def get_notice(self, req):
        """Get the current notice or empty string"""
        pn = ProjectNotice(self.env)
        return pn.get_notice() or ""

    def set_notice(self, req, text):
        """Set a new notice, or delete the current one with empty string"""
        pn = ProjectNotice(self.env)
        return pn.set_notice(text)

    # IXMLRPCHandler methods
    def xmlrpc_namespace(self):
        return 'notice'

    def xmlrpc_methods(self):
        yield ('PROJECT_ADMIN', ((str,),), self.get_notice)
        yield ('PROJECT_ADMIN', ((str, str),), self.set_notice)
