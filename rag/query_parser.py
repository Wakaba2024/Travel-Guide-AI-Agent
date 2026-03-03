# rag/query_parser.py

import re


def parse_query(query: str) -> dict:
    query_lower = query.lower()

    result = {
        "max_budget": None,
        "duration_days": None,
        "style": None,
        "destination": None,
    }

    # -------- Budget --------
    budget_match = re.search(r"(under|below|less than)\s*\$?(\d+)", query_lower)
    if budget_match:
        result["max_budget"] = int(budget_match.group(2))

    # -------- Duration --------
    duration_match = re.search(r"(\d+)\s*(day|days)", query_lower)
    if duration_match:
        result["duration_days"] = int(duration_match.group(1))

    # -------- Style --------
    if "luxury" in query_lower:
        result["style"] = "luxury"
    elif "budget" in query_lower:
        result["style"] = "budget"
    elif "midrange" in query_lower:
        result["style"] = "midrange"

    # -------- Destination --------
    destinations = [
        "maasai mara", "diani", "amboseli",
        "nakuru", "naivasha", "mombasa",
        "zanzibar", "dubai", "tsavo"
    ]

    for d in destinations:
        if d in query_lower:
            result["destination"] = d.title()

    return result