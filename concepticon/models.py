from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from clld import interfaces
from clld.db.meta import CustomModelMixin, Base
from clld.db.models.common import Contribution, Parameter, Value
from clld.lib.rdf import url_for_qname


# -----------------------------------------------------------------------------
# specialized common mapper classes
# -----------------------------------------------------------------------------
@implementer(interfaces.IValue)
class Concept(CustomModelMixin, Value):
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    number = Column(Integer)
    number_suffix = Column(String)

    def __rdf__(self, request):
        yield 'rdf:type', url_for_qname('skos:Concept')
        yield 'skos:topConceptOf', request.resource_url(self.valueset.contribution)


@implementer(interfaces.IParameter)
class ConceptSet(CustomModelMixin, Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    omegawiki = Column(String)
    semanticfield = Column(Unicode)
    ontological_category = Column(Unicode)
    representation = Column(Integer)

    @property
    def omegawiki_url(self):
        if self.omegawiki:
            return 'http://www.omegawiki.org/DefinedMeaning:%s' % self.omegawiki

    def __rdf__(self, request):
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


@implementer(interfaces.IContribution)
class Conceptlist(CustomModelMixin, Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    source_languages = Column(Unicode)
    target_languages = Column(Unicode)
    items = Column(Integer)
    year = Column(Integer)

    def __rdf__(self, request):
        yield 'rdf:type', url_for_qname('skos:ConceptScheme')
        for vs in self.valuesets:
            yield 'skos:hasTopConcept', request.resource_url(vs.values[0])
        for ref in self.references:
            yield 'dcterms:source', request.resource_url(ref.source)
