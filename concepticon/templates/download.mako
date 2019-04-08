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

<div class="alert alert-info">
    ${cutil.repos_info()|n}
    <p>
        The "raw" data is best accessed using the
        ${h.external_link('https://pypi.org/project/pyconcepticon/', label='pyconcepticon')}
        Python package.
    </p>
</div>
${mpg.downloads(request)}

<%def name="sidebar()">
    <div class="well well-small">
        ${mpg.downloads_legend()}
    </div>
</%def>
