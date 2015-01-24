import os

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
  loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)

class District(ndb.Model):
  name = ndb.StringProperty()
  
class Eviction(ndb.Model):
    """Contains eviction info"""
    location=ndb.GeoPtProperty()
    address = ndb.TextProperty()
    postcode = ndb.StringProperty()
    district = ndb.KeyProperty(kind=District)
    description = ndb.TextProperty()
    evictionDateTime = ndb.DateTimeProperty()
    lastUpdated = ndb.DateTimeProperty(auto_now=True)
  
class EvictionAlert(ndb.Model):
    """Model for an eviction alert"""
    eviction = ndb.KeyProperty(kind=Eviction)
    tweetText = ndb.TextProperty()

class EvictAlertUser(ndb.Model):
  user = ndb.UserProperty()


class HomePage(webapp2.RequestHandler):
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('templates/index.html')
    template_values = {
      'login_url' : users.create_login_url('/')
    }
    self.response.write(template.render(template_values))


application = webapp2.WSGIApplication([
    ('/', HomePage),
], debug=True)