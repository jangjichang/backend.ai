"""add_modified_at_to_users_and_kernels

Revision ID: e35332f8d23d
Revises: da24ff520049
Create Date: 2020-07-01 14:02:11.022032

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql.expression import bindparam

from ai.backend.manager.models.base import IDColumn, convention

# revision identifiers, used by Alembic.
revision = 'e35332f8d23d'
down_revision = 'da24ff520049'
branch_labels = None
depends_on = None


def upgrade():
    metadata = sa.MetaData(naming_convention=convention)
    # partial table to be preserved and referred
    users = sa.Table(
        'users', metadata,
        IDColumn('uuid'),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.func.now()),
        sa.Column('modified_at', sa.DateTime(timezone=True),
                  server_default=sa.func.now(), onupdate=sa.func.current_timestamp()),
    )
    keypairs = sa.Table(
        'keypairs', metadata,
        sa.Column('access_key', sa.String(length=20), primary_key=True),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.func.now()),
        sa.Column('modified_at', sa.DateTime(timezone=True),
                  server_default=sa.func.now(), onupdate=sa.func.current_timestamp()),
    )

    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('keypairs', sa.Column('modified_at', sa.DateTime(timezone=True),
                                        server_default=sa.text('now()'), nullable=True))
    op.add_column('users', sa.Column('modified_at', sa.DateTime(timezone=True),
                                     server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###

    conn = op.get_bind()

    # Set user's modified_at with the value of created_at.
    query = sa.select([users.c.uuid, users.c.created_at]).select_from(users)
    updates = []
    for row in conn.execute(query).fetchall():
        updates.append({'b_uuid': row['uuid'], 'modified_at': row['created_at']})
    if updates:
        query = (sa.update(users)
                   .values(modified_at=bindparam('modified_at'))
                   .where(users.c.uuid == bindparam('b_uuid')))
        conn.execute(query, updates)

    # Set keypairs's modified_at with the value of created_at.
    query = sa.select([keypairs.c.access_key, keypairs.c.created_at]).select_from(keypairs)
    updates = []
    for row in conn.execute(query).fetchall():
        updates.append({'b_access_key': row['access_key'], 'modified_at': row['created_at']})
    if updates:
        query = (sa.update(keypairs)
                   .values(modified_at=bindparam('modified_at'))
                   .where(keypairs.c.access_key == bindparam('b_access_key')))
        conn.execute(query, updates)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'modified_at')
    op.drop_column('keypairs', 'modified_at')
    # ### end Alembic commands ###
