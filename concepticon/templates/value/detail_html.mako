<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "values" %>
<%! from clld_markdown_plugin import markdown %>

<%def name="sidebar()">
    <%util:well>
        <dl>
            <dt>${_('Parameter')}:</dt>
            <dd>${h.link(request, ctx.valueset.parameter)}</dd>
            <dt>${_('Contribution')}:</dt>
            <dd>${h.link(request, ctx.valueset.contribution)}</dd>
            <dd>
                ${markdown(req, ctx.valueset.contribution.description)|n}
            </dd>
        </dl>
    </%util:well>
</%def>

<h2>${_('Value')} ${ctx.label}</h2>

<table class="table table-condensed table-nonfluid">
    <thead>
    <tr>
        <th>Language</th>
        <th>Gloss</th>
    </tr>
    </thead>
    <tbody>
        % for g in ctx.glosses:
            <tr>
                <td>${h.link(req, g.language)}</td>
                <td>${g.name}</td>
            </tr>
        % endfor
    </tbody>
</table>

% if ctx.jsondata:
    <h3>Metadata</h3>
    <dl class="dl-horizontal">
        ##% if ctx.description:
    ##    <dt>English gloss:</dt>
    ##    <dd>${ctx.description}</dd>
    ##% endif
    % for k, v in ctx.jsondata.items():
        <dt>${k.capitalize()}:</dt>
        <dd>
            % if k == 'url':
       ${h.external_link(v)}
            % else:
       ${v}
            % endif
        </dd>
    % endfor
        ## TODO: relations!
</dl>
% endif
