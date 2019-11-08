import collections

from sqlalchemy import and_
from sqlalchemy.orm import aliased, joinedload

from clld.web.datatables.base import Col, LinkCol, IdCol, DetailsRowLinkCol, IntegerIdCol
from clld.web.datatables.contribution import Contributions, ContributorsCol
from clld.web.datatables.contributor import Contributors, NameCol, ContributionsCol
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.unit import Units
from clld.web.datatables.value import Values
from clld.web.util.helpers import linked_references
from clld.web.util.htmllib import HTML
from clld.db.meta import DBSession
from clld.db.models.common import (
    Value, Value_data, ValueSet, Parameter, Contribution, ContributionContributor,
    ContributionReference, Language, Unit,
)
from clld.db.util import get_distinct_values, icontains

from concepticon.models import ConceptSet, Concept, Conceptlist, ConceptlistTag, Tag, Gloss


class Compilers(Contributors):
    def base_query(self, query):
        return query.join(ContributionContributor)

    def col_defs(self):
        return [
            NameCol(self, 'name'),
            ContributionsCol(self, 'concept_lists'),
        ]


class RefsCol(Col):
    __kw__ = {'bSortable': False, 'bSearchable': False}

    def format(self, item):
        return linked_references(self.dt.req, item)


class SourceLanguagesCol(Col):
    def __init__(self, dt, name, **kw):
        kw['choices'] = [
            r[0][5:].capitalize() for r in DBSession.query(Value_data.key)
            .filter(Value_data.key.startswith('lang_'))
            .order_by(Value_data.key)
            .distinct()]
        kw['bSortable'] = False
        Col.__init__(self, dt, name, **kw)

    def format(self, item):
        return HTML.ul(
            *[HTML.li(l) for l in item.source_languages.split()],
            **{'class': 'unstyled'})

    def search(self, qs):
        return icontains(Conceptlist.source_languages, qs)


class TagsCol(Col):
    __kw__ = {'bSortable': False}

    def format(self, item):
        return HTML.ul(
            *[HTML.li(
                HTML.span(t.name, **{
                    'data-hint': t.description,
                    'class': 'hint--bottom label label-success'})) for t in item.tags],
            **{'class': 'unstyled'})

    def search(self, qs):
        return Tag.id == qs


class Conceptlists(Contributions):
    def base_query(self, query):
        query = query.join(Conceptlist.tag_assocs, ConceptlistTag.tag).distinct()
        return query.options(
            joinedload(Conceptlist.tag_assocs).joinedload(ConceptlistTag.tag),
            joinedload(
                Contribution.contributor_assocs).joinedload(ContributionContributor.contribution),
            joinedload(
                Contribution.references).joinedload(ContributionReference.source))

    def col_defs(self):
        return [
            DetailsRowLinkCol(self, 'd', sTitle='Note'),
            LinkCol(self, 'name'),
            ContributorsCol(self, 'compiler'),
            Col(self, 'alias', model_col=Conceptlist.alias, input_size='mini'),
            Col(self, 'items', model_col=Conceptlist.items, input_size='mini'),
            TagsCol(self, 'tags', choices=[(t.id, t.name) for t in DBSession.query(Tag)]),
            Col(self,
                'uniqueness',
                model_col=Conceptlist.uniqueness,
                sDescription="Uniqueness of the concept inventory within a concept list: "
                "How often do the concepts in the list occur in other lists?",
                input_size='mini'),
            Col(self, 'year', model_col=Conceptlist.year, input_size='mini'),
            SourceLanguagesCol(self, 'source_languages'),
            Col(self, 'target_languages', model_col=Conceptlist.target_languages),
            RefsCol(self, 'sources'),
        ]


class ConceptSets(Parameters):
    def col_defs(self):
        return [
            IntegerIdCol(self, 'id', sTitle='ID'),
            LinkCol(self, 'name'),
            Col(self, 'description', sTitle='Definition'),
            Col(self,
                'semantic_field',
                choices=get_distinct_values(ConceptSet.semanticfield),
                model_col=ConceptSet.semanticfield),
            Col(self,
                'ontological_category',
                choices=get_distinct_values(ConceptSet.ontological_category),
                model_col=ConceptSet.ontological_category),
            Col(self,
                'representation',
                sDescription='number of concept lists this concept appears in',
                model_col=ConceptSet.representation),
        ]


class ConceptIdCol(IdCol):
    def order(self):
        if self.dt.contribution:
            return Concept.number, Concept.number_suffix
        return Concept.id


class ConceptInSourceCol(Col):
    def __init__(self, dt, name, alias, **kw):
        self.alias = alias
        kw['sTitle'] = name.capitalize()
        Col.__init__(self, dt, name, **kw)

    def format(self, item):
        return item.glossdict.get(self.name, '')

    def order(self):
        return self.alias.name

    def search(self, qs):
        return icontains(self.alias.name, qs)


class Concepts(Values):
    def __init__(self, req, *args, **kw):
        Values.__init__(self, req, *args, **kw)
        self._langs = collections.OrderedDict()
        if self.contribution:
            for lang in self.contribution.source_languages.split():
                lang = lang.lower()
                self._langs[lang] = aliased(Gloss, name=lang)

    def base_query(self, query):
        query = Values.base_query(self, query)
        if self.contribution:
            query = query.join(ValueSet.parameter)
            for lang, alias in self._langs.items():
                query = query.outerjoin(
                    alias,
                    and_(alias.lang_key == lang, alias.concept_pk == Value.pk))
            query = query.options(
                joinedload(Value.data),
                joinedload(Value.valueset).joinedload(ValueSet.parameter))
        elif self.parameter:
            pass
        else:
            query = query.join(ValueSet.parameter)
            query = query.options(joinedload(
                Value.valueset).joinedload(ValueSet.parameter))
        return query

    def col_defs(self):
        res = [
            ConceptIdCol(self, 'id', sClass='left'),
        ]
        if self.parameter:
            res.extend([
                Col(self, 'name', sTitle='Concept in source'),
                LinkCol(self, 'conceptlist', get_object=lambda v: v.valueset.contribution),
            ])
        elif self.contribution:
            for lang, alias in self._langs.items():
                res.append(ConceptInSourceCol(self, lang, alias=alias))
            res.append(LinkCol(
                self,
                'concept_set',
                model_col=Parameter.name,
                get_object=lambda v: v.valueset.parameter))
        else:
            res.extend([
                Col(self, 'name', sTitle='Description in source'),
                LinkCol(
                    self,
                    'concept_set',
                    model_col=Parameter.name,
                    get_object=lambda v: v.valueset.parameter),
            ])
        return res


class Glosses(Units):
    def base_query(self, query):
        query = query.join(Language).join(Gloss.concept).options(
            joinedload(Unit.language),
            joinedload(Gloss.concept),
        )
        query = query \
            .join(Value.valueset) \
            .join(ValueSet.parameter) \
            .join(ValueSet.contribution) \
            .options(
            joinedload(Gloss.concept, Value.valueset, ValueSet.parameter),
            joinedload(Gloss.concept, Value.valueset, ValueSet.contribution))

        if self.language:
            query = query\
                .join(Value.valueset)\
                .join(ValueSet.parameter)\
                .join(ValueSet.contribution)\
                .options(
                    joinedload(Gloss.concept, Value.valueset, ValueSet.parameter),
                    joinedload(Gloss.concept, Value.valueset, ValueSet.contribution))
            return query.filter(Unit.language == self.language)
        return query

    def col_defs(self):
        res = [
            Col(self, 'name', sTitle='Gloss'),
            LinkCol(
                self,
                'concept_set',
                model_col=Parameter.name,
                get_object=lambda i: i.concept.valueset.parameter),
            LinkCol(
                self,
                'concept_list',
                model_col=Contribution.name,
                get_object=lambda i: i.concept.valueset.contribution),
        ]
        if self.language:
            return res
        return [
            LinkCol(
                self,
                'language',
                model_col=Language.name,
                choices=get_distinct_values(Language.name),
                get_object=lambda i: i.language),
        ] + res


def includeme(config):
    config.register_datatable('parameters', ConceptSets)
    config.register_datatable('values', Concepts)
    config.register_datatable('units', Glosses)
    config.register_datatable('contributions', Conceptlists)
    config.register_datatable('contributors', Compilers)
