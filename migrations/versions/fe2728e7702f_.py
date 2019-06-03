"""empty message

Revision ID: fe2728e7702f
Revises: eb799ea51e5f
Create Date: 2019-06-03 15:01:45.499524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe2728e7702f'
down_revision = 'eb799ea51e5f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('StudentNum_4', table_name='student')
    op.drop_index('TeacherNum_3', table_name='teacher')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('TeacherNum_3', 'teacher', ['TeacherNum'], unique=False)
    op.create_index('StudentNum_4', 'student', ['StudentNum'], unique=False)
    # ### end Alembic commands ###
