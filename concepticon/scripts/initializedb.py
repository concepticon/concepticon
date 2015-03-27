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
    for i, name in enumerate(['Johann-Mattis List', 'Michael Cysouw']):
        c = common.Contributor(id=slug(name), name=name)
        dataset.editors.append(common.Editor(contributor=c, ord=i))

    english = data.add(
        common.Language, 'eng',
        id='eng',
        name='English')

    files = {}
    for fname in args.data_file('concepticon-data', 'sources').files():
        files[fname.namebase] = \
            "https://github.com/clld/concepticon-data/blob/master/sources/%s" % fname.name

    conceptlists = []
    for fname in args.data_file('concepticon-data', 'conceptlists').files():
        if fname.namebase.startswith('.'):
            continue
        conceptlists.append(fname)
        data.add(
            models.Conceptlist, fname.namebase,
            id=fname.namebase,
            name=' '.join(fname.namebase.split('-')))

    langs = []
    with_source = set()
    refdb = Database.from_file(
        args.data_file('concepticon-data', 'references', 'references.bib'),
        lowercase=True)
    for rec in refdb:
        if rec.id not in data['Conceptlist']:
            source = data.add(common.Source, rec.id, _obj=bibtex2source(rec))
            if rec.id in files:
                print 'a file!!', rec.id
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

    for concept in reader(
            args.data_file('concepticon-data', 'concepticon.tsv'), namedtuples=True):
        #OMEGAWIKI	SEEALSO	GLOSS	SEMANTICFIELD	DEFINITION	POS	WOLD
        data.add(
            models.DefinedConcept,
            concept.OMEGAWIKI,
            id='%s' % uuid4(),
            omegawiki=concept.OMEGAWIKI,
            name=concept.GLOSS,
            description=concept.DEFINITION,
            semanticfield=concept.SEMANTICFIELD,
            pos=concept.POS)

    sc = 0
    unmapped = 0
    number_pattern = re.compile('(?P<number>[0-9]+)(?P<suffix>.*)')

    for fname in conceptlists:
        conceptlist = data['Conceptlist'][fname.namebase]
        langs = [l.lower() for l in conceptlist.source_languages.split()]
        numbers = []
        for concept in reader(fname, namedtuples=True):
            sc += 1
            number = concept.NUMBER if hasattr(concept, 'NUMBER') else concept.ID
            if number in numbers:
                #print '---', concept.OMEGAWIKI, fname.namebase, number, 'multiple!'
                unmapped += 1
                continue

            numbers.append(number)
            if concept.OMEGAWIKI == 'NAN' or concept.OMEGAWIKI not in data['DefinedConcept']:
                #print '---', concept.OMEGAWIKI, fname.namebase, number
                unmapped += 1
                continue

            id_ = '%s--%s' % (fname.namebase, number)
            otherlgs = {}
            for lang in langs:
                if lang != 'english':
                    if getattr(concept, lang.upper(), None):
                        otherlgs[lang] = getattr(concept, lang.upper())
            match = number_pattern.match(number)
            gloss = concept.GLOSS if hasattr(concept, 'GLOSS') else concept.ENGLISH
            vs = data.add(
                common.ValueSet, id_,
                id=id_,
                description=gloss,
                language=english,
                contribution=conceptlist,
                parameter=data['DefinedConcept'][concept.OMEGAWIKI])
            d = {}
            for key, value in concept.__dict__.items():
                if key not in ['NUMBER', 'ID', 'OMEGAWIKI', 'GLOSS'] + [l.upper() for l in langs]:
                    d[key.lower()] = value
            v = data.add(
                models.Concept, id_,
                id=id_,
                valueset=vs,
                name=gloss,
                description='; '.join('%s [%s]' % (otherlgs[l], l) for l in sorted(otherlgs.keys())),
                number=int(match.group('number')),
                number_suffix=match.group('suffix'),
                jsondata=d)
            DBSession.flush()
            for key, value in otherlgs.items():
                DBSession.add(common.Value_data(key=key, value=value, object_pk=v.pk))

    print '%s of %s source concepts unmapped' % (unmapped, sc)


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    for concept in DBSession.query(models.DefinedConcept):
        concept.representation = len(concept.valuesets)

    for clist in DBSession.query(models.Conceptlist):
        clist.items = len(clist.valuesets)


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
