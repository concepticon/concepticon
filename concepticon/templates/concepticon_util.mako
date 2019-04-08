<%def name="repos_info()">
    <p>
        <a href="${req.resource_url(req.dataset)}" style="font-family: monospace">concepticon.clld.org</a>
        serves the latest
        ${h.external_link('https://github.com/concepticon/concepticon-data/releases', label='released version')}
        of data curated at
        ${h.external_link('https://github.com/concepticon/concepticon-data', label='concepticon/concepticon-data')}.
        Older released version are accessible via <br/>
        <a href="https://doi.org/10.5281/zenodo.596412"><img
                src="https://zenodo.org/badge/DOI/10.5281/zenodo.596412.svg" alt="DOI"></a>
        <br/>
        on ZENODO as well.
    </p>
</%def>