<%inherit file="app.mako"/>

<%block name="brand">
    <a class="brand" href="${request.route_url('dataset')}">
        <img width="20" height="20" src="${request.static_url('concepticon:static/favicon.png')}"/>
        Concepticon
    </a>
</%block>

${next.body()}
