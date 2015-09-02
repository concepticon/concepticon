from pyramid.config import Configurator

# we must make sure custom models are known at database initialization!
from concepticon import models
from concepticon.views import search_concept


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
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.add_route('search_concept', '/search_concept')
    config.add_view(search_concept, route_name='search_concept')
    return config.make_wsgi_app()
