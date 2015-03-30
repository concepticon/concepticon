from __future__ import unicode_literals
import sys
import re
from uuid import uuid4

from clld.scripts.util import initializedb, Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.bibtex import Database
from clld.lib.dsv import reader
from clld.util import slug

import concepticon
from concepticon import models


def split(s, sep=','):
    return [ss.strip() for ss in s.split(sep) if ss.strip()]


def main(args):
    data = Data()
    data_path = lambda *cs: args.data_file('concepticon-data', 'concepticondata', *cs)

    dataset = common.Dataset(
        id=concepticon.__name__,
        name="Concepticon",
        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="http://www.eva.mpg.de",
        license="http://creativecommons.org/licenses/by/4.0/",
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
    for fname in data_path('sources').files():
        files[fname.namebase] = \
            "https://github.com/clld/concepticon-data/blob/master/sources/%s" % fname.name

    conceptlists = []
    for fname in data_path('conceptlists').files():
        if fname.namebase.startswith('.'):
            continue
        conceptlists.append(fname)
        data.add(
            models.Conceptlist, fname.namebase,
            id=fname.namebase,
            name=' '.join(fname.namebase.split('-')))

    langs = []
    with_source = set()
    refdb = Database.from_file(data_path('references', 'references.bib'), lowercase=True)
    for rec in refdb:
        if rec.id not in data['Conceptlist']:
            source = data.add(common.Source, rec.id, _obj=bibtex2source(rec))
            if rec.id in files:
                DBSession.flush()
                DBSession.add(common.Source_files(
                    mime_type='application/pdf',
                    object_pk=source.pk,
                    jsondata=dict(url=files[rec.id])))

    for rec in refdb:
        if rec.id in data['Conceptlist']:
            conceptlist = data['Conceptlist'][rec.id]
            with_source.add(rec.id)

            for k, v in rec.items():
                if v.startswith('{') and v.endswith('}'):
                    v = v[1:-1].strip()
                if k in ['source_languages', 'target_languages', 'owner', 'timestamp']:
                    continue
                if k == 'source_language':
                    langs.extend(split(v))
                    conceptlist.source_languages = ' '.join(split(v))
                elif k == 'entryset':
                    for id_ in split(v):
                        common.ContributionReference(
                            source=data['Source'][id_], contribution=conceptlist)
                elif k == 'author':
                    for i, name in enumerate(split(rec['author'], sep=' and ')):
                        contrib = data['Contributor'].get(name)
                        if not contrib:
                            contrib = data.add(common.Contributor, name, id=slug(name), name=name)
                        DBSession.add(common.ContributionContributor(
                            ord=i, contribution=conceptlist, contributor=contrib))
                elif k == 'year':
                    conceptlist.year = int(v)
                elif k == 'note':
                    conceptlist.description = v
                elif k == 'target_language':
                    conceptlist.target_languages = v
                else:
                    DBSession.flush()
                    DBSession.add(common.Contribution_data(
                        object_pk=conceptlist.pk, key=k, value=v))

    assert with_source == set(list(data['Conceptlist'].keys()))

    for concept in reader(data_path('concepticon.tsv'), namedtuples=True):
        #Noun -> Thing
        #Verb    -> Action/Process
        #Adjective -> Property
        #Function Word -> Other
        data.add(
            models.DefinedMeaning,
            concept.ID,
            id=concept.ID,
            omegawiki=concept.OMEGAWIKI,
            name=concept.GLOSS,
            description=concept.DEFINITION,
            semanticfield=concept.SEMANTICFIELD,
            taxonomy=concept.POS)

    unmapped = 0
    number_pattern = re.compile('(?P<number>[0-9]+)(?P<suffix>.*)')

    for fname in conceptlists:
        conceptlist = data['Conceptlist'][fname.namebase]
        langs = [l.lower() for l in conceptlist.source_languages.split()]
        for concept in reader(fname, namedtuples=True):
            if not concept.ID or not concept.CONCEPTICON_ID or concept.CONCEPTICON_ID == 'NAN':
                unmapped += 1
                continue

            otherlgs = {}
            for lang in langs:
                if lang != 'english':
                    if getattr(concept, lang.upper(), None):
                        otherlgs[lang] = getattr(concept, lang.upper())

            match = number_pattern.match(concept.NUMBER)
            gloss = concept.GLOSS
            vs = common.ValueSet(
                id=concept.ID,
                description=gloss,
                language=english,
                contribution=conceptlist,
                parameter=data['DefinedMeaning'][concept.CONCEPTICON_ID])
            d = {}
            for key, value in concept.__dict__.items():
                if key not in ['NUMBER', 'ID', 'OMEGAWIKI', 'GLOSS'] + [l.upper() for l in langs]:
                    d[key.lower()] = value
            v = models.Concept(
                id=concept.ID,
                valueset=vs,
                name=gloss,
                description='; '.join('%s [%s]' % (otherlgs[l], l) for l in sorted(otherlgs.keys())),
                number=int(match.group('number')),
                number_suffix=match.group('suffix'),
                jsondata=d)
            DBSession.flush()
            for key, value in otherlgs.items():
                DBSession.add(common.Value_data(key=key, value=value, object_pk=v.pk))

    print '%s concepts unmapped' % unmapped


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    for concept in DBSession.query(models.DefinedMeaning):
        concept.representation = len(concept.valuesets)

    for clist in DBSession.query(models.Conceptlist):
        clist.items = len(clist.valuesets)


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
