from sqlalchemy import text
from rag.database import engine


def get_recommendations(budget=None, days=None, style=None, location=None):

    with engine.connect() as conn:

        base_query = """
        SELECT 
            id,
            package_name,
            destination,
            duration,
            price_usd,
            category_type,
            company
        FROM travel_packages
        WHERE 1=1
        """

        params = {}

        # STRICT LOCATION
        if location and location.strip():
            base_query += " AND LOWER(destination) LIKE :location"
            params["location"] = f"%{location.lower().strip()}%"

        # STRICT BUDGET
        if budget:
            base_query += " AND (price_usd IS NULL OR price_usd <= :budget)"
            params["budget"] = budget

        result = conn.execute(text(base_query), params)
        rows = result.fetchall()

        # --- SOFT RANKING LAYER ---
        scored_results = []

        for row in rows:
            score = 0

            package_name = (row.package_name or "").lower()
            category = (row.category_type or "").lower()
            duration = (row.duration or "").lower()

            # Style matching boosts score
            if style:
                if style.lower() in package_name:
                    score += 3
                if style.lower() in category:
                    score += 2

            # Days similarity boosts score
            if days:
                if str(days) in duration:
                    score += 2

            # Luxury boost for high price
            if style and style.lower() == "luxury":
                if row.price_usd and row.price_usd >= 3000:
                    score += 4

            scored_results.append((score, row))

        # Sort by score descending then price ascending
        scored_results.sort(
            key=lambda x: (-x[0], x[1].price_usd if x[1].price_usd else 999999)
        )

        return [r[1] for r in scored_results[:12]]