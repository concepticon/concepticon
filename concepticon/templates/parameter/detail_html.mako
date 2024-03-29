<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${_('Parameter')} ${ctx.name}</%block>

<%def name="sidebar()">
    % if ctx.norare_datasets:
        <%util:well>
            <a href="https://norare.clld.org/parameters/${ctx.id}">
                <img width="50%" src="${req.static_url('concepticon:static/norare-logo.png')}"/>
            </a>
            <p>
                NoRaRe offers information about specific concept and word properties published along with
                studies from linguistics and psychology.
            </p>
            <p>
                The <a href="https://norare.clld.org/parameters/${ctx.id}">corresponding entry in NoRaRe</a> is
                linked to ${ctx.norare_variables} variables from ${ctx.norare_datasets} datasets.
            </p>
        </%util:well>
    % endif
</%def>

<h2>${_('Parameter')} ${ctx.name}</h2>

% if ctx.description:
<p class="alert alert-success">${ctx.description}</p>
% endif

% if ctx.rel_to or ctx.rel_from:
    <h3>Related concept sets</h3>
    <table class="table table-nonfluid">
        % for rel in ctx.rel_to:
        <tr>
            <td>${ctx.name}</td><td>${rel.description}</td><td>${h.link(request, rel.target)}</td>
        </tr>
        % endfor
        % for rel in ctx.rel_from:
        <tr>
            <td>${h.link(request, rel.source)}</td><td>${rel.description}</td><td>${ctx.name}</td>
        </tr>
        % endfor
    </table>
% endif

${request.get_datatable('values', h.models.Value, parameter=ctx).render()}
