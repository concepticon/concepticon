<%inherit file="app.mako"/>

<%block name="brand">
    <a class="brand" href="${request.route_url('dataset')}" style="padding: 2px;">
        <img width="55" src="${request.static_url('concepticon:static/logo.png')}"/>
    </a>
</%block>

${next.body()}
