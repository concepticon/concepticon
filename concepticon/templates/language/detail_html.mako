<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>

<h2>Concept labels in ${ctx.name}</h2>

${request.get_datatable('units', h.models.Unit, language=ctx).render()}

<%def name="sidebar()">
    <%util:well title="Conceptlists">
        <p>${ctx.name} is used as gloss language in ${len(ctx.conceptlist_assocs)} conceptlists:</p>
        <ul>
            % for cla in sorted(ctx.conceptlist_assocs, key=lambda a: a.conceptlist.id):
                <li>${h.link(req, cla.conceptlist)}</li>
            % endfor
        </ul>
    </%util:well>
</%def>

