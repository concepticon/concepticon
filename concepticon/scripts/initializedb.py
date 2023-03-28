import re
import collections
import urllib.parse

from clld.cliutil import Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.bibtex import Database
from clldutils.misc import slug
from clldutils.apilib import assert_release
from clldutils.clilib import confirm
from clldutils.markup import iter_markdown_sections, iter_markdown_tables
from pycldf.ext.markdown import CLDFMarkdownLink
from markdown import markdown as _markdown
from tqdm import tqdm
from pycldf import Dataset

import concepticon
from concepticon import models


def markdown(s):
    return _markdown(s, extensions=['markdown.extensions.tables'])


def main(args):  # pragma: no cover
    ds = args.cldf
    norare = Dataset.from_metadata(
        ds.directory.parent.parent / 'norare-cldf' / 'cldf' / 'Wordlist-metadata.json')
    norare_cs = {r['ID']: r for r in norare['ParameterTable'] if r['count_datasets']}
    contributions = {
        header.replace('#', '').strip().lower(): text for _, header, text in
        iter_markdown_sections(ds.directory.joinpath('CONTRIBUTORS.md').read_text(encoding='utf8'))}
    data = Data()

    try:
        version = assert_release(ds.directory.parent)
    except AssertionError:
        if not confirm('This seems to be a test run. Correct? ', default=False):
            raise
        version = 'x'
    doi = input('DOI:')
    try:
        assert re.match(r'10\.5281/zenodo\.[0-9]+', doi or ''), 'Invalid DOI'
    except AssertionError:
        if not confirm('This seems to be a test run. Correct? ', default=False):
            raise

    dataset = common.Dataset(
        id=concepticon.__name__,
        name="CLLD Concepticon {}".format(version),
        publisher_name=ds.properties["dc:publisher"]['http://xmlns.com/foaf/0.1/name'],
        publisher_place=ds.properties["dc:publisher"]['dc:Location'],
        publisher_url=ds.properties["dc:publisher"]['http://xmlns.com/foaf/0.1/homepage'],
        license=ds.properties['dc:license']['url'],
        contact=ds.properties["dc:publisher"]['http://xmlns.com/foaf/0.1/mbox'],
        domain=urllib.parse.urlparse(ds.properties['dcat:accessURL']).netloc,
        jsondata={
            'doi': doi,
            'version': version,
            'funding': markdown(contributions['grant information']),
            'people': markdown(contributions['people']),
            'license_icon': ds.properties['dc:license']['icon'],
            'license_name': ds.properties['dc:license']['name']})

    DBSession.add(dataset)
    editors = next(iter_markdown_tables(contributions['editors']))
    editors = [dict(zip(editors[0], row)) for row in editors[1]]
    for i, editor in enumerate(editors, start=1):
        start, to_, end = editor['Period'].strip().partition('-')
        start, end = start.strip(), end.strip()
        if to_ and (not end):
            name = editor['Name'].strip()
            c = data.add(common.Contributor, slug(name), id=slug(name), name=name)
            dataset.editors.append(common.Editor(contributor=c, ord=i))

    TAGS = {row['ID']: row['Description'] for row in ds['tags.csv']}
    for name, description in TAGS.items():
        data.add(models.Tag, name, id=slug(name), name=name, description=description)

    pdfs = {row['ID']: row for row in ds['MediaTable']}
    for rec in Database.from_file(ds.bibpath, lowercase=True):
        source = data.add(common.Source, rec.id, _obj=bibtex2source(rec, lowercase_id=False))
        if rec.id in pdfs:
            spec = pdfs[rec.id]
            DBSession.flush()
            DBSession.add(common.Source_files(
                mime_type=spec['Media_Type'],
                object_pk=source.pk,
                jsondata=urllib.parse.urlunsplit(spec['Download_URL'])))

    for concept in ds['ParameterTable']:
        data.add(
            models.ConceptSet,
            concept['ID'],
            id=concept['ID'],
            name=concept['Name'],
            description=concept['Description'],
            semanticfield=concept['Semantic_Field'],
            ontological_category=concept['Ontological_Category'],
            norare_datasets=norare_cs[concept['ID']]['count_datasets'] if concept['ID'] in norare_cs else 0,
            norare_variables=norare_cs[concept['ID']]['count_variables'] if concept['ID'] in norare_cs else 0,
        )

    for rel in ds['conceptrelations.csv']:
        DBSession.add(models.Relation(
            source=data['ConceptSet'][rel['Source_ID']],
            target=data['ConceptSet'][rel['Target_ID']],
            description=rel['Relation_ID']))

    for lang in ds['LanguageTable']:
        data.add(
            models.GlossLanguage,
            lang['ID'],
            id=lang['ID'],
            name=lang['Name'],
            latitude=lang['Latitude'],
            longitude=lang['Longitude'],
            count_conceptlists=0,
            count_concepts=0,
        )

    def fname_to_component(ml):
        if ml.is_cldf_link:
            ml.url = "{}#cldf:{}".format(ml.component(cldf=ds), ml.objid)
        return ml

    for cl in ds['ContributionTable']:
        conceptlist = data.add(
            models.Conceptlist,
            cl['ID'],
            id=cl['ID'],
            name=' '.join(cl['ID'].split('-')),
            target_languages=cl['Target_Language'],
            source_languages=' '.join(cl['Gloss_Language_IDs']),
            description=CLDFMarkdownLink.replace(cl['Description'], fname_to_component),
            year=cl['Year'],
            alias=', '.join(cl['Alias']),
        )
        for glid in cl['Gloss_Language_IDs']:
            DBSession.add(models.ConceptlistLanguage(
                conceptlist=conceptlist, language=data['GlossLanguage'][glid]))
            data['GlossLanguage'][glid].count_conceptlists += 1
        for src in cl['Source']:
            common.ContributionReference(
                source=data['Source'][src], contribution=conceptlist)

        for tag in cl['Tags'] or ['specific']:
            DBSession.add(models.ConceptlistTag(
                conceptlist=conceptlist, tag=data['Tag'][tag]))

        for i, name in enumerate(cl['Contributor']):
            cid = slug(name)
            contrib = data['Contributor'].get(cid)
            if not contrib:
                contrib = data.add(common.Contributor, cid, id=cid, name=name)
            DBSession.add(common.ContributionContributor(
                ord=i, contribution=conceptlist, contributor=contrib))

    glosses_by_concept = collections.defaultdict(list)
    for gloss in ds['FormTable']:
        glosses_by_concept[gloss['Concept_ID']].append(gloss)

    number_pattern = re.compile('(?P<number>[0-9]+)(?P<suffix>.*)')
    metalang = models.GlossLanguage(id='meta', name='Meta Language')
    for concept in tqdm(ds['concepts.csv']):
        glosses = glosses_by_concept[concept['ID']]
        match = number_pattern.match(concept['Number'])
        vsid = (concept['Conceptlist_ID'], concept['Concepticon_ID'])
        vs = data['ValueSet'].get(vsid)
        if not vs:
            vs = data.add(
                common.ValueSet,
                vsid,
                id='-'.join(vsid),
                description='',
                language=metalang,
                contribution=data['Conceptlist'][concept['Conceptlist_ID']],
                parameter=data['ConceptSet'][concept['Concepticon_ID']])
        v = models.Concept(
            id=concept['ID'],
            valueset=vs,
            description=concept['Name'],  # our own gloss, if available
            name='; '.join('{} [{}]'.format(gl['Form'], gl['Language_ID']) for gl in glosses),
            number=int(match.group('number')),
            number_suffix=match.group('suffix'),
            jsondata=concept['Attributes'],
        )
        for gloss in glosses:
            DBSession.add(models.Gloss(
                language=data['GlossLanguage'][gloss['Language_ID']],
                concept=v,
                lang_key=gloss['Language_ID'],
                name=gloss['Form'],
                id='{0}-{1}'.format(v.id, gloss['Language_ID'])))
            data['GlossLanguage'][gloss['Language_ID']].count_concepts += 1

    for row in ds['retired.csv']:
        model = {
            'Concept': common.Value,
            'Conceptlist': common.Contribution,
        }[row['Type']]
        common.Config.add_replacement(row['ID'], row['Replacement_ID'], model=model)


def similarity(cl1, cl2):
    cs1 = set(c.parameter_pk for c in cl1.valuesets)
    cs2 = set(c.parameter_pk for c in cl2.valuesets)
    return len(cs1.intersection(cs2)) / len(cs1.union(cs2))


def uniqueness(cl):
    try:
        return sum([1 / len(c.parameter.valuesets) for c in cl.valuesets]) / len(cl.valuesets)
    except ZeroDivisionError:  # pragma: no cover
        return 0


def prime_cache(args):  # pragma: no cover
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
    for concept in DBSession.query(models.ConceptSet):
        concept.representation = len(concept.valuesets)

    for clist in DBSession.query(models.Conceptlist):
        clist.items = sum(len(vs.values) for vs in clist.valuesets)
        clist.uniqueness = uniqueness(clist)

        similar = collections.Counter()
        for other in DBSession.query(models.Conceptlist):
            if other != clist:
                similar[other.id] = similarity(clist, other)

        clist.update_jsondata(most_similar=similar.most_common(n=5))
