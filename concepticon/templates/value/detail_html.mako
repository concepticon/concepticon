<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "values" %>


<h2>${_('Value')} ${ctx.name}</h2>

<dl>
    % for k, v in ctx.datadict().items():
        <dt>${k.split('_')[1].capitalize()}:</dt>
        <dd>${v}</dd>
    % endfor
    % if ctx.description:
        <dt>English gloss:</dt>
        <dd>${ctx.description}</dd>
    % endif
    <dt>${_('Parameter')}:</dt>
    <dd>${h.link(request, ctx.valueset.parameter)}</dd>
    <dt>${_('Contribution')}:</dt>
    <dd>${h.link(request, ctx.valueset.contribution)}</dd>
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
