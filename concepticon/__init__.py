from clld.web.app import get_configurator

# we must make sure custom models are known at database initialization!
from concepticon import models


_ = lambda i: i
_('Contributor')
_('Contributors')
_('Contribution')
_('Contributions')
_('Parameter')
_('Parameters')
_('Value')
_('Values')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = get_configurator('concepticon', settings=settings)
    config.include('clldmpg')
    config.include('concepticon.datatables')
    config.include('concepticon.adapters')
    config.include('concepticon.maps')
    return config.make_wsgi_app()
