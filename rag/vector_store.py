import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

from rag.embeddings import generate_embedding
from rag.query_parser import parse_query

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables.")

engine = create_engine(DATABASE_URL)



# 1️ EMBED MISSING DOCUMENTS

def embed_missing_documents():
    """
    Embed travel_packages and destinations
    with enriched semantic context.
    """

    with engine.begin() as conn:

        # -------- Travel Packages --------
        travel_rows = conn.execute(text("""
            SELECT id, package_name, destination, duration, price_usd
            FROM travel_packages
            WHERE embedding IS NULL
        """)).fetchall()

        print(f"Found {len(travel_rows)} travel packages to embed")

        for row in travel_rows:
            doc_id = row[0]
            name = row[1] or ""
            destination = row[2] or ""
            duration = row[3] or ""
            price = row[4] or ""

            # 🔥 Enriched semantic embedding text
            text_content = f"""
            Travel Package: {name}
            Destination: {destination}
            Duration: {duration}
            Price: ${price}

            This Kenya travel package may include:
            safari wildlife experiences,
            Maasai Mara game drives,
            beach relaxation in Diani or Mombasa,
            cultural tourism,
            luxury lodges,
            honeymoon escapes,
            adventure activities,
            or budget-friendly travel options.
            """

            embedding = generate_embedding(text_content)
            vector_string = "[" + ",".join(str(x) for x in embedding) + "]"

            conn.execute(text("""
                UPDATE travel_packages
                SET embedding = CAST(:embedding AS vector)
                WHERE id = :id
            """), {
                "embedding": vector_string,
                "id": doc_id
            })

            print(f"Embedded travel package ID {doc_id}")

        # -------- Destinations --------
        destination_rows = conn.execute(text("""
            SELECT id, name, description
            FROM destinations
            WHERE embedding IS NULL
        """)).fetchall()

        print(f"Found {len(destination_rows)} destinations to embed")

        for row in destination_rows:
            doc_id = row[0]
            name = row[1] or ""
            description = row[2] or ""

            text_content = f"""
            Kenya Destination: {name}

            Description:
            {description}

            This destination may include:
            safari parks,
            beaches,
            wildlife reserves,
            adventure travel,
            relaxing vacations,
            family trips,
            luxury experiences,
            or budget tourism.
            """

            embedding = generate_embedding(text_content)
            vector_string = "[" + ",".join(str(x) for x in embedding) + "]"

            conn.execute(text("""
                UPDATE destinations
                SET embedding = CAST(:embedding AS vector)
                WHERE id = :id
            """), {
                "embedding": vector_string,
                "id": doc_id
            })

            print(f"Embedded destination ID {doc_id}")



# 2️ HYBRID SIMILARITY SEARCH WITH SMART FALLBACK


def similarity_search(query: str, k: int = 5):
    """
    Hybrid search flow:
    1. Strict filters
    2. Remove destination
    3. Remove style
    4. Pure vector fallback
    """

    parsed = parse_query(query)

    query_embedding = generate_embedding(query)
    vector_string = "[" + ",".join(str(x) for x in query_embedding) + "]"

    def run_query(parsed_filters):

        where_clauses = ["embedding IS NOT NULL"]
        params = {
            "query_embedding": vector_string,
            "k": k
        }

        # -------- Budget Filter --------
        if parsed_filters.get("max_budget"):
            where_clauses.append("price_usd <= :max_budget")
            params["max_budget"] = parsed_filters["max_budget"]

        # -------- Duration Filter --------
        if parsed_filters.get("duration_days"):
            where_clauses.append("duration ILIKE :duration")
            params["duration"] = f"%{parsed_filters['duration_days']}%"

        # -------- Destination Filter --------
        if parsed_filters.get("destination"):
            where_clauses.append("""
                (
                    destination ILIKE :destination
                    OR package_name ILIKE :destination
                )
            """)
            params["destination"] = f"%{parsed_filters['destination']}%"

        # -------- Style Filter --------
        if parsed_filters.get("style"):
            where_clauses.append("package_name ILIKE :style")
            params["style"] = f"%{parsed_filters['style']}%"

        where_sql = " AND ".join(where_clauses)

        sql = f"""
        SELECT 
            id,
            package_name AS title,
            destination || ' - ' || duration || ' - $' || price_usd AS content,
            'package' AS doc_type
        FROM travel_packages
        WHERE {where_sql}
        AND embedding <-> CAST(:query_embedding AS vector) < 0.9
        ORDER BY embedding <-> CAST(:query_embedding AS vector)
        LIMIT :k;
        """

        with engine.begin() as conn:
            results = conn.execute(text(sql), params).fetchall()

        return results

    # 1️⃣ Strict search
    results = run_query(parsed)
    if results:
        return results

    # 2️⃣ Remove destination
    relaxed_1 = parsed.copy()
    relaxed_1["destination"] = None

    results = run_query(relaxed_1)
    if results:
        return results

    # 3️⃣ Remove style
    relaxed_2 = relaxed_1.copy()
    relaxed_2["style"] = None

    results = run_query(relaxed_2)
    if results:
        return results

    # 4️⃣ Pure vector fallback
    pure = {
        "max_budget": None,
        "duration_days": None,
        "style": None,
        "destination": None
    }

    return run_query(pure)