Concepticon in CLLD
===================

Since the data and mappings provided by the concepticon project are an important
building block to interoperability between lexical resources, they should be
published as clld app (edited by Cysouw and List), thereby providing an API
which can be used by tools and methods.


Data model
----------

The main entities of the data model are

- ConcepticonConcept: An "authoritative" or "hub" concept, which can be used
  to relate other concepts to or directly by referencing it from wordlists.
  A ConcepticonConcept is identified by its unique English gloss. All
  ConcepticonConcepts have a description or example, possibly imported from
  OmegaWiki. (maps to Parameter)
- ConceptList: A list of concepts typically created to collect wordlists;
  e.g. the swadesh list, but maybe also OmegaWiki's DefinedMeanings.
  (maps to Contribution)
- SourceConcept: A concept as it appears in a ConceptList.
  (maps to ValueSet, the relation from ValueSet to Parameter is interpreted as
  the canonical sameAs relation (see below).)
- Relation (better term?): Relates SourceConcepts to ConcepticonConcepts,
  specifying a relation from "sameAs|narrower|broader".
  Each SourceConcept is assumed to be related to exactly one ConcepticonConcept
  via a sameAs relation.


clld app
--------

With this data model, a clld app can provide:

- URLs identifying SourceConcepts and ConcepticonConcepts (as well as ConceptLists).
- an API allowing discovery of related concepts given either a Source- or
  ConcepticonConcept.


Data curation
-------------

Data curation could proceed pretty much as done now, i.e. the data can be
curated as a set of csv files maintained in a GitHub repository. The clld app
can import well-defined releases of this repository. The set of files may
look as follows:

- One csv file listing ConcepticonConcepts:
        ID      Gloss   Description
- One csv file per ConceptList, e.g. swadesh-1955.csv:
        ID      Gloss   ConcepticonConceptID
- One csv file per ConceptList specifying additional relations:
        ID      ConcepticonConceptID    relation

The data repository could be equipped with a small python package providing data
integrity checks which can be run after each push as Travis-CI jobs.

