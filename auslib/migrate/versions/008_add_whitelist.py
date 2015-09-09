from sqlalchemy import String, MetaData, Table


def upgrade(migrate_engine):
    # TODO: add whitelist column
    metadata = MetaData(bind=migrate_engine)


def downgrade(migrate_engine):
    # TODO: remove whitelist column
    metadata = MetaData(bind=migrate_engine)
