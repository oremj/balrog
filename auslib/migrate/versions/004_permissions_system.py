from sqlalchemy import Column, Boolean, MetaData, Table

def upgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    def add_system(table):
        system = Column('system', Boolean, default=False)
        system.create(table)
    add_system(Table('permissions', metadata, autoload=True))
    add_system(Table('permissions_history', metadata, autoload=True))

def downgrade(migrate_engine):
    metadata = MetaData(bind=migrate_engine)
    Table('permissions', metadata, autoload=True).c.system.drop()
    Table('permissions_history', metadata, autoload=True).c.system.drop()
