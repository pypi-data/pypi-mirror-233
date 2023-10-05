from velikafkaclient.decorators import ctracing


class BaseHandler:
    web_integrator = None
    ios_integrator = None
    android_integrator = None
    event_model = None

    def __init__(self, event_name):
        self.event_name = event_name

    def set_data(self, event_data, source):
        return self.event_model(**event_data)

    @ctracing
    async def send_data(self, event_data):
        event_data = event_data.dict()
        source = event_data.get('source')
        model = await self.set_data(event_data, source)
        integrator_instances = {
            'web': self.web_integrator,
            'ios': self.ios_integrator,
            'android': self.android_integrator
        }
        await integrator_instances[source](model=model).create_object()
