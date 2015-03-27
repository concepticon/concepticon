<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>

<%def name="sidebar()">
    <%util:well>
        <h4>Source</h4>
        <p>${h.link(request, ctx.source)}</p>
        <h4>Note</h4>
        <p>
            ${u.link_conceptlists(request, ctx.description)|n}
        </p>
    </%util:well>
</%def>

<h2>${_('Contribution')} ${ctx.name}</h2>

${request.get_datatable('values', h.models.Value, contribution=ctx).render()}
