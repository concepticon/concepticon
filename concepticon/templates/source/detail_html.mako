<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "sources" %>

<h2>${ctx.name}</h2>
${ctx.coins(request)|n}

<div class="tabbable">
    <ul class="nav nav-tabs">
        <li class="active"><a href="#tab1" data-toggle="tab">Text</a></li>
        <li><a href="#tab2" data-toggle="tab">BibTeX</a></li>
        <li><a href="#tab3" data-toggle="tab">RIS</a></li>
        <li><a href="#tab4" data-toggle="tab">MODS</a></li>
    </ul>
    <div class="tab-content">
        <% bibrec = ctx.bibtex() %>
        <div id="tab1" class="tab-pane active">
            <p id="${h.format_gbs_identifier(ctx)}">${bibrec.text()|n}</p>
            % if ctx.datadict().get('Additional_information'):
                <p>
                    ${ctx.datadict().get('Additional_information')}
                </p>
            % endif
            % if bibrec.get('url'):
                <p>${h.external_link(bibrec['url'])}</p>
            % endif
            ${util.gbs_links(filter(None, [ctx.gbs_identifier]))}
            % if ctx.jsondata.get('internetarchive_id'):
                <hr/>
                <iframe src='https://archive.org/stream/${ctx.jsondata.get('internetarchive_id')}?ui=embed#mode/1up'
                        width='680px' height='750px' frameborder='1'></iframe>
            % endif
            % if ctx._files:
                <p>
                    <a href="${ctx._files[0].jsondata}">
                        <span>
                            <i class="icon-file"></i> View file (${ctx._files[0].mime_type})
                        </span>
                    </a>
                </p>
            % endif
        </div>
        <div id="tab2" class="tab-pane">
            <pre>${bibrec}</pre>
        </div>
        <div id="tab3" class="tab-pane">
            <pre>${bibrec.format('ris')}</pre>
        </div>
        <div id="tab4" class="tab-pane">
            <pre>${bibrec.format('mods')}</pre>
        </div>
    </div>
</div>

<%def name="sidebar()">
    <% referents = context.get('referents', {}) %>
    % if referents['contribution']:
        <%util:well title="Concept lists">
            ${util.stacked_links(referents['contribution'])}
        </%util:well>
    % endif
</%def>
