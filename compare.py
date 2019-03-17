import webapp2
import jinja2
import os

from google.appengine.ext import ndb
from myinfo import MyInfo

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Compare(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        name = self.request.get('name')
        current_name = self.request.get('current_name')

        if name != None and current_name != None:
            myinfo_key = ndb.Key('MyInfo', name)
            myinfo = myinfo_key.get()

            currentinfo_key = ndb.Key('MyInfo', current_name)
            current_name = currentinfo_key.get()

            myinfo_query = MyInfo.query(ndb.OR(MyInfo.name == name, MyInfo.name == current_name)).fetch()

        else:
            myinfo_query = MyInfo.query().fetch()

        template_values = {
            'myinfo': myinfo_query
        }

        template = JINJA_ENVIRONMENT.get_template('compare.html')
        self.response.write(template.render(template_values))
