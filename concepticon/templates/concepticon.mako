<%inherit file="app.mako"/>

<%block name="brand">
    <a class="brand" href="${request.route_url('dataset')}">Concepticon</a>
</%block>

${next.body()}
