<%inherit file="../home_comp.mako"/>
<%namespace name="util" file="../util.mako"/>

<%def name="sidebar()">
    <%util:well title="Cite">
        ${h.newline2br(h.text_citation(request, ctx))|n}
        ${h.cite_button(request, ctx)}
    </%util:well>
</%def>

<h2>Welcome to the Concepticon</h2>

<p class="lead">
    This project is an attempt to link the very many different conceptlists (aka
'Swadesh lists') that are used in the linguistic literature. In practice, we
link all entries from the various concept lists to an OmegaWiki ID as an
intermediate way to reference the concepts.  For a technical discussion of the
background of this enterprise, see
    ${h.external_link('http://bibliography.lingpy.org?key=Poornima2010', label='Poornima & Good (2010)')}. However, instead of
using the detailed RDF-structure proposed there, we decided to use a few simple
tables to actually collect the relevant information. Anybody who is interested
in turning this information into RDF is invited to clone our
    ${h.external_link('https://github.com/clld/concepticon-data', label='GitHub Repository')}.
</p>
<h3>Concept Lists</h3>
<p>A <em>concept list</em> is a selection of meanings that is deemed interesting by some
scholars to compare lexemes between languages. There are very many different
reasons why a particular meaning might be included into such a list, and we do
not have any preference here for a particular set. The only goal we have here
is to link meanings that are found in more than one list, with the goal to be
able to compare various datasets, collected on the basis of different
conceptlists.</p>
<p>In practice, we take any conceptlist, and reduce it to the main information as
found in a particular source. Typically, a conceptlist will have <em>glosses</em> in
one or a few widespread languages, either major scientific languages (like
English, Russian, or Spanish) or major languages from the region in which the
data is collected (i.e. Hausa for the Chadic list from ${h.link(request, Kraft1981)}).  Furthermore, most
conceptlists have some kind of <em>numerical identification (ID)</em>, sometimes
simply an ordering number, which we will also include. Any other information
that we consider important will also be extracted from the sources (e.g.
<em>semantic field</em> from the World Loanword Database, WOLD). These files are
available in the directory <em>/conceptlists/</em>. We also make PDFs with the
original lists available in the directory <em>/sources/</em>.</p>
<h3>Defined Meanings</h3>
<p>Most importantly, to every entry in every conceptlist we add a numeric ID
referring to a <em>defined meaning</em> in <a href="http://omegawiki.org">OmegaWiki</a>.
Depending how you look at it, it is either very hard to define meanings, or
very easy. It is very easy, because just anybody can stand up and propose
whatever definition s/he wants to define in whatever way deemed interesting. It
is very hard to actually come up with definitions that are useful for
widespread application across many different languages. Basically, OmegaWiki
takes the easy route, and just anybody can include there whatever meaning is
deemed important (wiki-style open editing allowed!). We don't necessarily think
that the definitions at OmegaWiki are ideal, but they are a practical start.</p>
<p>We decided to not necessarily link all entries in all conceptlists, as some
entries are not amenable for interoperability between conceptlists. For
example, Huber (1992) includes meanings <em>my hand</em>, <em>your hand</em>, etc. which we
have currently simply not linked at all. If deemed necessary, it would be
trivial to add links later on.</p>
<p>OmegaWiki IDs for defined meanings can be easily accessed online by using the
URL
<a href="/home/mattis/projects/scripts/concepticon/concepticon.github.io/index.md">http://www.omegawiki.org/DefinedMeaning:</a>
plus numeric ID, e.g. for the meaning <em>air</em> with ID 106, check
<a href="http://www.omegawiki.org/DefinedMeaning:106">http://www.omegawiki.org/DefinedMeaning:106</a>.</p>
<h3>Concepticon</h3>
<p>So, to every entry in every conceptlist we try to add a suitable link to a
defined meaning in OmegaWiki. If no suitable defined meaning exists, we simply
add a new one to OmegaWiki. In an attempt to make the different conceptlists
interoperable, we also keep track of all Defined Meanings from OmegaWiki that
we have found at least once in a conceptlist. This combined list of all
currently used meanings is available in the file <a href="https://github.com/concepticon/lists/blob/master/concepticon.tsv">concepticon.tsv</a>. You can
browse the concepticon <a href="browse.html">here</a>.</p>
<p>The concepticon basically lists all numbers referring to OmegaWiki <em>defined
meanings</em>. We also added some extra numbers to very similar meanings (<em>see
also</em>), where it is sometimes unclear to us, what the difference between them
is supposed to be (no criticism: OmegaWiki is a wiki after all!). We also add a
rough <em>gloss</em> to each entry, but this is not supposed to be taken as the
definition, just as a convenience abbreviation. More importantly, the
concepticon includes the <strong>English definitions</strong> from OmegaWiki, which should
give a closer definition of the actual intended meaning.</p>
<p>For convenience, it also includes <em>semantic fields</em> from the <a href="http://wold.clld.org">World Loanword
Database</a> (extended by us for new meanings that are not
included there) and <em>parts-of-speech</em> indications. The parts-of-speech
indications are not supposed to be cross-linguistically comparable (they are
not!), but only a help to better identify the meaning, and as a way to order
the different meanings.</p>
<h3>Future Development</h3>
<p>Every new conceptlist to be added will preferably be linked to the concepts
already in the concepticon. When new defined meanings are necessary, these will
be added to the concepticon.</p>