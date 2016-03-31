<%inherit file="home_comp.mako"/>
<%namespace name="util" file="util.mako"/>

<h2>About Concepticon</h2>

<p>
    A paper introducing Concepticon was submitted to LREC 2016
    <a href="${request.static_url('concepticon:static/list-cysouw-forkel-2016-concepticon-introduction.pdf')}">[PDF]</a>.
</p>


<h3>Contributing</h3>
<p>
    Concepticon is an ongoing community effort. Read our
    ${h.external_link('https://github.com/clld/concepticon-data/blob/master/CONTRIBUTING.md', label='contribution guidelines')}
    to find out how to become involved.
</p>

<h4>Acknowledgements</h4>
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
