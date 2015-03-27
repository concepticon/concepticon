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


def split(s):
    return [ss.strip() for ss in s.split(',') if ss.strip()]


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
    for rec in Database.from_file(
            args.data_file('concepticon-data', 'references', 'references.bib'), lowercase=True):
        source = bibtex2source(rec, cls=models.Ref)
        if rec.id in data['Conceptlist']:
            with_source.add(rec.id)
            langs.extend(split(rec['source_language']))
            source.conceptlist = data['Conceptlist'][rec.id]
            data['Conceptlist'][rec.id].description = source.note
            data['Conceptlist'][rec.id].source_languages = ' '.join(split(rec['source_language']))
            data['Conceptlist'][rec.id].target_languages = rec.get('target_language')

        data.add(models.Ref, rec.id, _obj=source)

    assert with_source == set(list(data['Conceptlist'].keys()))

    for concept in reader(
            args.data_file('concepticon-data', 'concepticon.tsv'), namedtuples=True):
        #OMEGAWIKI	SEEALSO	GLOSS	SEMANTICFIELD	DEFINITION	POS	WOLD
        data.add(
            models.DefinedConcept,
            concept.OMEGAWIKI,
            id='%s' % uuid4(),
            name=concept.GLOSS,
            description=concept.DEFINITION,
            semanticfield=concept.SEMANTICFIELD,
            pos=concept.POS)

    sc = 0
    unmapped = 0
    number_pattern = re.compile('(?P<number>[0-9]+)(?P<suffix>.*)')

    for fname in conceptlists:
        conceptlist = data['Conceptlist'][fname.namebase]
        langs = conceptlist.source_languages.split()
        numbers = []
        for concept in reader(fname, namedtuples=True):
            sc += 1
            number = concept.NUMBER if hasattr(concept, 'NUMBER') else concept.ID
            if number in numbers:
                print '---', concept.OMEGAWIKI, fname.namebase, number, 'multiple!'
                unmapped += 1
                continue

            numbers.append(number)
            if concept.OMEGAWIKI == 'NAN' or concept.OMEGAWIKI not in data['DefinedConcept']:
                print '---', concept.OMEGAWIKI, fname.namebase, number
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
            v = data.add(
                models.Concept, id_,
                id=id_,
                valueset=vs,
                name=gloss,
                description='; '.join('%s [%s]' % (otherlgs[l], l) for l in sorted(otherlgs.keys())),
                number=int(match.group('number')),
                number_suffix=match.group('suffix'))
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
