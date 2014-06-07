import webapp2
import jinja2
import os

from google.appengine.api import users


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"))

class MainPage(webapp2.RequestHandler):
  """ Handler for the front page."""
  def get(self):
      template = jinja_environment.get_template('front.html')
      self.response.out.write(template.render())

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
        user = users.get_current_user()
        if user:  # signed in already
            template_values = {
                'user_mail': users.get_current_user().email(),
                'logout': users.create_logout_url(self.request.host_url),
            }
            template = jinja_environment.get_template('temperature.html')
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(self.request.host_url)

class Light(webapp2.RequestHandler):
    # Light intensity

    def get(self):
        user = users.get_current_user()
        if user:  # signed in already
            template_values = {
                'user_mail': users.get_current_user().email(),
                'logout': users.create_logout_url(self.request.host_url),
            }
            template = jinja_environment.get_template('light.html')
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(self.request.host_url)

class Motion(webapp2.RequestHandler):
    # Motion

    def get(self):
        user = users.get_current_user()
        if user:  # signed in already
            template_values = {
                'user_mail': users.get_current_user().email(),
                'logout': users.create_logout_url(self.request.host_url),
            }
            template = jinja_environment.get_template('motion.html')
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(self.request.host_url)

class History(webapp2.RequestHandler):
    # History

    def get(self):
        user = users.get_current_user()
        if user:  # signed in already
            template_values = {
                'user_mail': users.get_current_user().email(),
                'logout': users.create_logout_url(self.request.host_url),
            }
            template = jinja_environment.get_template('history.html')
            self.response.out.write(template.render(template_values))
        else:
            self.redirect(self.request.host_url)


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
                               ('/mainuser', MainPageUser),
                               ('/temperature', Temperature),
                               ('/light', Light),
                               ('/motion', Motion),
                               ('/history', History),
                               ('/settings', Settings)],
                              debug=True)
