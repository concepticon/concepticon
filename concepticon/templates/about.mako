<%inherit file="home_comp.mako"/>
<%namespace name="util" file="util.mako"/>

<h2>About the Concepticon</h2>

<p class="lead">
    A paper introducing our Concepticon will be presented at
    ${h.external_link('http://lrec2016.lrec-conf.org/', label='LREC 2016')}
    <a href="${request.static_url('concepticon:static/list-cysouw-forkel-2016-concepticon-introduction.pdf')}">[PDF]</a>.
    For more details, see below.
</p>

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
    <a href="http://bibliography.lingpy.org?key=Poornima2010">Poornima and Good (2010)</a>.
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
    The ontological categories are not supposed to be
    cross-linguistically comparable, but only a help to better identify the
    meaning, and as a way to order the different meanings. 
    For many concepts, additional meta-data, including links to <a href="http://babelnet.org">BabelNet</a> and <a href="http://www.omegawiki.org">OmegaWiki</a>, are offered, will be expanded in future versions.
</p>

<h3>Contributing</h3>
<p>
    Our Concepticon is an ongoing community effort. Read our
    ${h.external_link('https://github.com/clld/concepticon-data/blob/master/CONTRIBUTING.md', label='contribution guidelines')}
    to find out how to become involved.
</p>

<h3>Acknowledgements</h3>
<p>
  The development of the Concepticon in its current version was supported by the
  DFG research fellowship grant 261553824 <a href="http://gepris.dfg.de/gepris/projekt/261553824?language=en">Vertical and lateral aspects of
  Chinese dialect history</a> (JML) and the ERC starting grant 240816
  <a href="http://quanthistling.info/">Quantitative modelling of historicalcompara- tive linguistics</a> (JML,
  MC). As part of the <a href="http://clld.org">CLLD Project</a> 
  and the <a href="http://glottobank.org">Glottobank Project</a>, 
  the work was further supported by the Max Planck Society, the Max Planck Institute for the Science of Human
  History, and the Royal Society of New Zealand (Marsden Fund grant 13-UOA-121,
  RF). All support is gratefully acknowledged. 
</p>
<p>
  Many people helped us in many ways in assembling the data. They pointed us to
  missing lists (M), provided scans (S), digitized data (D), typed off and
  corrected concept lists (C), provided translations (T), linked concept lists
  (L), or gave important advice (A). For all this help, we are very grateful and
  express our gratitude to
  <ul>
    <li>Alexei Kassian (D),</li>
    <li>Andrew Kitchen (D),</li>
    <li>Damian Satterthwaite-Phillips (D),</li>
    <li>Frederike Urke (CLS),</li>
    <li>Harald Hammarström (DMS),</li>
    <li>Julia Fischer (SDT),</li>
    <li>Lars Borin (DL),</li>
    <li>Martin Haspelmath (AD),</li>
    <li>Nicholas Evans (A),</li>
    <li>Paul Heggarty (D),</li>
    <li>Robert Blust (D),</li>
    <li>Sean Lee (D),</li>
    <li>Sebastian Nicolai (CMS),</li>
    <li>Thiago Chacon (MSD), and</li>
    <li>Viola Kirchhoff da Cruz (CLS).</li>
  </ul>
</p>


