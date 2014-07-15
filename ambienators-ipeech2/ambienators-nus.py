import datetime

import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Persons(ndb.Model):
    # celsius, fahrenheit or kelvin
    temperature_unit = ndb.StringProperty()

    # Timezone
    time_zone = ndb.FloatProperty()

    # By time or by parameters 
    notify_type = ndb.StringProperty(repeated=True)

    # If notify by time
    notify_time_value = ndb.IntegerProperty()
    notify_time_unit = ndb.StringProperty()

    # If notify by parameters
    notify_parameters = ndb.StringProperty(repeated=True)

    # Notify by temperature
    notify_temperature_abe = ndb.StringProperty() # above, below, exactly
    notify_temperature_value = ndb.IntegerProperty()
    notify_temperature_unit = ndb.StringProperty()

    # Notify by light intensity
    notify_light_abe = ndb.StringProperty() # above, below, exactly
    notify_light_value = ndb.IntegerProperty()

    # Notify by motion
    notify_motion = ndb.StringProperty()

    # How often to record history
    history_log_value = ndb.IntegerProperty()
    history_log_unit = ndb.StringProperty()

    # Number of readings to display
    num_readings = ndb.IntegerProperty()
 
class ArduinoSensorData(ndb.Model):
    temp = ndb.IntegerProperty()
    light = ndb.IntegerProperty()
    movement = ndb.IntegerProperty()
    lastmovement = ndb.DateTimeProperty(auto_now_add=True)
    lastupdate = ndb.DateTimeProperty(auto_now_add=True)

 
class ArduinoPost(webapp2.RequestHandler):
    def post(self):
        sensordata = ArduinoSensorData.get_or_insert('1')

        try:
            temp = int(self.request.get('temp'))
            movement = int(self.request.get('movement'))
            light = int(self.request.get('light'))
            sensordata.temp = temp
            sensordata.light = light
            sensordata.lastupdate = datetime.datetime.now()
            sensordata.movement = movement
            
            if movement == 1:
                sensordata.lastmovement = datetime.datetime.now()

            sensordata.put()
            params = urllib.urlencode({'username':users.get_current_user().nickname()})
            self.redirect('/sensors?' + params)

        except ValueError:
            pass

class MainPage(webapp2.RequestHandler):
  """ Handler for the front page."""
  def get(self):
        template = jinja_environment.get_template('front.html')
        self.response.write(template.render())


class MainPageUser(webapp2.RequestHandler):
    # Front page for those logged in

    def get(self):
        user = users.get_current_user()
        parent = ndb.Key('Persons', users.get_current_user().email())
        person = parent.get()

        if person == None:
            person = Persons(id=users.get_current_user().email())

            person.temperature_unit = 'celsius'

            person.time_zone = 8.00

            person.notify_type = ['by-time']

            person.notify_time_value = 4
            person.notify_time_unit = 'days'

            person.notify_parameters = ['by-temp']

            person.notify_temperature_abe = 'exactly'
            person.notify_temperature_value = 20
            person.notify_temperature_unit = 'celsius'

            person.notify_light_abe = 'above'
            person.notify_light_value = 90

            person.notify_motion = 'present'

            person.num_readings = 5

            person.history_log_value = 2
            person.history_log_unit = 'days'

            person.put()

        if user:  # signed in already
            params = urllib.urlencode({'username':users.get_current_user().nickname()})
            template_values = {
                'user_mail': users.get_current_user().email(),
                'logout': users.create_logout_url(self.request.host_url),
                'nickname': users.get_current_user().nickname(),
            }
            template = jinja_environment.get_template('frontuser.html')
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(self.request.host_url)


class Sensors(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        parent = ndb.Key('Persons', users.get_current_user().email())
        person = parent.get()

        if user:  # signed in already
            sense = ArduinoSensorData.get_or_insert('1')
            if (sense.movement):
                motionStatusString = "present"
            else: 
                motionStatusString = "not present"
            template_values = {
                'person': person,
                'temp': str(sense.temp),
                'light': str(sense.light),
                'datetimeLastMovement': (sense.lastmovement + datetime.timedelta(hours=person.time_zone)).strftime("%d %b %y, %I.%M.%S %p"),
                'datetime': (datetime.datetime.now() + datetime.timedelta(hours=person.time_zone)).strftime("%d %b %y, %I.%M.%S %p"),
                'datetimeLastUpdate': (sense.lastupdate + datetime.timedelta(hours=person.time_zone)).strftime("%d %b %y, %I.%M.%S %p"),
                'motionStatusString': motionStatusString,
                'user_mail': users.get_current_user().email(),
                'nickname': users.get_current_user().nickname(),
                'logout': users.create_logout_url(self.request.host_url),
            }
            template = jinja_environment.get_template('sensors.html')
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(self.request.host_url)

class History(webapp2.RequestHandler):
    # History

    def get(self):
        user = users.get_current_user()
        parent = ndb.Key('Persons', users.get_current_user().email())
        person = parent.get()
        
        if user:  # signed in already
            template_values = {
                'user_mail': users.get_current_user().email(),
                'nickname': users.get_current_user().nickname(),
                'logout': users.create_logout_url(self.request.host_url),
                'person': person,
                'datetime': (datetime.datetime.now() + datetime.timedelta(hours=person.time_zone)).strftime("%d %b %y, %I.%M.%S %p"),
            }
            template = jinja_environment.get_template('history.html')
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(self.request.host_url)


class Settings(webapp2.RequestHandler):
    # Settings

    def get(self):
        user = users.get_current_user()
        parent = ndb.Key('Persons', users.get_current_user().email())
        person = parent.get()

        if user:  # signed in already
            template_values = {
                'user_mail': users.get_current_user().email(),
                'logout': users.create_logout_url(self.request.host_url),
                'person': person,
                'nickname': users.get_current_user().nickname(),
            }
            template = jinja_environment.get_template('settings.html')
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(self.request.host_url)

    def post(self):
        parent = ndb.Key('Persons', users.get_current_user().email())
        person = parent.get()

        person.temperature_unit = self.request.get('select-temp-unit')

        person.time_zone = float(self.request.get('input-time-zone'))

        person.notify_type = self.request.get_all('notify-type')

        person.notify_time_value = int(self.request.get('notify-time-value'))
        person.notify_time_unit = self.request.get('notify-time-unit')

        person.notify_parameters = self.request.get_all('parameter')

        person.notify_temperature_abe = self.request.get('above-below-temp')
        person.notify_temperature_value = int(self.request.get('notify-temp-val'))
        person.notify_temperature_unit = self.request.get('notify-temp-unit')

        person.notify_light_abe = self.request.get('above-below-light')
        person.notify_light_value = int(self.request.get('notify-light-val'))

        person.notify_motion = self.request.get('present-notpresent')

        person.history_log_value = int(self.request.get('select-historylog-value'))
        person.history_log_unit = self.request.get('select-historylog-unit')

        person.num_readings = int(self.request.get('inputReadings'))

        person.put()
        self.redirect('/settings')


    
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/mainuser', MainPageUser),
                               ('/arduinopost', ArduinoPost),
                               ('/sensors', Sensors),
                               ('/history', History),
                               ('/settings', Settings)],
                              debug=True)