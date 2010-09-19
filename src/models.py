from google.appengine.ext import db

class Beacon(db.Expando):
    IP = db.StringProperty(required=True)
    type = db.StringProperty(required=True, choices=set(["GET", "POST"]))
    timestamp = db.DateTimeProperty(auto_now_add=True)
    refer = db.StringProperty(required=False)
    useragent = db.StringProperty(required=False)
    testid = db.StringProperty(required=True)