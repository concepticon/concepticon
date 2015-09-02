from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from sqlalchemy import text

from clld.db.meta import DBSession

from concepticon.models import Concept


def search_concept(req):
    if 'url' in req.params:
        for concept in DBSession.query(Concept)\
                .filter(text("""jsondata ilike '%"url":%'"""))\
                .filter(text("""jsondata ilike '%%%s%%'""" % req.params['url'])):
            if req.params['url'] == concept.jsondata.get('url'):
                raise HTTPFound(location=req.resource_url(concept))
    raise HTTPNotFound()
