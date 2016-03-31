from __future__ import unicode_literals
from itertools import product, izip

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from sqlalchemy import text
from sqlalchemy.orm import joinedload, aliased

from clld.db.meta import DBSession

from concepticon.models import Concept, Relation, ConceptSet


@view_config(route_name='search_concept')
def search_concept(req):
    if 'url' in req.params:
        for concept in DBSession.query(Concept)\
                .filter(text("""jsondata ilike '%"url":%'"""))\
                .filter(text("""jsondata ilike '%%%s%%'""" % req.params['url'])):
            if req.params['url'] == concept.jsondata.get('url'):
                raise HTTPFound(location=req.resource_url(concept))
    raise HTTPNotFound()


@view_config(route_name='relations', renderer='json')
def relations(req):
    csids = ['%s' % i for i in [
        2420,
        2421,
        1761,
        562,
        561,
        427,
        2419,
        2418,
        1263,
        1758,
        1760,
        1640,
        405,
        2417,
        2416,
        1262,
        560,
        559,
        1759,
        2415,
        2414,
    ]]
    res = dict(edges=[], nodes=[])
    nodes = {}
    source = aliased(ConceptSet)
    target = aliased(ConceptSet)
    for rel in DBSession.query(Relation) \
            .join(source, Relation.source_pk == source.pk)\
            .join(target, Relation.target_pk == target.pk) \
            .filter(source.id.in_(csids)) \
            .filter(target.id.in_(csids)) \
            .options(joinedload(Relation.source), joinedload(Relation.target)):
        res['edges'].append(dict(
            id=str(rel.pk),
            label=rel.description,
            size=0.5,
            source=rel.source.id,
            target=rel.target.id))
        for node in [rel.source, rel.target]:
            nodes[node.id] = dict(id=node.id, label=node.name, size=1)

    for node, (x, y) in izip(nodes.values(), product(range(5), range(5))):
        node['x'], node['y'] = x, y
        res['nodes'].append(node)

    return res
