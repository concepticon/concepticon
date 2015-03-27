<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>


<h2>${_('Value')} ${ctx.name}</h2>

<dl>
    <dt>Gloss:</dt>
    <dd>${ctx.name} [${h.link(request, ctx.valueset.language)}]</dd>
    <dt>Defined concept:</dt>
    <dd>${h.link(request, ctx.valueset.parameter)}</dd>
    <dt>Conceptlist:</dt>
    <dd>${h.link(request, ctx.valueset.contribution)}</dd>
    ## TODO: relations!
</dl>
