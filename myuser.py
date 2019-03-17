from google.appengine.ext import ndb
from myinfo import MyInfo


class MyUser(ndb.Model):
    name = ndb.StringProperty()
    myinfos = ndb.StructuredProperty(MyInfo, repeated=True)
