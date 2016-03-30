<%inherit file="../home_comp.mako"/>
<%namespace name="util" file="../util.mako"/>

<%def name="sidebar()">
    <%util:well title="Cite">
        ${h.newline2br(h.text_citation(request, ctx))|n}
        <p>
        <a href="http://dx.doi.org/10.5281/zenodo.17199">
            <img src="https://zenodo.org/badge/5142/clld/concepticon-data.svg">
        </a>
        </p>
        ${h.cite_button(request, ctx)}
    </%util:well>
    <%util:well title="Version">
        <a href="${req.resource_url(req.dataset)}" style="font-family: monospace">concepticon.clld.org</a>
        serves the latest
        ${h.external_link('https://github.com/clld/concepticon-data/releases', label='released version')}
        of data curated at
        ${h.external_link('https://github.com/clld/concepticon-data', label='clld/concepticon-data')} -
        currently the
        ${h.external_link('https://github.com/clld/concepticon-data/releases/tag/v1.0', label='v1.0')}
    </%util:well>
</%def>

<h2>Welcome to the Concepticon</h2>

<p class="lead">
    This project is an attempt to link the very many different
    <a href="${request.route_url('contributions')}">concept lists</a>
    (aka 'Swadesh lists') that are used in the linguistic literature. In practice, we
link all entries from the various concept lists to a
    <a href="${request.route_url('parameters')}">concept set</a>
    as an intermediate way to reference the concepts.  For a technical discussion of the
background of this enterprise, see
    ${h.external_link('http://bibliography.lingpy.org?key=Poornima2010', label='Poornima & Good (2010)')}.
    ##However, instead of using the detailed RDF-structure proposed there, we decided to use
    ##a few simple tables to actually collect the relevant information. Anybody who is interested
    ##in turning this information into RDF is invited to clone our
    ##${h.external_link('https://github.com/clld/concepticon-data', label='GitHub Repository')}.
</p>
<h3>Concept Lists</h3>
## skos:ConceptScheme
<p>A <em>concept list</em> is a selection of meanings that is deemed interesting by some
scholars to compare lexemes between languages. There are very many different
reasons why a particular meaning might be included into such a list, and we do
not have any preference here for a particular set. The only goal we have here
is to link meanings that are found in more than one list, with the goal to be
able to compare various datasets, collected on the basis of different
concept lists.</p>
<p>In practice, we take any concept list, and reduce it to the main information as
found in a particular source. Typically, a concept list will have <em>glosses</em> in
one or a few widespread languages, either major scientific languages (like
English, Russian, or Spanish) or major languages from the region in which the
data is collected (i.e. Hausa for the Chadic list from ${h.link(request, Kraft1981)}).  Furthermore, most
concept lists have some kind of <em>numerical identification (ID)</em>, sometimes
simply an ordering number, which we will also include. Any other information
that we consider important will also be extracted from the sources (e.g.
<em>semantic field</em> from the
    ${h.external_link('http://wold.clld.org', label='World Loanword Database, WOLD')}).
</p>

<h3>Concept Sets</h3>
## skos:Collection
<p>Most importantly, every concept in every concept list is linked
to a <a href="${request.route_url('parameters')}"><em>concept set</em></a>, i.e.
    a set of concepts sharing the same definition.
Depending how you look at it, it is either very hard to define meanings, or
very easy. It is very easy, because just anybody can stand up and propose
whatever definition s/he wants to define in whatever way deemed interesting. It
is very hard to actually come up with definitions that are useful for
widespread application across many different languages.</p>

<h3>Concepticon</h3>
<p>If no suitably defined concept set exists, we simply
add a new one. The combined list of all
<a href="${request.route_url('parameters')}">concept sets</a> is the concepticon.</p>
<p>We also add a
rough <em>gloss</em> to each concept set, but this is not supposed to be taken as the
definition, just as a convenience abbreviation.
An attempt to give a more precise definition of each concept set is made, currently by
    taking Definitions from (and links to)
   ${h.external_link('http://www.omegawiki.org/', label='OmegaWiki')}.
</p>
<p>For convenience, it also includes <em>semantic fields</em> from the World Loanword Database
    (extended by us for new meanings that are not
included there) and <em>ontological categories</em>. The ontological categories
are not supposed to be cross-linguistically comparable (they are
not!), but only a help to better identify the meaning, and as a way to order
the different meanings.</p>

<h3>Future Development</h3>
<p>Every new concept list to be added will preferably be linked to the concept sets
already in the concepticon. When new concept sets are necessary, these will
be added to the concepticon.</p>

    <h3>Acknowledgements</h3>
    <p>
        Concepticon is a community effort.
    </p>
    <ul>
        <li>Harald Hammarström submitted several new list suggestions in scanned form.</li>
        <li>Robert Blust sent his list from the 1980s.</li>
        <li>Our student assistants in Marburg times did a lot of the initial mapping,
            and also typing, three were involved, Frederike Urke, Sebastian Nicolai, and
            Viola Kirchhoff da Cruz.</li>
        <li>Thiago Chacon provided a typed off version of the list by Payne-1991-202.</li>
        <li>Alexei Kassian provided his annotated Swadesh list in digital form.</li>
        <li>Sean Lee provided his Japonic list and his Ainu list.</li>
        <li>Andrew Kitchen provided his Semitic list.</li>
        <li>Damian Satterthwaite-Phillips provided his Sino-Tibetan list.</li>
        <li>Lars Borin provided his mapping to Wordnet.</li>
        <li>Martin Haspelmath provided his earlier mappings, which we have still not really
            looked into, but especially also helped us with initial questions of how to
            handle the structure.</li>
        <li>Julia Fischer, student assistant in Düsseldorf times, typed off some of the
            first lists in my collection and added translations for French data, like Meillet,
            for example.</li>
        <li>Paul Heggarty send me one of his lists.</li>
    </ul>
