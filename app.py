def print_method(
    number,
    name,
    description,
    results
):

    print("\n" + "=" * 60)

    print(f"{number}. {name}")

    print("=" * 60)

    print("Method:", description)

    print("Results:", len(results))

    pages = get_page_list(results)

    print("Pages:", pages)

    for i, result in enumerate(
        results,
        start=1
    ):

        print("\n" + "-" * 60)

        print(f"Result {i}")

        print("-" * 60)

        if isinstance(result, dict):

            chunk_id = result["chunk_id"]
            filename = result["filename"]
            page = result["page"]
            text = result["text"]

        else:

            chunk_id = result[0]
            filename = result[1]
            page = result[2]
            text = result[3]

        print("Chunk ID:", chunk_id)

        print("File:", filename)

        print("Page:", page)

        # Show hybrid ranking information
        if isinstance(result, dict):

            if "keyword_rank" in result:
                print(
                    "Keyword rank:",
                    result["keyword_rank"]
                )

            if "vector_rank" in result:
                print(
                    "Vector rank:",
                    result["vector_rank"]
                )

            if "hybrid_score" in result:
                print(
                    "Hybrid score:",
                    round(
                        result["hybrid_score"],
                        6
                    )
                )

        print("\nRetrieved Text:")

        print(text)