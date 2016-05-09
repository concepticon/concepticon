# coding: utf8
from __future__ import unicode_literals
from collections import OrderedDict

from sqlalchemy.orm import joinedload_all

from clld.scripts.util import parsed_args
from clld.db.meta import DBSession
from clld.db.models.common import Parameter, ValueSet, Value
from clldutils.jsonlib import dump


def main(args):
    res = dict(conceptset_labels=OrderedDict(), alternative_labels=OrderedDict())
    for cs in DBSession.query(Parameter)\
            .options(joinedload_all(Parameter.valuesets, ValueSet.values, Value.data))\
            .order_by(Parameter.name):
        res['conceptset_labels'][cs.name.lower()] = (cs.id, cs.name)
        for vs in cs.valuesets:
            for value in vs.values:
                for k, v in value.datadict().items():
                    if k == 'lang_english':
                        res['alternative_labels'][v.lower()] = (cs.id, cs.name)
    dump(res, 'labels.json', indent=4)


if __name__ == '__main__':
    main(parsed_args())
