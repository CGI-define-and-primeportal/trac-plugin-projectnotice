from trac.core import *
from trac.config import *
from trac.admin.api import IAdminPanelProvider
from trac.web.chrome import add_stylesheet, add_script, add_notice, add_warning
from trac.util.translation import _
from genshi.filters.transform import Transformer
from genshi.builder import tag

class ProjectNotice(Component):

    """Plugin to allow us to post notices on projects,
    disable access to a project (for maintenance, etc.)"""

    implements(IAdminPanelProvider, ITemplateStreamFilter)

    def get_notice(self):
        """Retrieve the notice from the DB or None if not set"""
        cursor = self.env.get_read_db().cursor
        (text,) = cursor.execute("SELECT value FROM system_table WHERE name='notice'")
        return text

    def set_notice(self, text):
        """Insert the notice into the DB"""
        @self.env.with_transaction()
        def set_notice_transaction(db, text):
            cursor = db.cursor()
            cursor.execute("DELETE FROM system_table WHERE name='notice'")
            cursor.execute("INSERT INTO system_table (name, value) VALUES ('notice', '%s')" % text)

        return set_notice_transaction(text)

    # IAdminPageProvider methods
    def get_admin_panels(self, req):
        if req.perm.has_permission('TRAC_ADMIN'):
            yield ('general', _('General'))

    def render_admin_panel(self, req, cat, page, path_info):
        data = {}

        if req.method == 'post':
            self.set_notice(req.data.get('notice', ''))

        data['notice'] = self.get_notice()
        return 'project_notice_admin.html', data

    # ITemplateStreamFilter methods
    def filter_stream(req, method, filename, stream, data):
        notice = self.get_notice()
        if notice:
            stream |= Transformer("//div[id='mainnav']").after(tag.div(notice, id="project-notice"))
