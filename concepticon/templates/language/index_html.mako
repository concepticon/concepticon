<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Languages')}</%block>

<h2>Gloss languages</h2>

<p>
    Concepticon contains concepts glossed in many languages; although, due to the motivation behind
    the conceptlists, the focus is on lingua francas for the targeted region of data collection.
</p>

% if map_ or request.map:
${(map_ or request.map).render()}
% endif

${ctx.render()}
