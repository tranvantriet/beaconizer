############################### LICENSE #######################################
# Copyright (c) 2010, Sajal Kayan                                             #
# All rights reserved.                                                        #
# Redistribution and use in source and binary forms, with or without          #
# modification, are permitted provided that the following conditions are met: #
#                                                                             #
# 1) Redistributions of source code must retain the above copyright notice,   #
#    this list of conditions and the following disclaimer.                    #
# 2) Redistributions in binary form must reproduce the above copyright notice,#
#    this list of conditions and the following disclaimer in the documentation#
#    and/or other materials provided with the distribution.                   #
# 3) The names of its contributors may be used to endorse or promote products #
#    derived from this software without specific prior written permission.    #
#                                                                             #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" #
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE   #
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE  #
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE   #
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR         #
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF        #
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS    #
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN     #
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)     #
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE  #
# POSSIBILITY OF SUCH DAMAGE.                                                 #
###############################################################################


from google.appengine.ext import webapp
from models import Beacon
import pprint
from django.utils import simplejson
import datetime
import os
from google.appengine.ext.webapp import template

class JSONEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S')
        else:
            return simplejson.JSONEncoder.default(self, obj)


class ShowBeacons(webapp.RequestHandler):

    def get(self, id, format="html"):
#        self.response.out.write('showing.... --%s-- ...' % (id))
        query = Beacon.all()
        query.filter('testid =', id).order('-timestamp')
        beacons = []
        for be in query.fetch(10, 0):
            customvars = []
            for prop in be.dynamic_properties():
                customvars += [{
                                "varname": prop.replace("custom__",""),
                                "varvalue" :  getattr(be, prop)
                                }]

            beacon = {'timestamp' : be.timestamp,
                         'type': be.type,
                         'IP': be.IP,
                         'refer': be.refer,
                         'useragent': be.useragent,
                         'customvars': customvars,
                         }
                
            beacons += [beacon]
        pp = pprint.PrettyPrinter(indent=4)
#        print pp.pprint(beacons)
        if self.request.get("format") == "json":
            #todo process and output json
            self.response.headers['Content-Type'] = 'application/json'
            j = JSONEncoder().encode(beacons)
            self.response.out.write(j)
        else:
            #todo make and render into html template
            template_values = { 'testid': id,
                               'beacons': beacons,
                               }
            path = os.path.join(os.path.dirname(__file__), 'templates/show.html')
            self.response.out.write(template.render(path, template_values))
        #        self.response.out.write(pp.pprint(beacons))
        


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