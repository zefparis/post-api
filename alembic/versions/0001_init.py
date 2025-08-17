from __future__ import annotations
from alembic import op
import sqlalchemy as sa

revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('partners',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True)),
        sa.Column('api_key_hash', sa.String(255)),
        sa.Column('status', sa.String(50), nullable=False, server_default='active'),
    )
    op.create_index(op.f('ix_partners_email'), 'partners', ['email'], unique=True)

    op.create_table('assets',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('summary', sa.Text(), nullable=False),
        sa.Column('payload_json', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True)),
        sa.Column('partner_id', sa.Integer(), nullable=False),
    )

    op.create_table('posts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('asset_id', sa.Integer(), nullable=False),
        sa.Column('partner_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('target_url', sa.String(2048), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True)),
        sa.Column('status', sa.String(50), nullable=False, server_default='active'),
    )

    op.create_table('links',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('code', sa.String(16), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('partner_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True)),
    )
    op.create_index(op.f('ix_links_code'), 'links', ['code'], unique=True)

    op.create_table('click_events',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('link_id', sa.Integer(), nullable=False),
        sa.Column('partner_id', sa.Integer(), nullable=False),
        sa.Column('ts', sa.DateTime(timezone=True)),
        sa.Column('ip', sa.String(64), nullable=False),
        sa.Column('ua', sa.String(512), nullable=False),
        sa.Column('referer', sa.String(1024)),
        sa.Column('country', sa.String(8)),
        sa.Column('asn', sa.String(16)),
        sa.Column('fingerprint', sa.String(128)),
        sa.Column('risk_score', sa.Float(), nullable=False),
        sa.Column('payable_amount_eur', sa.Float(), nullable=False, server_default='0'),
        sa.Column('payable', sa.Boolean(), nullable=False, server_default=sa.text('false')),
    )
    op.create_index('idx_click_link_ts', 'click_events', ['link_id', 'ts'])

    op.create_table('metric_events',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('post_id', sa.Integer()),
        sa.Column('platform', sa.String(64)),
        sa.Column('kind', sa.String(64), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True)),
        sa.Column('metadata_json', sa.Text()),
    )

    op.create_table('balances',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('partner_id', sa.Integer(), nullable=False, unique=True),
        sa.Column('available_eur', sa.Float(), nullable=False, server_default='0'),
        sa.Column('on_hold_eur', sa.Float(), nullable=False, server_default='0'),
        sa.Column('lifetime_eur', sa.Float(), nullable=False, server_default='0'),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )

    op.create_table('jobs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('kind', sa.String(64), nullable=False),
        sa.Column('payload', sa.Text(), nullable=False),
        sa.Column('status', sa.String(32), nullable=False, server_default='queued'),
        sa.Column('attempts', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('last_error', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True)),
    )


def downgrade() -> None:
    for name in ['jobs','balances','metric_events','click_events','links','posts','assets','partners']:
        try:
            op.drop_table(name)
        except Exception:
            pass
