<%inherit file="home_comp.mako"/>
<%namespace name="util" file="util.mako"/>

<h2>About the Concepticon</h2>


<h3>Concept List and Concept Sets</h3>
## skos:ConceptScheme
<p>
    A <em>concept list</em> is a selection of meanings that is deemed
    interesting by some scholars to compare lexemes between languages. There
    are very many different reasons why a particular meaning might be included
    into such a list, and we do not have any preference here for a particular
    set. The only goal we have here is to link meanings that are found in more
    than one list, with the goal to be able to compare various datasets,
    collected on the basis of different concept lists.
    In practice, we take any concept list, and reduce it to the main
    information as found in a particular source. Typically, a concept list will
    have <em>concept labels</em> in one or a few widespread languages, either major
    scientific languages (like English, Russian, or Spanish) or major languages
    from the region in which the data is collected (i.e. Hausa for the Chadic
    list from <a href="${request.route_url('contributions')}/Kraft-1981-434">Kraft (1981)</a>).  
    Furthermore, most concept lists
    have some kind of <em>numerical identification (ID)</em>, sometimes simply
    an ordering number, which we will also include. Any other information that
    we consider important will also be extracted from the sources (e.g.
    <em>semantic field</em> from the 
    ${h.external_link('http://wold.clld.org', label='World Loanword Database, WOLD')}).
</p>
## skos:Collection
<p>
    Most importantly, every concept in every concept list is linked
    to a <a href="${request.route_url('parameters')}">concept set</a>, i.e.
    a set of concepts sharing the same definition.
    Depending how one looks at it, it is either very hard to define meanings, or
    very easy. It is very easy, because just anybody can stand up and propose
    whatever definition s/he wants to define in whatever way deemed interesting. It
    is very hard to actually come up with definitions that are useful for
    widespread application across many different languages.
    In our Concepticon, we link concept sets by assigning simple relations like
    "broader" and "narrower". Yet even these simple relations can get very
    complex, as you can see from the network that shows the major kinship
    relations which are linked to the concept set "SIBLING" at the 
    <a href="../">start page</a>.
    If no suitably defined concept set exists, we simply
    add a new one. The combined list of all
    <a href="${request.route_url('parameters')}">concept sets</a> is our "Concepticon" in the sense of 
    ${h.external_link("http://bibliography.lingpy.org?key=Poornima2010", label='Poornima and Good (2010)')}.
</p>
<p>
    To each concept set, we add a rough <em>gloss</em>, but this is not
    supposed to be taken as the definition, just as a convenience abbreviation
    that offers further clarification as to what concept we try to describe.
    An attempt to give a more precise definition of each concept set is made by
    taking definitions from different sources, but also by adding them
    ourselves, if no valid definition is available.  For convenience, we also
    include <em>semantic fields</em> from the World Loanword Database (extended
    by us for new meanings that are not included there) and <em>ontological categories</em>.

    The ontological categories are mostly added for practical reasons of
    allowing us to order and link the concepts more quickly. They should not
    be taken as a serious semantic classification of the concept lists.

    For many concepts, additional meta-data, including links to
    ${h.external_link("https://babelnet.org", label="BabelNet")} and
    ${h.external_link("http://www.omegawiki.org", label="OmegaWiki")},
    are offered, will be expanded in future versions.
</p>

<h3>Contributing</h3>
<p>
    Our Concepticon is an ongoing community effort. Read our
    ${h.external_link('https://github.com/concepticon/concepticon-data/blob/master/CONTRIBUTING.md', label='contribution guidelines')}
    to find out how to become involved.
</p>


<h3>Funding</h3>

${req.dataset.jsondata['funding'].replace('<table>', '<table class="table table-striped table-condensed"')|n}


<%def name="sidebar()">
    <%util:well title="Acknowledgements">
        ${req.dataset.jsondata['people'].replace('<table>', '<table class="table table-striped table-condensed"')|n}
    </%util:well>
</%def>