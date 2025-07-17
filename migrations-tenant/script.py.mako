"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op, context
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, Sequence[str], None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade():
    schema = context.get_context().opts['schema_translate_map'][None]
    op.execute(f"""
    CREATE TABLE IF NOT EXISTS "{schema}".your_table_name (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL
    );
    """)

def downgrade():
    schema = context.get_context().opts['schema_translate_map'][None]
    op.execute(f'DROP TABLE IF EXISTS "{schema}".your_table_name')