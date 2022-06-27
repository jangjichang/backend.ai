"""enumerate_vfolder_perms

Revision ID: a1fd4e7b7782
Revises: f9971fbb34d9
Create Date: 2018-09-05 16:51:49.973195

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from ai.backend.manager.models import VFolderPermission

# revision identifiers, used by Alembic.
revision = 'a1fd4e7b7782'
down_revision = 'f9971fbb34d9'
branch_labels = None
depends_on = None

# NOTE: VFolderPermission is EnumValueType
vfperm_choices = list(map(lambda v: v.value, VFolderPermission))
vfolderpermission = postgresql.ENUM(
    *vfperm_choices,
    name='vfolderpermission',
)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    vfolderpermission.create(op.get_bind())
    op.alter_column('vfolder_invitations', column_name='permission',
                    type_=sa.Enum(*vfperm_choices, name='vfolderpermission'),
                    postgresql_using='permission::vfolderpermission')
    op.alter_column('vfolder_permissions', column_name='permission',
                    type_=sa.Enum(*vfperm_choices, name='vfolderpermission'),
                    postgresql_using='permission::vfolderpermission')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('vfolder_invitations', column_name='permission',
                    type_=sa.String(length=2),
                    postgresql_using='permission::text::vfolderpermission')
    op.alter_column('vfolder_permissions', column_name='permission',
                    type_=sa.String(length=2),
                    postgresql_using='permission::text::vfolderpermission')
    vfolderpermission.drop(op.get_bind())
    # ### end Alembic commands ###
