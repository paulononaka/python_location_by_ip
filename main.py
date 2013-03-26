import os
import urllib2
import md5
import time

import pprint
import xml.dom.minidom
from xml.dom.minidom import Node, parse, parseString

from maps import PyMap
from google.appengine.ext import webapp
from google.appengine.ext.webapp.template import render
from google.appengine.ext.webapp.util import run_wsgi_app

class MainHandler(webapp.RequestHandler):
    def get(self):
        context = {}
        tmpl = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(render(tmpl, context))

class SearchIP(webapp.RequestHandler):
    def post(self):

        ip = self.request.get('ip')
        service = 'http://api.quova.com/'
        version = 'v1/'
        method = 'ipinfo/'
        apikey = '100.tkdykh8mvt7uut8ychhv'
        secret = 'Pd3c9pzT'
        
        hash = md5.new()
        timestamp = str(int(time.time()))
        sig = md5.new(apikey + secret + timestamp).hexdigest()
        url = service + version + method + ip + '?apikey=' + apikey + '&sig=' + sig + '&format=xml'
        xml = urllib2.urlopen(url).read()
        
        doc = parseString(xml)

        ip_address = doc.getElementsByTagName('ip_address')[0].firstChild.nodeValue
        organization = doc.getElementsByTagName('organization')[0].firstChild.nodeValue
        carrier = doc.getElementsByTagName('carrier')[0].firstChild.nodeValue
        sld = doc.getElementsByTagName('sld')[0].firstChild.nodeValue
        country = doc.getElementsByTagName('country')[0].firstChild.nodeValue
        state = doc.getElementsByTagName('state')[0].firstChild.nodeValue
        city = doc.getElementsByTagName('city')[0].firstChild.nodeValue
        postal_code = doc.getElementsByTagName('postal_code')[0].firstChild.nodeValue
        lat = doc.getElementsByTagName('latitude')[0].firstChild.nodeValue
        lon = doc.getElementsByTagName('longitude')[0].firstChild.nodeValue

        g = PyMap()
        g.key = "ABQIAAAAGcWIjwYvD9qHwmbKuSQEsxQ_LYszwfeN3sChNNHex23LZKwkgRTB3_7Qo5_EhYBGijp8h1khiBFjkg"
        g.maps[0].zoom = 12
        s = [lat,lon, ip_address+'<br>'+organization+'<br>'+carrier+'<br>'+sld+'<br>'+country+'<br>'+state+'<br>'+city+'<br>'+postal_code+'<br>'+lat+'<br>'+lon]
        g.maps[0].setpoint(s)
	g.maps[0].center = (lat,lon)
        self.response.out.write(g.showhtml())

application = webapp.WSGIApplication([
    ( '/', MainHandler),
    ( '/searchIP', SearchIP),
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
