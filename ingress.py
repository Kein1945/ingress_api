# -*- coding: utf-8 -*-
import urllib2
import cookielib
import codecs
import json


SAINT_PETERSBURG = {'minLat': 56830944, 'minLng': 27443848, 'maxLat': 61042332, 'maxLng': 35551758}
SAINT_PETERSBURG_CITY = {'minLat': 59326840, 'minLng': 29116741, 'maxLat': 60371064, 'maxLng': 31588665}
SAINT_PETERSBURG_POINT = {'lat': 59934103, 'lng': 30339024}


class rpc:
    def __init__(self, cookieFile, token, debug=False):
        self.cookieFile = cookieFile
        self.cookies = cookielib.LWPCookieJar()
        self.cookies.load(self.cookieFile)
        handlers = [
            urllib2.HTTPHandler(),
            urllib2.HTTPSHandler(),
            urllib2.HTTPCookieProcessor(self.cookies)
        ]
        self.opener = urllib2.build_opener(*handlers)
        self.token = token
        self.debug = debug

    def buildRequest(self, uri):
        """
        Build request for success query
        """
        req = urllib2.Request(uri)
        req.add_header('X-CSRFToken', self.token)
        req.add_header('Referer', 'http://www.ingress.com/intel')
        req.add_header('Accept-Charset', 'utf-8')
        req.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31')
        return req

    def loadData(self, uri, form_data):
        """
        Load data for uri(command) and data,
        and return Object
        """
        req = self.buildRequest(uri)
        data_encoded = json.dumps(form_data)
        if self.debug:
            print data_encoded
        resp = self.opener.open(req, data_encoded)
        self.cookies.save(self.cookieFile)
        return json.loads(resp.read().replace('\"', '\\"').decode('unicode-escape').replace("\t", ' '))


class command(object):
    def __init__(self, rpc, url):
        self.rpc = rpc
        self.url = url

    def proceed(self):
        return self.rpc.loadData(self.url, self.form_data)


class events(command):
    url = 'http://www.ingress.com/rpc/dashboard.getPaginatedPlextsV2'
    def __init__(self, rpc, view=SAINT_PETERSBURG):
        self.form_data = {
            "minTimestampMs": -1,
            "maxTimestampMs": -1,
            "method": "dashboard.getPaginatedPlextsV2"
        }
        self.setView(view)
        super(events, self).__init__(rpc, events.url)

    def setView(self, view):
        self.form_data["minLatE6"] = view['minLat']
        self.form_data["minLngE6"] = view['minLng']
        self.form_data["maxLatE6"] = view['maxLat']
        self.form_data["maxLngE6"] = view['maxLng']

    def retrieve(self, count=150):
        self.form_data["desiredNumItems"] = count
        return self.proceed()


class message(command):
    url = 'http://www.ingress.com/rpc/dashboard.sendPlext'
    def __init__(self, rpc, point=SAINT_PETERSBURG_POINT, faction_only=True):
        self.form_data = {
            "method": "dashboard.sendPlext"
        }
        if faction_only:
            self.setPrivate()
        else:
            self.setPublic()
        self.setPoint(point)
        super(message, self).__init__(rpc, message.url)

    def setPrivate(self):
        self.setFactionOnly(True)

    def setPublic(self):
        self.setFactionOnly(False)

    def setFactionOnly(self, faction_only):
        self.form_data['factionOnly'] = faction_only

    def setPoint(self, point):
        self.form_data["latE6"] = point['lat']
        self.form_data["lngE6"] = point['lng']

    def send(self, text):
        self.form_data["message"] = text
        if len(text):
            return self.proceed()
        else:
            raise Exception("Text should be not empty")


class chat(command):
    url = 'http://www.ingress.com/rpc/dashboard.getPaginatedPlextsV2'
    def __init__(self, rpc, view=SAINT_PETERSBURG_CITY, faction_only=True):
        self.form_data = {
            "method": "dashboard.getPaginatedPlextsV2",
            "minTimestampMs": -1,
            "maxTimestampMs": -1
        }
        if faction_only:
            self.setPrivate()
        else:
            self.setPublic()
        self.setView(view)
        super(chat, self).__init__(rpc, chat.url)

    def setPrivate(self):
        self.setFactionOnly(True)

    def setPublic(self):
        self.setFactionOnly(False)

    def setFactionOnly(self, faction_only):
        self.form_data['factionOnly'] = faction_only

    
    def setView(self, view):
        self.form_data["minLatE6"] = view['minLat']
        self.form_data["minLngE6"] = view['minLng']
        self.form_data["maxLatE6"] = view['maxLat']
        self.form_data["maxLngE6"] = view['maxLng']

    def retrieve(self, count=150):
        self.form_data["desiredNumItems"] = count
        return self.proceed()
