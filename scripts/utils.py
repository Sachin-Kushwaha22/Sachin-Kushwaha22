from pathlib import Path
from collections import defaultdict
from typing import Any
from config import ASSETS_DIR


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIRECTORY = ".templates"


def _asset_path(filename: str) -> Path:
    return PROJECT_ROOT / ASSETS_DIR / filename


def _template_path(filename: str) -> Path:
    return _asset_path(filename).parent / TEMPLATE_DIRECTORY / filename


def load_svg(filename: str) -> str:
    """
    Load the immutable SVG template. On the first successful run, preserve the
    original SVG inside assets/.templates so scheduled runs remain idempotent.
    """
    asset_path = _asset_path(filename)
    template_path = _template_path(filename)

    if not template_path.exists():
        if not asset_path.exists():
            raise FileNotFoundError(f"{filename} not found in the assets directory.")

        template_path.parent.mkdir(parents=True, exist_ok=True)
        template_path.write_text(
            asset_path.read_text(encoding="utf-8"), encoding="utf-8"
        )

    return template_path.read_text(encoding="utf-8")


def save_svg(filename: str, content: str) -> None:
    """Atomically save a rendered SVG into the assets directory."""
    asset_path = _asset_path(filename)
    temporary_path = asset_path.with_suffix(f"{asset_path.suffix}.tmp")

    temporary_path.write_text(content, encoding="utf-8")
    temporary_path.replace(asset_path)


def replace_placeholder(svg: str, placeholder: str, value) -> str:
    """Replace one {{PLACEHOLDER}} token."""
    return svg.replace(f"{{{{{placeholder}}}}}", str(value))


def replace_many(svg: str, values: dict[str, object]) -> str:
    """Replace all supplied {{PLACEHOLDER}} tokens."""
    for placeholder, value in values.items():
        svg = replace_placeholder(svg, placeholder, value)

    return svg


# Keeps compatibility with the existing helper name.
def replace(svg: str, placeholder: str, value) -> str:
    return replace_placeholder(svg, placeholder, value)

def build_profile_metrics(profile: dict[str, Any]) -> dict[str, Any]:
    repositories_connection = profile.get("repositories") or {}
    repositories = repositories_connection.get("nodes") or []

    language_totals: defaultdict[str, int] = defaultdict(int)
    total_stars = 0
    total_issues = 0
    total_pull_requests = 0

    for repository in repositories:
        total_stars += int(repository.get("stargazerCount", 0))
        total_issues += int((repository.get("issues") or {}).get("totalCount", 0))
        total_pull_requests += int(
            (repository.get("pullRequests") or {}).get("totalCount", 0)
        )

        for edge in (repository.get("languages") or {}).get("edges") or []:
            language = edge.get("node") or {}
            if language.get("name"):
                language_totals[language["name"]] += int(edge.get("size", 0))

    return {
        "username": profile.get("login", ""),
        "followers": int((profile.get("followers") or {}).get("totalCount", 0)),
        "following": int((profile.get("following") or {}).get("totalCount", 0)),
        "repository_count": int(repositories_connection.get("totalCount", 0)),
        "total_stars": total_stars,
        "total_issues": total_issues,
        "total_pull_requests": total_pull_requests,
        "language_totals": dict(language_totals),
    }