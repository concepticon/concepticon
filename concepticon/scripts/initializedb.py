from __future__ import unicode_literals, division
import sys
import re
from itertools import combinations
from collections import Counter

from clld.scripts.util import initializedb, Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.bibtex import Database
from clldutils.dsv import reader as _reader
from clldutils.jsonlib import load
from clldutils.misc import slug

import concepticon
from concepticon import models


def reader(*args, **kw):
    kw.setdefault('delimiter', '\t')
    return _reader(*args, **kw)


def split(s, sep=','):
    return [ss.strip() for ss in s.split(sep) if ss.strip()]


def strip_braces(s):
    s = s.strip()
    if s.startswith('{'):
        s = s[1:]
    if s.endswith('}'):
        s = s[:-1]
    return s.strip()


def main(args):
    data = Data()
    data_path = lambda *cs: args.data_file('concepticon-data', 'concepticondata', *cs)

    dataset = common.Dataset(
        id=concepticon.__name__,
        name="Concepticon 0.2",
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
    for i, name in enumerate(['Johann-Mattis List', 'Michael Cysouw', 'Robert Forkel']):
        c = common.Contributor(id=slug(name), name=name)
        dataset.editors.append(common.Editor(contributor=c, ord=i))

    english = data.add(
        common.Language, 'eng',
        id='eng',
        name='English')

    files = {}
    for fname in data_path('sources').iterdir():
        files[fname.stem] = \
            "https://github.com/clld/concepticon-data/blob/master/concepticondata/sources/%s" % fname.name

    for rec in Database.from_file(
            data_path('references', 'references.bib'), lowercase=True):
        source = data.add(common.Source, rec.id, _obj=bibtex2source(rec))
        if rec.id in files:
            DBSession.flush()
            DBSession.add(common.Source_files(
                mime_type='application/pdf',
                object_pk=source.pk,
                jsondata=dict(url=files[rec.id])))

    for concept in reader(data_path('concepticon.tsv'), namedtuples=True):
        data.add(
            models.ConceptSet,
            concept.ID,
            id=concept.ID,
            name=concept.GLOSS,
            description=concept.DEFINITION,
            semanticfield=concept.SEMANTICFIELD,
            ontological_category=concept.ONTOLOGICAL_CATEGORY)

    for rel in reader(data_path('conceptrelations.tsv'), namedtuples=True):
        DBSession.add(models.Relation(
            source=data['ConceptSet'][rel.SOURCE],
            target=data['ConceptSet'][rel.TARGET],
            description=rel.RELATION))

    unmapped = Counter()
    number_pattern = re.compile('(?P<number>[0-9]+)(?P<suffix>.*)')

    for cl in reader(data_path('conceptlists.tsv'), dicts=True):
        concepts = data_path('conceptlists', '%(ID)s.tsv' % cl)
        if not concepts.exists():
            continue
        langs = [l.lower() for l in split(cl['SOURCE_LANGUAGE'])]
        conceptlist = data.add(
            models.Conceptlist,
            cl['ID'],
            id=cl['ID'],
            name=' '.join(cl['ID'].split('-')),
            description=cl['NOTE'],
            target_languages=cl['TARGET_LANGUAGE'],
            source_languages=' '.join(langs),
            year=int(cl['YEAR']) if cl['YEAR'] else None,
        )
        for id_ in split(cl['REFS']):
            common.ContributionReference(
                source=data['Source'][id_], contribution=conceptlist)
        for i, name in enumerate(split(cl['AUTHOR'], sep=' and ')):
            name = strip_braces(name)
            contrib = data['Contributor'].get(name)
            if not contrib:
                contrib = data.add(
                    common.Contributor, name, id=slug(name), name=name)
            DBSession.add(common.ContributionContributor(
                ord=i, contribution=conceptlist, contributor=contrib))
        for k in 'ID NOTE TARGET_LANGUAGE SOURCE_LANGUAGE YEAR REFS AUTHOR'.split():
            del cl[k]
        DBSession.flush()
        for k, v in cl.items():
            DBSession.add(common.Contribution_data(
                object_pk=conceptlist.pk, key=k, value=v))

        for concept in reader(concepts, namedtuples=True):
            if not concept.ID or not concept.CONCEPTICON_ID or concept.CONCEPTICON_ID == 'NAN':
                #print conceptlist.id, getattr(concept, 'ENGLISH', getattr(concept, 'GLOSS', None))
                unmapped.update([conceptlist.id])
                continue

            lgs = {}
            for lang in langs:
                v = getattr(concept, lang.upper())
                if v:
                    lgs[lang] = v

            match = number_pattern.match(concept.NUMBER)
            if not match:
                print(concept.ID)
                raise ValueError
            vs = common.ValueSet(
                id=concept.ID,
                description=getattr(concept, 'GLOSS', getattr(concept, 'ENGLISH', None)),
                language=english,
                contribution=conceptlist,
                parameter=data['ConceptSet'][concept.CONCEPTICON_ID])
            d = {}
            for key, value in concept.__dict__.items():
                if not key.startswith('CONCEPTICON_') and \
                        key not in ['NUMBER', 'ID', 'GLOSS'] + [l.upper() for l in langs]:
                    d[key.lower()] = value
            v = models.Concept(
                id=concept.ID,
                valueset=vs,
                description=getattr(concept, 'GLOSS', None),  # our own gloss, if available
                name='; '.join('%s [%s]' % (lgs[l], l) for l in sorted(lgs.keys())),
                number=int(match.group('number')),
                number_suffix=match.group('suffix'),
                jsondata=d)
            DBSession.flush()
            for key, value in lgs.items():
                DBSession.add(
                    common.Value_data(key='lang_' + key, value=value, object_pk=v.pk))

    print('Unmapped concepts:')
    for clid, no in unmapped.most_common():
        print(clid, no)

    for fname in data_path('concept_set_meta').iterdir():
        if fname.suffix == '.tsv':
            md = load(fname.parent.joinpath(fname.name + '-metadata.json'))
            provider = models.MetaProvider(
                id=fname.stem,
                name=md['dc:title'],
                description=md['dc:description'],
                url=md['dc:source'],
                jsondata=md)
            for meta in reader(fname, dicts=True):
                try:
                    for k, v in meta.items():
                        if v and k != 'CONCEPTICON_ID':
                            models.ConceptSetMeta(
                                metaprovider=provider,
                                conceptset=data['ConceptSet'][meta['CONCEPTICON_ID']],
                                key=k,
                                value=v)
                except:
                    print(fname)
                    print(meta)
                    raise


def similarity(cl1, cl2):
    cs1 = set(c.parameter_pk for c in cl1.valuesets)
    cs2 = set(c.parameter_pk for c in cl2.valuesets)
    return len(cs1.intersection(cs2)) / len(cs1.union(cs2))


def uniqueness(cl):
    return sum([1 / len(c.parameter.valuesets) for c in cl.valuesets]) / len(cl.valuesets)


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    for concept in DBSession.query(models.ConceptSet):
        concept.representation = len(concept.valuesets)

    ul = []
    for clist in DBSession.query(models.Conceptlist):
        clist.items = len(clist.valuesets)
        ul.append((clist.name, uniqueness(clist)))

    #for i, (n, u) in enumerate(sorted(ul, key=lambda t: t[1], reverse=True)):
    #    if i > 10:
    #        break
    #    print n, u

    similarities = {}
    for cl1, cl2 in combinations(DBSession.query(models.Conceptlist), 2):
        s = similarity(cl1, cl2)
        similarities[(cl1.name, cl2.name)] = s

    #for i, ((l1, l2), s) in enumerate(sorted(similarities.items(), key=lambda i: i[1], reverse=True)):
    #    if i < 20:
    #        print l1, l2, s
    #    if s == 0:
    #        pass


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
