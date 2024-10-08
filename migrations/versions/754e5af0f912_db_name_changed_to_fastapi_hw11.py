"""db_name changed to fastapi_hw11

Revision ID: 754e5af0f912
Revises: ff29329c7ed3
Create Date: 2024-09-07 13:28:32.807326

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '754e5af0f912'
down_revision: Union[str, None] = 'ff29329c7ed3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('notes', sa.ARRAY(sa.String()), nullable=True))
    op.drop_column('contacts', 'note')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('note', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('contacts', 'notes')
    # ### end Alembic commands ###
