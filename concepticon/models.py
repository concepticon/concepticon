from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import Source, Contribution, Parameter, Value, HasSourceMixin


# -----------------------------------------------------------------------------
# specialized common mapper classes
# -----------------------------------------------------------------------------
@implementer(interfaces.IValue)
class Concept(CustomModelMixin, Value):
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    number = Column(Integer)
    number_suffix = Column(String)


@implementer(interfaces.IParameter)
class DefinedConcept(CustomModelMixin, Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    omegawiki = Column(String)
    semanticfield = Column(Unicode)
    pos = Column(Unicode)
    representation = Column(Integer)

    @property
    def omegawiki_url(self):
        if self.omegawiki:
            return 'http://www.omegawiki.org/DefinedMeaning:%s' % self.omegawiki


@implementer(interfaces.IContribution)
class Conceptlist(CustomModelMixin, Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    source_languages = Column(Unicode)
    target_languages = Column(Unicode)
    items = Column(Integer)
    year = Column(Integer)
