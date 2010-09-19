from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class MainPage(webapp.RequestHandler):
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Under Construction!')


class ConsumeBeacon(webapp.RequestHandler):

    def consume(self, id, vars=[]):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Consuming.... --%s-- nom nom nom...' % (id))
        self.response.out.write(vars)

    def get(self, id):
        vars = [{arg: self.request.get(arg)}  for arg in self.request.arguments()]
        self.consume(id, vars )

    def post(self, id):
        self.consume(id)

application = webapp.WSGIApplication([('/', MainPage),
                                     ('/consume/(.*)', ConsumeBeacon)
                                     ],
                                      debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
