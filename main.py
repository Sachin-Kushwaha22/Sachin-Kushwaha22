import sys

from scripts.github_api import GitHubAPI
from scripts.utils import build_profile_metrics
from scripts.update_achievements import update_achievements
from scripts.update_languages import update_languages
from scripts.update_stats import update_stats


def main() -> int:
    try:
        print("Fetching GitHub profile data...")
        profile = GitHubAPI().get_profile()

        print("Calculating profile metrics...")
        metrics = build_profile_metrics(profile)

        print("Updating stats...")
        update_stats(metrics)

        print("Updating languages...")
        update_languages(metrics)

        print("Updating achievements...")
        update_achievements(metrics)

        print("Profile assets updated successfully.")
        return 0

    except Exception as error:
        print(f"Profile update failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
