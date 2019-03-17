import os
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from datetime import datetime

from myuser import MyUser
from myinfo import MyInfo
from view import View
from edit import Edit
from compare import Compare

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        if user == None:
            template_values = {
                'login_url': users.create_login_url(self.request.url)
            }

            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render(template_values))
            return
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        if myuser == None:
            myuser = MyUser(id=user.user_id())
            myuser.put()
        myinfo_query = MyInfo().query().fetch()

        template_values = {
            'logout_url': users.create_logout_url(self.request.url),
            'myinfos': myinfo_query
        }

        template = JINJA_ENVIRONMENT.get_template('homepage.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        action = self.request.get('button')
        if action == 'add Information':
            name = self.request.get('name')
            manufacturer = self.request.get('manufacturer')
            date = self.request.get('date')
            geometryShader = self.request.get('geometryShader') == 'on'
            tesselationShader = self.request.get('tesselationShader') == 'on'
            shaderInt16 = self.request.get('shaderInt16') == 'on'
            sparseBinding = self.request.get('sparseBinding') == 'on'
            textureCompressionETC2 = self.request.get('textureCompressionETC2') == 'on'
            vertexPipelineStoresAndAtomics = self.request.get('vertexPipelineStoresAndAtomics') == 'on'
            myinfo_list = MyInfo.query()

            myinfo_list = myinfo_list.fetch()

            user = users.get_current_user()

            myinfo_key = ndb.Key('MyUser', name)
            myinfo = myinfo_key.get()

            myinfo.myinfos.append(myinfo_list)
            myinfo.put()
            template_values = {
                'myinfo_list': myinfo_list,
                'geometryShader': geometryShader,
                'tesselationShader': tesselationShader,
                'shaderInt16': shaderInt16,
                'sparseBinding': sparseBinding,
                'textureCompressionETC2': textureCompressionETC2,
                'vertexPipelineStoresAndAtomics': vertexPipelineStoresAndAtomics
            }

            template = JINJA_ENVIRONMENT.get_template('homepage.html')
            self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        if action == 'add Information':
            name = self.request.get('name')
            manufacturer = self.request.get('manufacturer')
            date = self.request.get('date')
            geometryShader = self.request.POST.get('geometryShader') == 'on'
            tesselationShader = self.request.POST.get('tesselationShader') == 'on'
            shaderInt16 = self.request.POST.get('shaderInt16') == 'on'
            sparseBinding = self.request.POST.get('sparseBinding') == 'on'
            textureCompressionETC2 = self.request.POST.get('textureCompressionETC2') == 'on'
            vertexPipelineStoresAndAtomics = self.request.POST.get('vertexPipelineStoresAndAtomics') == 'on'

            user = users.get_current_user()

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()
            myinfo_key = ndb.Key('MyInfo', name)
            myinfo = myinfo_key.get()

            if myinfo == None:
                new_address = MyInfo(id=name, name=name, manufacturer=manufacturer,
                                     date=datetime.strptime(date, '%Y-%m-%d').date(), geometryShader=geometryShader,
                                     tesselationShader=tesselationShader, shaderInt16=shaderInt16,
                                     sparseBinding=sparseBinding, textureCompressionETC2=textureCompressionETC2,
                                     vertexPipelineStoresAndAtomics=vertexPipelineStoresAndAtomics)
                myuser.myinfos.append(new_address)
                new_address.put()

                self.redirect('/')
            else:
                template_values = {
                    'message': 'Name already exists in the database, try again using other name'
                }
                template = JINJA_ENVIRONMENT.get_template('homepage.html')
                self.response.write(template.render(template_values))

                self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/view', View),
    ('/edit', Edit),
    ('/compare', Compare)
], debug=True)
