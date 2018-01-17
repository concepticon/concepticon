# coding=utf-8
"""bundle unlinked concepts

Revision ID: c440e8ef9626
Revises: 1aabb3eb6546
Create Date: 2018-01-17 11:50:09.944092

"""

# revision identifiers, used by Alembic.
revision = 'c440e8ef9626'
down_revision = '5a9b3ae30643'

import datetime

from alembic import op
import sqlalchemy as sa



def upgrade():
    # for each contribution, get concepts linked to paramter_pk = 1,
    # update valueset_pk to point to the first corresponding valueset.
    conn = op.get_bind()
    pk_sets = []
    for row in conn.execute("select parameter_pk, contribution_pk, array_agg(pk) from valueset group by parameter_pk, contribution_pk having count(pk) > 1;"):
        pk_sets.append(sorted(row[2], reverse=True))
    for pk_set in pk_sets:
        keep = pk_set.pop()
        for pk in pk_set:
            conn.execute("update value set valueset_pk = %s where valueset_pk = %s", (keep, pk))


def downgrade():
    pass

