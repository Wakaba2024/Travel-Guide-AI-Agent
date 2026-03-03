from rag.recommendation_engine import get_recommendations
from rag.llm import generate_response


def build_context(results):
    """
    Builds structured context string for the LLM,
    including trend intelligence and personalization.
    """

    context_blocks = []

    for r in results:
        trend_label = ""
        if r.trend_score and r.trend_score > 0.8:
            trend_label = "🔥 Trending this week"
        elif r.trend_score and r.trend_score > 0.6:
            trend_label = "📈 Popular choice"

        price_text = (
            f"${r.price_usd}"
            if r.price_usd
            else "Price not listed"
        )

        block = f"""
Package: {r.package_name}
Destination: {r.destination}
Duration: {r.duration}
Price: {price_text}
Trend Score: {round(r.trend_score, 2) if r.trend_score else 0}
{trend_label}
        """

        context_blocks.append(block.strip())

    return "\n\n".join(context_blocks)


def build_prompt(context, budget, days, style, location):
    """
    Creates intelligent prompt with personalization
    """

    return f"""
You are Kenya Tourism Intelligence Assistant 🇰🇪

User Preferences:
- Budget: {budget if budget else "Not specified"}
- Duration: {days if days else "Flexible"}
- Travel Style: {style if style else "Open"}
- Preferred Location: {location if location else "Anywhere in Kenya"}

Available Recommendations:
{context}

Instructions:
1. Recommend the best matching packages.
2. Mention if a destination is trending.
3. Highlight budget-friendly options if price is available.
4. Keep tone friendly and Kenyan.
5. If price is missing, say "Contact provider for pricing".
6. Explain WHY the package fits the user's preferences.
7. Keep response structured and clear.

Respond now:
"""


def main():
    print("Kenya Tourism Intelligence Assistant 🇰🇪\n")

    budget_input = input("Enter your budget (or leave blank): ").strip()
    days_input = input("How many days? ").strip()
    style_input = input(
        "Travel style (adventure, relaxing, family, honeymoon, luxury, budget): "
    ).strip()
    location_input = input("Preferred location: ").strip()

    budget = float(budget_input) if budget_input else None
    days = days_input if days_input else None
    style = style_input if style_input else None
    location = location_input if location_input else None

    results = get_recommendations(
        budget=budget,
        days=days,
        style=style,
        location=location
    )

    if not results:
        print("\nAI Response:\n")
        print("No matching travel packages found.")
        return

    context = build_context(results)

    prompt = build_prompt(
        context,
        budget,
        days,
        style,
        location
    )

    response = generate_response(prompt)

    print("\nAI Response:\n")
    print(response)


if __name__ == "__main__":
    main()