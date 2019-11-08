from collections import OrderedDict
from zipfile import ZIP_DEFLATED, ZipFile
from json import dumps
from pathlib import Path
import shutil

from sqlalchemy.orm import joinedload

from clld.db.meta import DBSession
from clld.db.models.common import Parameter, ValueSet
from clld.web.adapters.download import Download, README
from clld.web.adapters.md import TxtCitation

from concepticon.models import ConceptSet, Concept


JSON_DESC = """
Description
-----------

The file conceptset.json contains information about concept sets labels and alternative
labels used in concept lists in the following format:

```
{
    "conceptset_labels": {
        "run": [
            "1519",
            "RUN"
        ],
        ...
    }
    "alternative_labels": {
        "to run": [
            "1519",
            "RUN"
        ],
        ...
    }
}
```

The `conceptset_labels` dictionary maps the lowercased english unique concept set label
to pairs `(CONCEPTSET_ID, CONCEPTSET_LABEL)`, while
the `alternative_labels` dictionary maps the lowercased english labels encountered in
concept lists to pairs `(CONCEPTSET_ID, CONCEPTSET_LABEL)`.
"""


class ConceptSetLabels(Download):
    ext = 'json'
    description = "Concept sets and alternative labels as JSON"

    def create(self, req, filename=None, verbose=True):
        p = self.abspath(req)
        if not p.parent.exists():  # pragma: no cover
            p.parent.mkdir()
        tmp = Path('%s.tmp' % p.as_posix())

        with ZipFile(tmp.as_posix(), 'w', ZIP_DEFLATED) as zipfile:
            zipfile.writestr(self.name, dumps(create(), indent=4))
            zipfile.writestr(
                'README.txt',
                README.format(
                    req.dataset.name,
                    '=' * (len(req.dataset.name) + len(' data download')),
                    req.dataset.license,
                    TxtCitation(None).render(req.dataset, req)).encode('utf8') +
                JSON_DESC.encode('utf8'))
        if p.exists():  # pragma: no cover
            p.unlink()
        shutil.move(str(tmp), str(p))


def create():
    res = dict(conceptset_labels=OrderedDict(), alternative_labels=OrderedDict())
    for cs in DBSession.query(Parameter) \
            .options(
                joinedload(Parameter.valuesets)
                .joindeload(ValueSet.values)
                .joinedload(Concept.glosses)) \
            .order_by(Parameter.name):
        if int(cs.id):
            res['conceptset_labels'][cs.name.lower()] = (cs.id, cs.name)
            for vs in cs.valuesets:
                for value in vs.values:
                    for k, v in value.glossdict.items():
                        if k == 'english':
                            res['alternative_labels'][v.lower()] = (cs.id, cs.name)
    return res


def includeme(config):
    config.register_download(ConceptSetLabels(ConceptSet, 'concepticon'))
