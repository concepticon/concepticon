from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    ForeignKey,
)

from clld import interfaces
from clld.db.meta import CustomModelMixin
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
        yield 'skos:topConceptOf', request.resource_url(self.contribution)


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
