from sqlalchemy import text
from db.database import engine


def insert_destination(data):
    """
    Safe insert that ignores duplicates.
    """

    query = text("""
        INSERT INTO destinations (name, county, category, description, source)
        VALUES (:name, :county, :category, :description, :source)
        ON CONFLICT (name, source) DO NOTHING
    """)

    with engine.begin() as conn:
        conn.execute(query, data)