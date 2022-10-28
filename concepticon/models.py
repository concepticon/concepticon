from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

from clld import interfaces
from clld.db.meta import CustomModelMixin, Base
from clld.db.models.common import Contribution, Parameter, Value, IdNameDescriptionMixin, Unit
from clld.lib.rdf import url_for_qname, NAMESPACES

# Maximum number of language columns to display for a conceptlist:
MAX_LANG_COLS = 4

# -----------------------------------------------------------------------------
# specialized common mapper classes
# -----------------------------------------------------------------------------
@implementer(interfaces.IValue)
class Concept(CustomModelMixin, Value):
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    number = Column(Integer)
    number_suffix = Column(String)

    @property
    def label(self):
        comps = self.name.split('; ')
        res = comps[0]
        if len(comps) > 1:
            res += '…'
        return res

    def __rdf__(self, request):
        yield 'rdf:type', url_for_qname('skos:Concept')
        yield 'skos:topConceptOf', request.resource_url(self.valueset.contribution)

    @property
    def glossdict(self):
        return {gl.lang_key: gl.name for gl in self.glosses}


@implementer(interfaces.IUnit)
class Gloss(CustomModelMixin, Unit):
    pk = Column(Integer, ForeignKey('unit.pk'), primary_key=True)
    lang_key = Column(Unicode)
    concept_pk = Column(Integer, ForeignKey('concept.pk'))
    concept = relationship(Concept, backref=backref('glosses'))


@implementer(interfaces.IParameter)
class ConceptSet(CustomModelMixin, Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    semanticfield = Column(Unicode)
    ontological_category = Column(Unicode)
    representation = Column(Integer)

    def __rdf__(self, request):
        yield 'dcterms:type', self.ontological_category
        yield 'rdf:type', url_for_qname('skos:Collection')
        for vs in self.valuesets:
            yield 'skos:member', request.resource_url(vs.values[0])
        for rel in self.rel_to:
            if rel.description == 'broader':
                yield 'skos:broader', request.resource_url(rel.target)
            elif rel.description == 'narrower':
                yield 'skos:narrower', request.resource_url(rel.target)
            else:
                yield 'skos:related', request.resource_url(rel.target)
        for rel in self.rel_from:
            if rel.description == 'broader':
                yield 'skos:narrower', request.resource_url(rel.source)
            elif rel.description == 'narrower':
                yield 'skos:broader', request.resource_url(rel.source)
            else:
                yield 'skos:related', request.resource_url(rel.source)


class Relation(Base):
    source_pk = Column(Integer, ForeignKey('parameter.pk'))
    target_pk = Column(Integer, ForeignKey('parameter.pk'))
    description = Column(Unicode)

    source = relationship(ConceptSet, foreign_keys=[source_pk], backref='rel_to')
    target = relationship(ConceptSet, foreign_keys=[target_pk], backref='rel_from')


class Tag(Base, IdNameDescriptionMixin):
    pass


@implementer(interfaces.IContribution)
class Conceptlist(CustomModelMixin, Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    source_languages = Column(Unicode)
    target_languages = Column(Unicode)
    items = Column(Integer)
    uniqueness = Column(Float)
    year = Column(Integer)
    alias = Column(Unicode)

    @property
    def source_languages_list(self):
        return [s.lower() for s in self.source_languages.split()]

    @property
    def excess_source_languages(self):
        return len(self.source_languages_list) > MAX_LANG_COLS

    def __rdf__(self, request):
        yield 'rdf:type', url_for_qname('skos:ConceptScheme')
        for vs in self.valuesets:
            yield 'skos:hasTopConcept', request.resource_url(vs.values[0])
        for ref in self.references:
            yield 'dcterms:source', request.resource_url(ref.source)

    @property
    def github_url(self):
        return 'https://github.com/concepticon/concepticon-data/blob/master' \
               '/concepticondata/conceptlists/{0}.tsv'.format(self.id)

    @property
    def tags(self):
        return [ta.tag for ta in self.tag_assocs]


class ConceptlistLanguage(Base):
    conceptlist_pk = Column(Integer, ForeignKey("conceptlist.pk"))
    language_pk = Column(Integer, ForeignKey("language.pk"))
    conceptlist = relationship(Conceptlist, backref="language_assocs")
    language = relationship("Language", backref="conceptlist_assocs")


class ConceptlistTag(Base):
    conceptlist_pk = Column(Integer, ForeignKey('conceptlist.pk'))
    tag_pk = Column(Integer, ForeignKey('tag.pk'))
    conceptlist = relationship(Conceptlist, backref='tag_assocs')
    tag = relationship(Tag, backref='conceptlist_assocs')
