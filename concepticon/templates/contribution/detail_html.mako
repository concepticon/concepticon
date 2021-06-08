<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>

<%def name="sidebar()">
    <%util:well>
        <h4>${_('Contributors')}</h4>
        <ul class="unstyled">
            % for c in ctx.primary_contributors:
                <li>${h.link(request, c)}</li>
            % endfor
        </ul>
        <h4>Tags</h4>
        <ul class="inline">
            % for tag in ctx.tags:
                <li><span class="hint--left label label-success" data-hint="${tag.description}">${tag.name}</span></li>
            % endfor
        </ul>
        <h4>Source</h4>
        <ul class="unstyled">
            % for ref in ctx.references:
                <li>
                    ${h.link(request, ref.source)}
                    % if 'PAGES' in ctx.datadict():
                        (${ctx.datadict()['PAGES']})
                    % endif
                    % if ref.source.files:
                        ${u.cdstar.link(ref.source._files[0])}
                    % endif
                </li>
            % endfor
        </ul>
        % if 'URL' in ctx.datadict():
            ${h.external_link(ctx.datadict()['URL'])}
        % endif
        <h4>Target languages</h4>
        <p>${ctx.target_languages}</p>
        <h4>Most similar concept lists</h4>
        <table class="table table-condensed table-nonfluid">
            <thead>
                <tr><th>Concept list</th><th>Similarity score</th></tr>
            </thead>
            <tbody>
                <% rsc = [r for r in h.RESOURCES if r.name == 'contribution'][0] %>
                % for clid, score in ctx.jsondata['most_similar']:
                <tr>
                    <td><a href="${request.resource_url(clid, rsc=rsc)}">${clid}</a></td>
                    <td>${'{0:.2}'.format(score)}</td>
                </tr>
                % endfor
            </tbody>
        </table>
        % if ctx.data:
            <dl>
                % for d in [_d for _d in ctx.data if _d.value and _d.key not in ['PAGES', 'URL']]:
                <dt>${d.key.capitalize()}</dt>
                <dd>${d.value}</dd>
                % endfor
            </dl>
        % endif
    </%util:well>
</%def>

<h2>${_('Contribution')} ${ctx.name} ${u.github_link(ctx)|n}</h2>
<div>${ctx.description|n}</div>

% if ctx.excess_source_languages:
    <div class="alert alert-danger">
        This conceptlist contains glosses in more languages than we can display. Please refer to the
        ${h.external_link(ctx.github_url, 'data on GitHub')} for a complete list.
    </div>
% endif

${request.get_datatable('values', h.models.Value, contribution=ctx).render()}
