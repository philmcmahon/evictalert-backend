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

# Might need this model to handle permissions etc.
# class EvictAlertUser(ndb.Model):
#   user_id = ndb.StringProperty(required=True)

class AlertGroup(ndb.Model):
  name = ndb.StringProperty()

class GroupAlerter(ndb.Model):
  userid = ndb.StringProperty(required=True)
  group = ndb.KeyProperty(required=True, kind=AlertGroup)

class HomePage(webapp2.RequestHandler):
  def get(self):
    current_user = users.get_current_user()
    if current_user:
      alert_groups = getUserAlertGroups(current_user.user_id())

      template = JINJA_ENVIRONMENT.get_template('templates/grouplist.html')
      template_values = {
        'logout_url' : users.create_logout_url('/'),
        'alert_groups' : alert_groups 
      }
      self.response.write(template.render(template_values))
    else:
      template = JINJA_ENVIRONMENT.get_template('templates/index.html')
      template_values = {
        'login_url' : users.create_login_url('/')
      }
      self.response.write(template.render(template_values))

def getUserAlertGroups(user_id):
  user_groups = GroupAlerter.query(GroupAlerter.userid==user_id)
  alert_groups = []
  for user_group in user_groups:
    alert_group = AlertGroup.get_by_id(user_group.group.id())
    alert_groups.append(alert_group)
  return alert_groups

# hacky code to put stuff into datastore
# tg = AlertGroup(name='testgroup1', id='testgroup1')
# tgk = tg.put()
# tga = GroupAlerter(userid='185804764220139124118', group='testgroup1')
# tga.put()

application = webapp2.WSGIApplication([
    ('/', HomePage),
], debug=True)