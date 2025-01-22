from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'aee12ee92814'
down_revision = '221ea224621d'
branch_labels = None
depends_on = None

def upgrade():
    # Create a new table with the desired schema
    op.create_table(
        'todos_new',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=False),
        sa.Column('state', sa.String, nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    )

    # Copy data from the old table to the new table
    op.execute('''
        INSERT INTO todos_new (id, title, description, state, user_id)
        SELECT id, title, description, state, user_id FROM todos
    ''')

    # Drop the old table
    op.drop_table('todos')

    # Rename the new table to the original table name
    op.rename_table('todos_new', 'todos')

def downgrade():
    # Create the old table without the new columns
    op.create_table(
        'todos_old',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=False),
        sa.Column('state', sa.String, nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
    )

    # Copy data from the current table to the old table
    op.execute('''
        INSERT INTO todos_old (id, title, description, state, user_id)
        SELECT id, title, description, state, user_id FROM todos
    ''')

    # Drop the current table
    op.drop_table('todos')

    # Rename the old table back to the original table name
    op.rename_table('todos_old', 'todos')
