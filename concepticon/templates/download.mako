<%inherit file="home_comp.mako"/>
<%namespace name="mpg" file="clldmpg_util.mako"/>
<%namespace name="cutil" file="concepticon_util.mako"/>

<%block name="head">
    <style>
        a.accordion-toggle {
            font-weight: bold;
        }
    </style>
</%block>

<h3>Downloads</h3>

<div class="alert alert-warning">
    <p>
        Starting with release 3.0.0, the Concepticon data is available as CLDF dataset from Zenodo via
        <a href="https://doi.org/10.5281/zenodo.7298022">DOI: 10.5281/zenodo.7298022</a>. The metadata linked
        to Concepticon concept sets that was previously made available in this web app as well, has now moved
        to <a href="https://norare.clld.org">NoRaRe</a>.
    </p>
    ${cutil.repos_info()|n}
</div>
${mpg.downloads(request)}

<%def name="sidebar()">
    <div class="well well-small">
        ${mpg.downloads_legend()}
    </div>
</%def>
