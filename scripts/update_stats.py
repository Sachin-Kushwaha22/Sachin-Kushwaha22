from scripts.utils import load_svg, replace_many, save_svg


def update_stats(metrics: dict) -> None:
    svg = load_svg("stats.svg")

    values = {
        "USERNAME": metrics["username"],
        "FOLLOWERS": metrics["followers"],
        "FOLLOWING": metrics["following"],
        "REPOSITORIES": metrics["repository_count"],
        "STARS": metrics["total_stars"],
        "ISSUES": metrics["total_issues"],
        "PULL_REQUESTS": metrics["total_pull_requests"],
        "PROFILE_VIEWS": "--",
        "RING_LABEL": "PUBLIC REPOS",
        "RING_VALUE": metrics["repository_count"],
    }

    save_svg("stats.svg", replace_many(svg, values))
    print("✓ stats.svg updated.")
