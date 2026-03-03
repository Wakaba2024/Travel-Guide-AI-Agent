from rag.vector_store import similarity_search


def retrieve_context(query: str, k: int = 5):

    results = similarity_search(query, k)

    if not results:
        return "No relevant travel packages found."

    context_blocks = []

    for row in results:
        doc_id = row[0]
        title = row[1]
        content = row[2]
        doc_type = row[3]

        block = f"""
==============================
Type: {doc_type.upper()}
Title: {title}
Details: {content}
Document ID: {doc_id}
==============================
"""
        context_blocks.append(block)

    return "\n".join(context_blocks)


if __name__ == "__main__":
    print(retrieve_context("Best budget safari in Kenya"))