# coding: utf-8
from __future__ import unicode_literals, division
import sys
import re
from collections import Counter
from decimal import Decimal
from _functools import partial

from clld.scripts.util import initializedb, Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.bibtex import Database
from clldutils.misc import slug
from clldutils.jsonlib import load
from pyconcepticon.api import Concepticon
from pyconcepticon.util import BIB_PATTERN
from markdown import markdown

import concepticon
from concepticon import models


# Missing data (in the sources) is marked using a dash. We don't import these markers in
# the database but regard absence of data in the database as absence of data in the
# sources.
NA = '-'


def strip_braces(s):
    s = s.strip()
    if s.startswith('{'):
        s = s[1:]
    if s.endswith('}'):
        s = s[:-1]
    return s.strip()


def main(args):
    data = Data()

    api = Concepticon(args.data_file('concepticon-data'))
    dataset = common.Dataset(
        id=concepticon.__name__,
        name="Concepticon",
        publisher_name="Max Planck Institute for the Science of Human History",
        publisher_place="Jena",
        publisher_url="http://www.shh.mpg.de",
        license="http://creativecommons.org/licenses/by/4.0/",
        contact='concepticon@shh.mpg.de',
        domain='concepticon.clld.org',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'})
    DBSession.add(dataset)
    for i, ed in enumerate(api.editors):
        if not ed.end:
            c = common.Contributor(id=slug(ed.name), name=ed.name)
            dataset.editors.append(common.Editor(contributor=c, ord=i))

    TAGS = {k: v for k, v in load(api.data_path('concepticon.json'))['TAGS'].items()}

    english = data.add(common.Language, 'eng', id='eng', name='English')
    for name, description in TAGS.items():
        data.add(models.Tag, name, id=slug(name), name=name, description=description)

    for rec in Database.from_file(api.bibfile, lowercase=True):
        source = data.add(common.Source, rec.id, _obj=bibtex2source(rec, lowercase_id=True))
        if rec.id in api.sources:
            spec = api.sources[rec.id]
            DBSession.flush()
            DBSession.add(common.Source_files(
                mime_type=spec['mimetype'], object_pk=source.pk, jsondata=spec))

    data.add(
        models.ConceptSet,
        NA,
        id='0',
        name='<NA>',
        description='Set of all concepts not yet mapped to a meaningful concept set')

    for concept in api.conceptsets.values():
        data.add(
            models.ConceptSet,
            concept.id,
            id=concept.id,
            name=concept.gloss,
            description=concept.definition,
            semanticfield=concept.semanticfield,
            ontological_category=concept.ontological_category)

    for rel in api.relations.raw:
        DBSession.add(models.Relation(
            source=data['ConceptSet'][rel['SOURCE']],
            target=data['ConceptSet'][rel['TARGET']],
            description=rel['RELATION']))

    number_pattern = re.compile('(?P<number>[0-9]+)(?P<suffix>.*)')

    for cl in api.conceptlists.values():
        conceptlist = data.add(
            models.Conceptlist,
            cl.id,
            id=cl.id,
            name=' '.join(cl.id.split('-')),
            description=cl.note,
            target_languages=cl.target_language,
            source_languages=' '.join(cl.source_language),
            year=cl.year,
        )
        for id_ in cl.refs:
            common.ContributionReference(
                source=data['Source'][id_], contribution=conceptlist)

        for tag in cl.tags or ['specific']:
            DBSession.add(models.ConceptlistTag(
                conceptlist=conceptlist, tag=data['Tag'][tag]))

        for i, name in enumerate(re.split('\s+(?:and|AND)\s+', cl.author)):
            name = strip_braces(name)
            cid = slug(name)
            contrib = data['Contributor'].get(cid)
            if not contrib:
                contrib = data.add(common.Contributor, cid, id=cid, name=name)
            DBSession.add(common.ContributionContributor(
                ord=i, contribution=conceptlist, contributor=contrib))
        #for k in 'ID NOTE TARGET_LANGUAGE SOURCE_LANGUAGE YEAR REFS AUTHOR'.split():
        #    del cl[k]
        #DBSession.flush()
        #for k, v in cl.items():
        #    if k not in ['ITEMS', 'TAGS', 'PDF'] and v and v != NA:
        #        DBSession.add(common.Contribution_data(
        #            object_pk=conceptlist.pk, key=k, value=v))

        for concept in cl.concepts.values():
            lgs = {}
            for lang in cl.source_language:
                v = getattr(concept, lang, concept.attributes.get(lang))
                if v:
                    if v == NA:
                        print('missing %s translation in %s' % (lang, concept.id))
                    lgs[lang] = v
                else:
                    raise ValueError(
                        'missing %s translation in %s' % (lang, conceptlist.id))

            match = number_pattern.match(concept.number)
            if not match:
                raise ValueError
            vsid = (english.id, conceptlist.id, data['ConceptSet'][concept.concepticon_id or NA])
            vs = data['ValueSet'].get(vsid)
            if not vs:
                vs = data.add(
                    common.ValueSet,
                    vsid,
                    id=concept.id,
                    description=concept.label,
                    language=english,
                    contribution=conceptlist,
                    parameter=data['ConceptSet'][concept.concepticon_id or NA])
            v = models.Concept(
                id=concept.id,
                valueset=vs,
                description=concept.gloss,  # our own gloss, if available
                name='; '.join('%s [%s]' % (lgs[l], l) for l in sorted(lgs.keys())),
                number=int(match.group('number')),
                number_suffix=match.group('suffix'),
                jsondata={
                    k: float(v) if isinstance(v, Decimal) else (v.unsplit() if hasattr(v, 'unsplit') else v)
                    for k, v in concept.attributes.items()
                    if k not in cl.source_language})
            DBSession.flush()
            #
            # TODO: map these to Gloss ínstances!
            #
            for key, value in lgs.items():
                DBSession.add(
                    common.Value_data(key='lang_' + key, value=value, object_pk=v.pk))

    for md in api.metadata.values():
        provider = models.MetaProvider(
            id=md.id,
            name=md.meta['dc:title'],
            description=md.meta['dc:description'],
            url=md.meta['dc:source'],
            jsondata=md.meta)
        for meta in md.values.values():
            for k, v in meta.items():
                if v and k != 'CONCEPTICON_ID':
                    models.ConceptSetMeta(
                        metaprovider=provider,
                        conceptset=data['ConceptSet'][meta['CONCEPTICON_ID']],
                        key=k,
                        value=v)

    for obj_type, retirements in load(api.path('concepticondata', 'retired.json')).items():
        model = {
            'Concept': common.Value,
            'ConceptList': common.Contribution,
        }[obj_type]
        for spec in retirements:
            common.Config.add_replacement(spec['id'], spec['replacement'], model=model)


def similarity(cl1, cl2):
    cs1 = set(c.parameter_pk for c in cl1.valuesets)
    cs2 = set(c.parameter_pk for c in cl2.valuesets)
    return len(cs1.intersection(cs2)) / len(cs1.union(cs2))


def uniqueness(cl):
    try:
        return sum([1 / len(c.parameter.valuesets) for c in cl.valuesets]) / len(cl.valuesets)
    except ZeroDivisionError:
        return 0

REF_PATTERN = re.compile(':ref:(?P<id>[^\)]+)')


def link_conceptlists(req, s):
    if not s:
        return ''  # pragma: no cover

    def repl(cls, m, lower=False):
        id_ = m.group('id')
        if lower:
            id_ = id_.lower()
        obj = cls.get(id_, default=None)
        return req.resource_url(obj) if obj else m.group('id')

    return markdown(
        BIB_PATTERN.sub(
            partial(repl, common.Source, lower=True),
            REF_PATTERN.sub(partial(repl, common.Contribution), s)))


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    for concept in DBSession.query(models.ConceptSet):
        concept.representation = len(concept.valuesets)

    for clist in DBSession.query(models.Conceptlist):
        clist.items = len(clist.valuesets)
        clist.uniqueness = uniqueness(clist)
        clist.description = link_conceptlists(args.env['request'], clist.description)

        similar = Counter()
        for other in DBSession.query(models.Conceptlist):
            if other != clist:
                similar[other.id] = similarity(clist, other)

        clist.update_jsondata(most_similar=similar.most_common(n=5))


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache, bootstrap=True)
    sys.exit(0)
