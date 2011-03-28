from trac.core import *
from trac.config import Option
from trac.admin.api import IAdminPanelProvider
from trac.web import ITemplateStreamFilter
from trac.web.chrome import add_stylesheet, add_notice, ITemplateProvider
from trac.util.translation import _
from genshi.filters.transform import Transformer
from genshi.builder import tag

class ProjectNotice(Component):

    """Plugin to allow the posting of notices on projects,
    disable access to a project (for maintenance, etc.)"""
    insert_after = Option('projectnotice', 'insert_after', '//div[@id="mainnav"]',
                          doc="Genshi path expression to after which element the project notice should be inserted")
    implements(IAdminPanelProvider, ITemplateStreamFilter, ITemplateProvider)

    def get_notice(self):
        """Retrieve the notice from the DB or None if not set"""
        text = None

        cursor = self.env.get_read_db().cursor()
        cursor.execute("SELECT value FROM system WHERE name='notice'")
        result = cursor.fetchone()
        if result:
            (text,) = result

        return text

    def set_notice(self, text):
        """Insert the notice into the DB"""
        text = text.strip()

        @self.env.with_transaction()
        def set_notice_transaction(db):
            cursor = db.cursor()
            cursor.execute("DELETE FROM system WHERE name='notice'")
            if text:
                cursor.execute("""INSERT INTO system (name, value) VALUES ('notice', %s)""", (text,))

        return text

    # IAdminPageProvider methods
    def get_admin_panels(self, req):
        if req.perm.has_permission('TRAC_ADMIN'):
            yield ('general', _('General'), 'notice', _('Project Notice'))

    def render_admin_panel(self, req, cat, page, path_info):
        data = {}

        if req.method == 'POST':
            if self.set_notice(req.args.get('notice', '')):
                add_notice(req, _("Added project notice"))
            else:
                add_notice(req, _("Removed project notice"))

            req.redirect(req.href.admin(cat, page))

        data['notice'] = self.get_notice()

        return 'project_notice_admin.html', data

    # ITemplateStreamFilter methods
    def filter_stream(self, req, method, filename, stream, data):
        notice = self.get_notice()

        if notice:
            stream |= Transformer(self.insert_after).after(tag.div(tag.div(tag.span(_("Notice: ")), notice), id="project-notice"))

        return stream

    # ITemplateProvider methods
    def get_htdocs_dirs(self):
        """Return the absolute path of a directory containing additional
        static resources (such as images, style sheets, etc).
        """
        from pkg_resources import resource_filename
        return [('projectnotice', resource_filename(__name__, 'htdocs'))]

    def get_templates_dirs(self):
        """Return the absolute path of the directory containing the provided
        ClearSilver/Genshi templates.
        """
        from pkg_resources import resource_filename
        return [resource_filename(__name__, 'templates')]
