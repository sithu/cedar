from sqlalchemy import *
from migrate import *

from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()

col = Column('gender', String, default='M')

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pass


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pass
