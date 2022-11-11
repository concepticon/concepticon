from pyramid.config import Configurator

from clld.interfaces import IDownload

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
_('Unit')
_('Units')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.include('clld_markdown_plugin')
    cldf = config.registry.queryUtility(IDownload, name='dataset.cldf')
    assert config.registry.unregisterUtility(cldf, name='dataset.cldf')
    config.add_route('search_concept', '/search_concept')
    config.add_route('relations', '/relations')
    return config.make_wsgi_app()
