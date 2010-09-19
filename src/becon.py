from google.appengine.ext import webapp
from models import Beacon



class ShowBeacons(webapp.RequestHandler):

    def get(self, id):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('showing.... --%s-- ...' % (id))
        query = Beacon.all()
        query.filter('testid =', id).order('-timestamp')
        beacons = []
        for be in query.fetch(10, 0):
            customvars = {}
            for prop in be.dynamic_properties():
                customvars[prop.replace("custom__","")] = getattr(be, prop)

            beacon = {'timestamp' : be.timestamp,
                         'type': be.type,
                         'IP': be.IP,
                         'refer': be.refer,
                         'useragent': be.useragent,
                         'customvars': customvars,
                         }
                
            beacons += [beacon]
        self.response.out.write("\n" + str(beacons))
        


class ConsumeBeacons(webapp.RequestHandler):

    def GetHeader(self, header):
        try:
            return self.request.headers[header]
        except:
            return None

    def consume(self, id, vars={} , type="GET"):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Consuming.... --%s-- nom nom nom...' % (id))
        self.response.out.write(vars)
        b = Beacon(IP = self.request.remote_addr, type=type, testid=id)
        b.useragent = self.GetHeader("User-Agent")
        b.refer = self.GetHeader("Referer")
        for var in vars:
            self.response.out.write("\n")
            self.response.out.write(var + ": " + vars[var])
            setattr(b, "custom__" + var, vars[var])
            
        b.put()
        self.response.out.write("\n\n")
        self.response.out.write(b)


    def get(self, id):
        vars = {}
        for arg in self.request.arguments():
            vars[arg] = self.request.get(arg)
        self.consume(id, vars )

    def post(self, id):
        self.consume(id)