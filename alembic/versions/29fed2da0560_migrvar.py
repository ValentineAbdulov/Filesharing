"""migrVAR

Revision ID: 29fed2da0560
Revises: d516410efb33
Create Date: 2023-12-10 10:14:40.496887

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29fed2da0560'
down_revision: Union[str, None] = 'd516410efb33'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('files', 'filename',
               existing_type=sa.CHAR(length=255),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
    op.alter_column('files', 'link_code',
               existing_type=sa.CHAR(length=255),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)
    op.alter_column('users', 'username',
               existing_type=sa.CHAR(length=36),
               type_=sa.VARCHAR(length=36),
               existing_nullable=False)
    op.alter_column('users', 'first_name',
               existing_type=sa.CHAR(length=36),
               type_=sa.VARCHAR(length=36),
               existing_nullable=True)
    op.alter_column('users', 'last_name',
               existing_type=sa.CHAR(length=36),
               type_=sa.VARCHAR(length=36),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(length=36),
               type_=sa.CHAR(length=36),
               existing_nullable=True)
    op.alter_column('users', 'first_name',
               existing_type=sa.VARCHAR(length=36),
               type_=sa.CHAR(length=36),
               existing_nullable=True)
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(length=36),
               type_=sa.CHAR(length=36),
               existing_nullable=False)
    op.alter_column('files', 'link_code',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.CHAR(length=255),
               existing_nullable=False)
    op.alter_column('files', 'filename',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.CHAR(length=255),
               existing_nullable=False)
    # ### end Alembic commands ###