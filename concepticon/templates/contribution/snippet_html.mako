<%! from clld_markdown_plugin import markdown %>
<div>${markdown(req, ctx.description)|n}</div>
