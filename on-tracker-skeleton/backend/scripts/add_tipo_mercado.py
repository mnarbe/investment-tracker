from sqlalchemy import create_engine, text
import os

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    # fallback to the one provided in the conversation
    DATABASE_URL = 'postgresql://neondb_owner:npg_9UeRx5LWjIYh@ep-young-sound-acz7vqv2-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'

print('Using DATABASE_URL:', '***hidden***' if DATABASE_URL else 'None')
engine = create_engine(DATABASE_URL)
with engine.begin() as conn:
    try:
        conn.execute(text('ALTER TABLE obligacionnegociable ADD COLUMN tipo_mercado VARCHAR;'))
        print('Added column tipo_mercado')
    except Exception as e:
        print('ALTER TABLE error:', e)
    try:
        conn.execute(text("UPDATE obligacionnegociable SET tipo_mercado='PRIMARIO' WHERE tipo_mercado IS NULL;"))
        print('Updated existing rows to PRIMARIO where null')
    except Exception as e:
        print('UPDATE error:', e)
print('Done')
