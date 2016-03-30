from __future__ import unicode_literals

from sqlalchemy import and_
from sqlalchemy.orm import aliased, joinedload, joinedload_all

from clld.web.datatables.base import Col, LinkCol, IdCol, DetailsRowLinkCol, IntegerIdCol
from clld.web.datatables.contribution import Contributions, ContributorsCol
from clld.web.datatables.contributor import Contributors, NameCol, ContributionsCol
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.value import Values
from clld.web.util.helpers import linked_references
from clld.web.util.htmllib import HTML
from clld.db.meta import DBSession
from clld.db.models.common import (
    Value, Value_data, ValueSet, Parameter, ContributionContributor)
from clld.db.util import get_distinct_values, icontains

from concepticon.models import ConceptSet, Concept, Conceptlist


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


class Conceptlists(Contributions):
    def col_defs(self):
        return [
            DetailsRowLinkCol(self, 'd', sTitle='Note'),
            LinkCol(self, 'name'),
            ContributorsCol(self, 'compiler'),
            Col(self, 'items', model_col=Conceptlist.items),
            Col(self, 'uniqueness', model_col=Conceptlist.uniqueness),
            Col(self, 'year', model_col=Conceptlist.year),
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
        return item.datadict()['lang_' + self.name]

    def order(self):
        return self.alias.value

    def search(self, qs):
        return icontains(self.alias.value, qs)


class Concepts(Values):
    def __init__(self, req, *args, **kw):
        Values.__init__(self, req, *args, **kw)
        self._langs = {}
        if self.contribution:
            for lang in self.contribution.source_languages.split():
                lang = lang.lower()
                self._langs[lang] = aliased(Value_data, name=lang)

    def base_query(self, query):
        query = Values.base_query(self, query)
        if self.contribution:
            query = query.join(ValueSet.parameter)
            for lang, alias in self._langs.items():
                query = query.outerjoin(
                    alias,
                    and_(alias.key == 'lang_' + lang, alias.object_pk == Concept.pk))
            query = query.options(
                joinedload(Value.data),
                joinedload_all(Value.valueset, ValueSet.parameter))
        elif self.parameter:
            pass
        else:
            query = query.join(ValueSet.parameter)
            query = query.options(joinedload_all(Value.valueset, ValueSet.parameter))
        return query

    def col_defs(self):
        res = [
            ConceptIdCol(self, 'id', sClass='left'),
        ]
        if self.parameter:
            res.extend([
                Col(self, 'name', sTitle='Concept in source'),
                Col(self, 'description', sTitle='English gloss'),
                LinkCol(self, 'conceptlist', get_object=lambda v: v.valueset.contribution),
            ])
        elif self.contribution:
            #
            # TODO: join Value_data for each source language!
            #
            for lang, alias in self._langs.items():
                res.append(ConceptInSourceCol(self, lang, alias=alias))
            res.append(Col(self, 'description', sTitle='English gloss'))
            res.append(LinkCol(
                self,
                'concept_set',
                model_col=Parameter.name,
                get_object=lambda v: v.valueset.parameter))
        else:
            res.extend([
                Col(self, 'name', sTitle='Description in source'),
                Col(self, 'description', sTitle='English gloss'),
                LinkCol(
                    self,
                    'concept_set',
                    model_col=Parameter.name,
                    get_object=lambda v: v.valueset.parameter),
            ])
        return res


def includeme(config):
    config.register_datatable('parameters', ConceptSets)
    config.register_datatable('values', Concepts)
    config.register_datatable('contributions', Conceptlists)
    config.register_datatable('contributors', Compilers)
