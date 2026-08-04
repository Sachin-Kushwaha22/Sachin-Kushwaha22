from scripts.utils import load_svg, replace_many, save_svg


MAX_BAR_WIDTH = 320
LANGUAGE_LIMIT = 6


def update_languages(metrics: dict) -> None:
    language_totals = metrics["language_totals"]
    total_bytes = sum(language_totals.values())

    languages = [
        {
            "name": name,
            "percent": round((size / total_bytes) * 100, 1) if total_bytes else 0.0,
        }
        for name, size in language_totals.items()
    ]
    languages.sort(key=lambda language: language["percent"], reverse=True)

    top_languages = languages[:LANGUAGE_LIMIT]

    while len(top_languages) < LANGUAGE_LIMIT:
        top_languages.append({"name": "-", "percent": 0.0})

    values = {}

    for index, language in enumerate(top_languages, start=1):
        percent = language["percent"]

        values[f"LANG_{index}"] = language["name"]
        values[f"PERCENT_{index}"] = f"{percent:.1f}"
        values[f"PERCENT_{index}_STEP_1"] = f"{percent / 3:.1f}"
        values[f"PERCENT_{index}_STEP_2"] = f"{(percent * 2) / 3:.1f}"
        values[f"WIDTH_{index}"] = round((percent / 100) * MAX_BAR_WIDTH, 2)

    values["PRIMARY_STACK"] = (
        " • ".join(
            language["name"]
            for language in top_languages[:3]
            if language["name"] != "-"
        )
        or "-"
    )

    svg = load_svg("langs.svg")
    save_svg("langs.svg", replace_many(svg, values))
    print("✓ langs.svg updated.")
