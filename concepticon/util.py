"""
This module will be available in templates as ``u``.

This module is also used to lookup custom template context providers, i.e. functions
following a special naming convention which are called to update the template context
before rendering resource's detail or index views.
"""
import re

from markdown import markdown

from clld.web.util.helpers import get_referents
from clld.db.models.common import Contribution, Source


REF_PATTERN = re.compile(':ref:(?P<id>[^\)]+)')


def link_conceptlists(req, s):
    if not s:
        return ''

    def repl(m):
        ref = Contribution.get(m.group('id'), default=None)
        return req.resource_url(ref) if ref else m.group('id')

    return markdown(REF_PATTERN.sub(repl, s))


def dataset_detail_html(request=None, context=None, **kw):
    return {
        'Kraft1981': Source.get('kraft1981'),
    }


def source_detail_html(context=None, request=None, **kw):
    return dict(referents=get_referents(context, exclude=['valueset', 'language']))
