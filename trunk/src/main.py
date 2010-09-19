from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from becon import ConsumeBeacons, ShowBeacons

class MainPage(webapp.RequestHandler):
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Under Construction!')




application = webapp.WSGIApplication([('/', MainPage),
                                     ('/consume/(.*)', ConsumeBeacons),
                                     ('/show/(.*)', ShowBeacons),
                                     ],
                                      debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
