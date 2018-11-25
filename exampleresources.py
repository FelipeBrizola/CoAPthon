import time
from random import randint
from coapthon import defines

from coapthon.resources.resource import Resource

__author__ = 'Felipe Brizola'

class TemperatureResource(Resource):
    def __init__(self, name="temperature", coap_server=None):
        super(TemperatureResource, self).__init__(name, coap_server, visible=True,
                                            observable=False, allow_children=True)
        self.payload = None
        self.content_type = "text/plain"

    def render_GET(self, request):
        self.payload = str(randint(0, 40)) + ' C'
        return self

class WindResource(Resource):
    def __init__(self, name="wind", coap_server=None):
        super(WindResource, self).__init__(name, coap_server, visible=True,
                                            observable=False, allow_children=True)
        self.payload = None
        self.content_type = "text/plain"

    def render_GET(self, request):
        self.payload = self.payload = str(randint(0, 200)) + ' km/h'
        return self

class HumidityResource(Resource):
    def __init__(self, name="humidity", coap_server=None):
        super(HumidityResource, self).__init__(name, coap_server, visible=True,
                                            observable=False, allow_children=True)
        self.payload = None
        self.content_type = "text/plain"

    def render_GET(self, request):
        self.payload = str(randint(0, 100)) + ' %'
        return self

class PrecipitationResource(Resource):
    def __init__(self, name="precipitation", coap_server=None):
        super(PrecipitationResource, self).__init__(name, coap_server, visible=True,
                                            observable=False, allow_children=True)
        self.payload = None
        self.content_type = "application/json"

    def render_GET(self, request):
        
        self.payload = {
            'precipitation': str(randint(0, 100)),
            'unit': 'cm'
        }
        return self


class LightResource(Resource):
    def __init__(self, name="light", coap_server=None):
        super(LightResource, self).__init__(name, coap_server, visible=True,
                                            observable=False, allow_children=False)
        self.payload = None
        self.content_type = "text/plain"

    def render_GET(self, request):
        self.payload = str(randint(0, 1))
        return self

class PresenceResource(Resource):
    def __init__(self, name="presence", coap_server=None):
        super(PresenceResource, self).__init__(name, coap_server, visible=True,
                                            observable=False, allow_children=False)
        self.payload = None
        self.content_type = "text/plain"

    def render_GET(self, request):
        self.payload = str(randint(0, 1))
        return self

class CamResource(Resource):
    def __init__(self, name="cam", coap_server=None):
        super(CamResource, self).__init__(name, coap_server, visible=True,
                                            observable=False, allow_children=False)
        self.payload = ''
        self.content_type = "application/octet-stream"

    def render_GET(self, request):
        for i in range(500):
            self.payload += str(randint(0, 1))

        return self


class IdentifierResource(Resource):
    def __init__(self, name="identifier", coap_server=None):
        super(IdentifierResource, self).__init__(name, coap_server, visible=True,
                                            observable=False, allow_children=True)
        self.payload = None
        self.content_type = "application/json"

    def render_GET(self, request):
        self.payload = { 'id': str(randint(0, 100)) }
        return self

class WeightResource(Resource):
    def __init__(self, name="weight", coap_server=None):
        super(WeightResource, self).__init__(name, coap_server, visible=True,
                                            observable=False, allow_children=True)
        self.payload = None
        self.content_type = "application/json"

    def render_GET(self, request):
        self.payload = {
            'weight': str(randint(0, 100)),
            'unit': 'kg'
        }
        return self

class FoodResource(Resource):
    def __init__(self, name="food", coap_server=None):
        super(FoodResource, self).__init__(name, coap_server, visible=True,
                                            observable=False, allow_children=True)
        self.payload = None
        self.content_type = "application/json"

    def render_GET(self, request):
        self.payload = {
            'level': str(randint(0, 100)),
            'unit': '%'
        }
        return self

class WaterResource(Resource):
    def __init__(self, name="water", coap_server=None):
        super(WaterResource, self).__init__(name, coap_server, visible=True,
                                            observable=False, allow_children=True)
        self.payload = None
        self.content_type = "application/json"

    def render_GET(self, request):
        self.payload = {
            'level': str(randint(0, 100)),
            'unit': '%'
        }
        return self