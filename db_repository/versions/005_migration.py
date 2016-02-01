from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
adjustment = Table('adjustment', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('category', String(length=64)),
    Column('description', Text),
    Column('adjStrength', Integer),
    Column('adjDexterity', Integer),
    Column('adjConstitution', Integer),
    Column('adjIntelligence', Integer),
    Column('adjWisdom', Integer),
    Column('adjCharisma', Integer),
    Column('adjAbiCheck', Integer),
    Column('adjStrCheck', Integer),
    Column('adjDexCheck', Integer),
    Column('adjConCheck', Integer),
    Column('adjIntCheck', Integer),
    Column('adjWisCheck', Integer),
    Column('adjChaCheck', Integer),
    Column('adjAttack', Integer),
    Column('adjMelee', Integer),
    Column('adjRanged', Integer),
    Column('adjCMB', Integer),
    Column('adjDef', Integer),
    Column('adjAC', Integer),
    Column('adjCMD', Integer),
    Column('adjSaves', Integer),
    Column('adjFort', Integer),
    Column('adjRef', Integer),
    Column('adjWill', Integer),
    Column('adjSkills', Integer),
    Column('adjInit', Integer),
    Column('adjSpeed', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['adjustment'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['adjustment'].drop()
