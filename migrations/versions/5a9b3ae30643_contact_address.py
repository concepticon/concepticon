# coding=utf-8
"""contact address

Revision ID: 5a9b3ae30643
Revises: None
Create Date: 2015-10-07 11:22:09.067186

"""

# revision identifiers, used by Alembic.
revision = '5a9b3ae30643'
down_revision = None

import datetime

from alembic import op
import sqlalchemy as sa



def upgrade():
    op.execute("update dataset set contact = 'concepticon@shh.mpg.de'")


def downgrade():
    pass

