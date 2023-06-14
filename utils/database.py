import sqlalchemy
from sqlalchemy import text
from dotenv import dotenv_values

config = dotenv_values(".env")

engine = sqlalchemy.create_engine(
    f"postgresql://{config['DB_USER']}:{config['DB_PASS']}@{config['DB_HOST']}:{config['DB_PORT']}/{config['DB_NAME']}"
)

def insert_api_call(data, result):
    query = text(f"""
        INSERT INTO api_calls (data, result)
        VALUES ('{data}', '{result}')
    """)
    with engine.connect() as connection:
        connection.execute(query)
