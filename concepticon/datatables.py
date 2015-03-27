from clld.web.datatables.base import Col, LinkCol, IdCol, DetailsRowLinkCol
from clld.web.datatables.contribution import Contributions, ContributorsCol
from clld.web.datatables.parameter import Parameters
from clld.web.datatables.value import Values
from clld.web.util.helpers import linked_references

from concepticon.models import DefinedConcept, Concept, Conceptlist


class RefsCol(Col):
    __kw__ = {'bSortable': False, 'bSearchable': False}

    def format(self, item):
        return linked_references(self.dt.req, item)


class Conceptlists(Contributions):
    def col_defs(self):
        return [
            DetailsRowLinkCol(self, 'd', sTitle='Note'),
            LinkCol(self, 'name'),
            ContributorsCol(self, 'compiler'),
            Col(self, 'items', model_col=Conceptlist.items),
            Col(self, 'year', model_col=Conceptlist.year),
            Col(self, 'source_languages', model_col=Conceptlist.source_languages),
            Col(self, 'target_languages', model_col=Conceptlist.target_languages),
            RefsCol(self, 'sources'),
        ]


class DefinedConcepts(Parameters):
    def col_defs(self):
        return [
            IdCol(self, 'id', sClass='left'),
            LinkCol(self, 'name'),
            Col(self, 'description', sTitle='Definition'),
            Col(self, 'semantic_field', model_col=DefinedConcept.semanticfield),
            Col(self, 'part_of_speech', model_col=DefinedConcept.pos),
            Col(self,
                'representation',
                sDescription='number of concept lists this concept appears in',
                model_col=DefinedConcept.representation),
        ]


class ConceptIdCol(IdCol):
    def order(self):
        if self.dt.contribution:
            return Concept.number, Concept.number_suffix
        return Concept.id


class Concepts(Values):
    def col_defs(self):
        res = [
            ConceptIdCol(self, 'id', sClass='left'),
            LinkCol(self, 'name', sTitle='Gloss'),
            Col(self, 'description', sTitle='Source languages')
        ]
        if self.parameter:
            res.append(LinkCol(self, 'conceptlist', get_object=lambda v: v.valueset.contribution))
        if self.contribution:
            res.append(LinkCol(self, 'defined_concept', get_object=lambda v: v.valueset.parameter))
        return res


def includeme(config):
    config.register_datatable('parameters', DefinedConcepts)
    config.register_datatable('values', Concepts)
    config.register_datatable('contributions', Conceptlists)
