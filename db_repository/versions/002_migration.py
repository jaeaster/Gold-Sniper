from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
apscheduler_jobs = Table('apscheduler_jobs', pre_meta,
    Column('id', String, primary_key=True, nullable=False),
    Column('next_run_time', Float),
    Column('job_state', LargeBinary, nullable=False),
)

snipe = Table('snipe', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('snipe_name', String(length=140)),
    Column('enroll_code', String(length=10)),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['apscheduler_jobs'].drop()
    post_meta.tables['snipe'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['apscheduler_jobs'].create()
    post_meta.tables['snipe'].drop()
