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


class View(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        name = self.request.get('name')
        myinfo_key = ndb.Key('MyInfo', name)
        myinfo = myinfo_key.get()

        geometryShader = bool(self.request.GET.get('GeometryShader'))
        tesselationShader = bool(self.request.GET.get('tesselationShader'))
        shaderInt16 = bool(self.request.GET.get('ShaderInt16'))
        sparseBinding = bool(self.request.GET.get('sparseBinding'))
        textureCompressionETC2 = bool(self.request.GET.get('textureCompressionETC2'))
        vertexPipelineStoresAndAtomics = bool(self.request.GET.get('vertexPipelineStoresAndAtomics'))

        template_values = {
            "myinfo": myinfo,
            'geometryShader': geometryShader,
            'tesselationShader': tesselationShader,
            'shaderInt16': shaderInt16,
            'sparseBinding': sparseBinding,
            'textureCompressionETC2': textureCompressionETC2,
            'vertexPipelineStoresAndAtomics': vertexPipelineStoresAndAtomics
        }

        template = JINJA_ENVIRONMENT.get_template('display.html')
        self.response.write(template.render(template_values))

