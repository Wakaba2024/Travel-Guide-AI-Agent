import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


def save_query(budget, days, style, location, query_text):
    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO user_queries
                (budget, days, style, location, query_text)
                VALUES (:budget, :days, :style, :location, :query_text)
            """),
            {
                "budget": budget,
                "days": days,
                "style": style,
                "location": location,
                "query_text": query_text
            }
        )
        conn.commit()