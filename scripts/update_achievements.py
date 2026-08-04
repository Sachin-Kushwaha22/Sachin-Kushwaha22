from scripts.utils import load_svg, replace_many, save_svg


XP_PER_LEVEL = 1000
XP_BAR_WIDTH = 578
XP_BAR_START_X = 200


def _number(value: float) -> str:
    return f"{value:.2f}".rstrip("0").rstrip(".")


def calculate_achievement_values(metrics: dict) -> dict:
    """
    The XP score is derived entirely from GitHub profile data.
    Adjust the weights below only if you later want a different level curve.
    """
    total_xp = (
        metrics["repository_count"] * 100
        + metrics["total_stars"] * 25
        + metrics["followers"] * 20
        + metrics["following"] * 5
        + metrics["total_issues"] * 5
        + metrics["total_pull_requests"] * 15
    )

    account_level = (total_xp // XP_PER_LEVEL) + 1
    account_xp = total_xp % XP_PER_LEVEL
    xp_percent = round((account_xp / XP_PER_LEVEL) * 100, 1)
    bar_width = round((account_xp / XP_PER_LEVEL) * XP_BAR_WIDTH, 2)

    return {
        "TOTAL_REPOS": metrics["repository_count"],
        "TOTAL_STARS": metrics["total_stars"],
        "TOTAL_FOLLOWERS": metrics["followers"],
        "TOTAL_FOLLOWING": metrics["following"],
        "TOTAL_ISSUES": metrics["total_issues"],
        "TOTAL_PULL_REQUESTS": metrics["total_pull_requests"],
        "ACCOUNT_LEVEL": account_level,
        "ACCOUNT_XP": account_xp,
        "NEXT_LEVEL": XP_PER_LEVEL,
        "XP_BAR_WIDTH": _number(bar_width),
        "XP_DOT_X": _number(XP_BAR_START_X + bar_width),
        "XP_PERCENT": _number(xp_percent),
    }


def update_achievements(metrics: dict) -> None:
    svg = load_svg("achievements.svg")
    values = calculate_achievement_values(metrics)

    save_svg("achievements.svg", replace_many(svg, values))
    print("✓ achievements.svg updated.")
