from sqlalchemy import text
from db.database import engine


def insert_travel_package(data):
    query = text("""
        INSERT INTO travel_packages
        (package_name, price_usd, duration, company, destination, source, rating, category_type)
        VALUES
        (:package_name, :price_usd, :duration, :company, :destination, :source, :rating, :category_type)
        ON CONFLICT (package_name, company)
        DO UPDATE SET
            price_usd = EXCLUDED.price_usd,
            duration = EXCLUDED.duration,
            destination = EXCLUDED.destination,
            source = EXCLUDED.source,
            rating = EXCLUDED.rating,
            category_type =
                CASE
                    WHEN travel_packages.category_type = 'Safari' THEN 'Safari'
                    ELSE EXCLUDED.category_type
                END;
    """)

    with engine.connect() as conn:
        conn.execute(query, data)
        conn.commit()