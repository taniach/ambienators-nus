from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import datetime
 
from google.appengine.ext import db




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

 
class ArduinoSensorData(db.Model):
    temp = db.IntegerProperty()
    light = db.IntegerProperty()
    movement = db.IntegerProperty()
    list = db.StringListProperty()
    lastmovement = db.DateTimeProperty(auto_now_add=True)
    lastupdate = db.DateTimeProperty(auto_now_add=True)

 
class ArduinoPost(webapp2.RequestHandler):
    def post(self):
        sensordata = ArduinoSensorData.get_or_insert('1')

        try:
            temp = int(self.request.get('temp'))
            movement = int(self.request.get('movement'))
            moves = int(self.request.get('moves'))
            light = int(self.request.get('light'))
            sensordata.temp = temp
            sensordata.light = light
            sensordata.lastupdate = datetime.datetime.now() + datetime.timedelta(hours=8)
            sensordata.movement = movement
            
            if movement == 1:
                sensordata.lastmovement = datetime.datetime.now() + datetime.timedelta(hours=8)
                
            sensordata.list.append((datetime.datetime.now()+ datetime.timedelta(hours=8)).strftime("%d %b %y, %I.%M.%S %p"))
            sensordata.list.append(str(temp))
            sensordata.list.append(str(moves))
            sensordata.put()
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
        if user:  # signed in already
            template_values = {
                'user_mail': users.get_current_user().email(),
                'logout': users.create_logout_url(self.request.host_url),
            }
            template = jinja_environment.get_template('frontuser.html')
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(self.request.host_url)

class Temperature(webapp2.RequestHandler):
    # Temperature

    def get(self):
        sense = ArduinoSensorData.get_or_insert('1')
        
        #user = users.get_current_user()
        #if user:  # signed in already
        template_values = {
            #'user_mail': users.get_current_user().email(),
            #'logout': users.create_logout_url(self.request.host_url),
            'listToRowData': listToRowData(sense.list),
            'temp': str(sense.temp),
            'timeSinceLastMovement': sense.lastmovement,
            'datetime': (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%d %b %y, %I.%M.%S %p"),
            'datetimeLastUpdate': str(sense.lastupdate.strftime("%d %b %y, %I.%M.%S %p")),
            }
        template = jinja_environment.get_template('temperature.html')
        self.response.out.write(template.render(template_values))
        #else:
        #    self.redirect(self.request.host_url)

class Light(webapp2.RequestHandler):
    # Light intensity

    def get(self):
        #user = users.get_current_user()
        #if user:  # signed in already
        sense = ArduinoSensorData.get_or_insert('1')
        template_values = {
            'listToRowData': listToRowData(sense.list),
            'light': str(sense.light),
            'datetime': (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%d %b %y, %I.%M.%S %p"),
            'datetimeLastUpdate': str(sense.lastupdate.strftime("%d %b %y, %I.%M.%S %p")),
            #'user_mail': users.get_current_user().email(),
            #'logout': users.create_logout_url(self.request.host_url),
        }
        template = jinja_environment.get_template('light.html')
        self.response.out.write(template.render(template_values))
        #else:
        #    self.redirect(self.request.host_url)

class Motion(webapp2.RequestHandler):
    # Motion



    def get(self):
        #user = users.get_current_user()
        #if user:  # signed in already
        sense = ArduinoSensorData.get_or_insert('1')
        if (sense.movement):
            motionStatusString = "present"
        else: 
            motionStatusString = "not present"
        template_values = {
            'datetimeLastMovement': str(sense.lastmovement.strftime("%d %b %y, %I.%M.%S %p")),
            'datetime': (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%d %b %y, %I.%M.%S %p"),
            'datetimeLastUpdate': str(sense.lastupdate.strftime("%d %b %y, %I.%M.%S %p")),
            'motionStatusString': motionStatusString,
            #'user_mail': users.get_current_user().email(),
            #'logout': users.create_logout_url(self.request.host_url),
        }
        template = jinja_environment.get_template('motion.html')
        self.response.out.write(template.render(template_values))
        #else:
        #    self.redirect(self.request.host_url)

class History(webapp2.RequestHandler):
    # History

    def get(self):
        sense = ArduinoSensorData.get_or_insert('1')
        #user = users.get_current_user()
        #if user:  # signed in already
        template_values = {
            #'user_mail': users.get_current_user().email(),
            #'logout': users.create_logout_url(self.request.host_url),
            'listToRowData': listToRowData(sense.list),
            'datetime': datetime.datetime.now(),
        }
        template = jinja_environment.get_template('history.html')
        self.response.out.write(template.render(template_values))
        #else:
        #    self.redirect(self.request.host_url)


class Settings(webapp2.RequestHandler):
    # Settings

    def get(self):
        user = users.get_current_user()
        if user:  # signed in already
            template_values = {
                'user_mail': users.get_current_user().email(),
                'logout': users.create_logout_url(self.request.host_url),
            }
            template = jinja_environment.get_template('settings.html')
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(self.request.host_url)

      
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/arduino_post', ArduinoPost),
                               ('/mainuser', MainPageUser),
                               ('/temperature', Temperature),
                               ('/light', Light),
                               ('/motion', Motion),
                               ('/history', History),
                               ('/settings', Settings)],
                              debug=True)


########HelperFunction########
 
def listToRowData(list):
    #'[new Date(year, month, day, hours, minutes, seconds), Temperature, Moves],\n'
    str1 =''
    for i in range(0,len(list)-2,3):
        str1 = str1 + '\t[ new Date(' + list[i] + '), ' + list[i+1] + ', ' + list[i+2] + '],\n'
    return str1
 
def generateDHMString(difference):
    #60 seconds * 60 minutes * 24 hours
    hours = difference.seconds // 3600
    temp = difference.seconds - (hours * 3600)
    minutes = temp // 60
    seconds = temp - (minutes * 60)
    andVal = False
    ret = str(seconds) + (" second ago" if seconds == 1 else " seconds ago!")
    if minutes != 0:
        str1 = " minute " if minutes == 1 else " minutes "
        andVal = True
        ret = str(minutes) + str1 + "and " + ret
    if hours !=0:
        str1 = " hour" if hours == 1 else " hours"
        if andVal:
            ret = str(hours) + str1 + ", " + ret
        else:
            andVal=True
            ret = str(hours) + str1 + " and " + ret
    if difference.days !=0:
        str1 = " day" if difference.days == 1 else " days"
        if andVal:
            ret = str(difference.days) + str1 + ", " + ret
        else:
            ret = str(difference.days) + str1 + " and " + ret
    return ret
 
def main():
    run_wsgi_app(application)
 
if __name__ == '__main__':
    main()
