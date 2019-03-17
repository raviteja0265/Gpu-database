import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from myinfo import MyInfo
from datetime import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Edit(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        name = self.request.get('name')
        myinfo_key = ndb.Key('MyInfo', name)
        myinfo = myinfo_key.get()

        template_values = {
            'myinfo': myinfo
        }

        template = JINJA_ENVIRONMENT.get_template('edit.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        if self.request.get('button') == 'Edit':
            name = self.request.get('name')
            myinfo_key = ndb.Key('MyInfo', name)
            myinfo = myinfo_key.get()

            manufacturer = self.request.get('manufacturer')
            date = datetime.strptime(self.request.get('date'), '%Y-%m-%d')
            geometryShader = self.request.POST.get('geometryShader') == 'on'
            tesselationShader = self.request.POST.get('tesselationShader') == 'on'
            shaderInt16 = self.request.POST.get('shaderInt16') == 'on'
            sparseBinding = self.request.POST.get('sparseBinding') == 'on'
            textureCompressionETC2 = self.request.POST.get('textureCompressionETC2') == 'on'
            vertexPipelineStoresAndAtomics = self.request.POST.get('vertexPipelineStoresAndAtomics') == 'on'

            myinfo.name = name
            myinfo.manufacturer = manufacturer
            myinfo.date = date
            myinfo.geometryShader = geometryShader
            myinfo.tesselationShader = tesselationShader
            myinfo.shaderInt16 = shaderInt16
            myinfo.sparseBinding = sparseBinding
            myinfo.textureCompressionETC2 = textureCompressionETC2
            myinfo.vertexPipelineStoresAndAtomics = vertexPipelineStoresAndAtomics

            myinfo.put()
            self.redirect('/')
