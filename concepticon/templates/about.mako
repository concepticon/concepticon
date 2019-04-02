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
    ${h.external_link('https://github.com/clld/concepticon-data/blob/master/CONTRIBUTING.md', label='contribution guidelines')}
    to find out how to become involved.
</p>


<h3>Funding</h3>

<table class="table table-nonfluid table-condensed table-striped">
<thead>
<tr>
<th>Period</th>
<th>Grant Name</th>
<th>Grant Type</th>
<th>Funding Agency</th>
<th>Grant Number</th>
<th>Beneficiaries</th>
</tr>
</thead>
<tbody>
<tr>
<td>2012-2014</td>
<td><em>Quantitative modelling of historical-comparative linguistics</em></td>
<td>ERC Starting Grant</td>
<td>European Research Council</td>
<td>240816</td>
<td>MC, JML</td>
</tr>
<tr>
<td>2015-2016</td>
<td><em>Vertical and lateral aspects of Chinese dialect history</em></td>
<td>Research Fellowship</td>
<td>German Research Council</td>
<td>261553824</td>
<td>JML</td>
</tr>
<tr>
<td>2017-now</td>
<td>${h.external_link("http://calc.digling.org", label="Computer-Assisted Language Comparison")}</td>
<td>Research Fellowship</td>
<td>German Research Council</td>
<td>261553824</td>
<td>JML</td>
</tr>
<tr>
<td>2012-2016</td>
<td></td>
<td>ARC Discovery Projects</td>
<td>Australian Research Council</td>
<td>DE 120101954</td>
<td>SJG</td>
</tr>
<tr>
<td>2015-now</td>
<td></td>
<td>Center of Excellence for the Dynamics of Language</td>
<td>Australian Research Council</td>
<td>CE140100041</td>
<td>SJG</td>
</tr>
<tr>
<td>2014-2017</td>
<td>${h.external_link("http://glottobank.org", label="Glottobank Project")}</td>
<td>Marsden Fund</td>
<td>Royal Society of New Zealand</td>
<td>13-UOA-121</td>
<td>SJG, JML, RF</td>
</tr>
<tr>
<td>2014-now</td>
<td>${h.external_link("http://glottobank.org", label="Glottobank Project")}</td>
<td></td>
<td>Max Planck Institute for the Science of Human history</td>
<td></td>
<td>SJG, JML, RF</td>
</tr>
<tr>
<td>2014-2017</td>
<td><a href="http://clld.org" rel="nofollow">CLLD Project</a></td>
<td></td>
<td>Max Planck Society</td>
<td></td>
<td></td>
</tr></tbody></table>


<%def name="sidebar()">
    <%util:well title="Acknowledgements">
        <p>
            Many people helped us in many
            ways in assembling the data. They pointed us to missing
            lists (M), provided scans (S), digitized data (D), typed off
            and corrected concept lists (C), provided translations (T),
            linked concept lists (L), provided corrections of concept definitions and concept linkings (P), or gave important advice (A), and (G) contributed new data via the GitHub-Workflow.
        </p>
        <p>
            For all this help, we are very grateful and express our gratitude.
        </p>

        <table class="table table-condensed table-nonfluid table-striped">
            <thead>
            <tr><th>Name</th>
                <th>Contribution</th>
                <th>Version</th></tr>
            </thead>
            <tbody>
            <tr><td>Alexei Kassian</td><td>D</td><td>1.0</td></tr>
            <tr><td>Andreea Calude</td><td>D</td><td>1.1</td></tr>
            <tr><td>Andrew Kitchen</td><td>D</td><td>1.0</td></tr>
            <tr><td>Anja Gampe</td><td>D</td><td>1.1</td></tr>
            <tr><td>Anthony Grant</td><td>MS</td><td>1.1</td></tr>
            <tr><td>Ben Yackley</td><td>P</td><td>1.1</td></tr>
            <tr><td>Christoph Rzymski</td><td>CLPG</td><td>1.1</td></tr>
            <tr><td>Claire Bowern</td><td>D</td><td>1.1</td></tr>
            <tr><td>Cormac Anderson</td><td>C</td><td>1.1</td></tr>
            <tr><td>Damian Satterthwaite-Phillips</td><td>D</td><td>1.0</td></tr>
            <tr><td>Doug Cooper</td><td>DCSM</td><td>1.1</td></tr>
            <tr><td>Evgeniya Korovina</td><td>MSCLPA</td><td>1.1</td></tr>
            <tr><td>Frederike Urke</td><td>CLS</td><td>1.0</td></tr>
            <tr><td>Harald Hammarström</td><td>DMS</td><td>1.0</td></tr>
            <tr><td>Isabella Boga</td><td>LP</td><td>1.1</td></tr>
            <tr><td>Jan Auracher</td><td>D</td><td>1.1</td></tr>
            <tr><td>Johannes Dellert</td><td>LPD</td><td>1.1</td></tr>
            <tr><td>Julia Fischer</td><td>SDT</td><td>1.0</td></tr>
            <tr><td>Lars Borin</td><td>DL</td><td>1.0</td></tr>
            <tr><td>Magdalena Łuniewska</td><td>D</td><td>1.1</td></tr>
            <tr><td>Martin Haspelmath</td><td>AD</td><td>1.0</td></tr>
            <tr><td>Maurizio Serva</td><td>MD</td><td>1.1</td></tr>
            <tr><td>Michael Dunn</td><td>G</td><td>1.1</td></tr>
            <tr><td>Nathan Hill</td><td>MSDP</td><td>1.1</td></tr>
            <tr><td>Nicholas Evans</td><td>A</td><td>1.0</td></tr>
            <tr><td>Paul Heggarty</td><td>D</td><td>1.0</td></tr>
            <tr><td>Quentin Atkinson</td><td>MD</td><td>1.1</td></tr>
            <tr><td>Robert Blust</td><td>D</td><td>1.0</td></tr>
            <tr><td>Sean Lee</td><td>D</td><td>1.0</td></tr>
            <tr><td>Sebastian Nicolai</td><td>CMS</td><td>1.0</td></tr>
            <tr><td>Thiago Chacon</td><td>MSD</td><td>1.0, 1.1</td></tr>
            <tr><td>Tiago Tresoldi</td><td>CTLG</td><td>1.1</td></tr>
            <tr><td>Viola Kirchhoff da Cruz</td><td>CLS</td><td>1.0</td></tr>
            <tr><td>Wang Feng</td><td>D</td><td>1.0</td></tr>
            </tbody>
        </table>

    </%util:well>
</%def>