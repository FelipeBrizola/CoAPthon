import time
from random import randint
from coapthon import defines

from coapthon.resources.resource import Resource

__author__ = 'Felipe Brizola'

class TemperatureResource(Resource):
    def __init__(self, name="temperature", coap_server=None):
        super(TemperatureResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = None
        self.content_type = "text/plain"

    def render_GET(self, request):
        self.payload = str(randint(0, 40)) + ' C'
        return self

class WindResource(Resource):
    def __init__(self, name="wind", coap_server=None):
        super(WindResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = None
        self.content_type = "text/plain"

    def render_GET(self, request):
        self.payload = self.payload = str(randint(0, 200)) + ' km/h'
        return self

class HumidityResource(Resource):
    def __init__(self, name="humidity", coap_server=None):
        super(HumidityResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = None
        self.content_type = "text/plain"

    def render_GET(self, request):
        self.payload = str(randint(0, 100)) + ' %'
        return self

class PrecipitationResource(Resource):
    def __init__(self, name="precipitation", coap_server=None):
        super(PrecipitationResource, self).__init__(name, coap_server, visible=True,
                                            observable=True, allow_children=True)
        self.payload = None
        self.content_type = "text/plain"

    def render_GET(self, request):
        self.payload = str(randint(0, 100)) + ' cm'
        return self
