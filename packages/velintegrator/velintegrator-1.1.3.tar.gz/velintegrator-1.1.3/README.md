VELIntegrator - Package for third-party integrations ;)

Description
This module helps you to have a base class of Integrator and CRUDIntegrator, 
which are used to connect to third-party service providers.

Integrator Base class provide request validation posting data in different services, 
CRUDIntegrator helps to create, read, update and delete objects in third-party services.

There are also handler Base class, for handling data before sending it. you can find it in handler.py

Base handler attributes: 

class BaseHandler:
    web_integrator = None
    ios_integrator = None
    android_integrator = None
    event_model = None
    params_methods_mapper = {}
    base_params_method = None
    params_method = None
    tracing_id = None


feel free to use it.

