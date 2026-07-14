#!/usr/bin/env python3
"""Refresh the committed Observatory OpenAPI snapshot used by the API Reference.

The Observatory backend serves a *public* OpenAPI document that contains only the
endpoints available to non-team users (the same surface the `coworld` and
`softmax` CLIs use). This script downloads that public spec, adds `servers` so
Mintlify's API playground can send real requests, and re-tags each operation into
curated resource groups so the generated navigation reads well.

Usage:
    python scripts/update-observatory-openapi.py
    python scripts/update-observatory-openapi.py --source /path/to/openapi.json
    python scripts/update-observatory-openapi.py --source https://softmax.com/api/observatory/openapi.json

Source of truth (regenerate against these, never hand-edit the output):
    https://softmax.com/api/observatory/openapi.json
    https://api.observatory.softmax-research.net/openapi.json
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

DEFAULT_SOURCE = "https://softmax.com/api/observatory/openapi.json"
OUTPUT = Path(__file__).resolve().parent.parent / "api-reference" / "observatory-openapi.json"

SERVERS = [
    {"url": "https://softmax.com/api/observatory", "description": "softmax.com (data API under /observatory)"},
    {"url": "https://api.observatory.softmax-research.net", "description": "Observatory host (endpoints at root)"},
]

# Ordered (prefix, group) rules. First match wins, so list specific paths first.
# `group` is the curated tag; display names come from GROUP_META below.
RULES: list[tuple[str, str]] = [
    ("/whoami", "auth"),
    ("/players", "players"),
    ("/v2/players", "players"),
    ("/stats/policies", "policies"),
    ("/stats/policy-versions", "policies"),
    ("/stats/policy-secret-envs", "policies"),
    ("/stats/episodes", "policies"),
    ("/v2/policy-versions", "policies"),
    ("/v2/container_images", "container-images"),
    ("/v2/games", "games-catalog"),
    ("/v2/schema", "games-catalog"),
    ("/v2/participate", "games-catalog"),
    ("/v2/leagues", "leagues"),
    ("/v2/league-submissions", "submissions"),
    ("/v2/league-policy-memberships", "memberships"),
    ("/v2/policy-membership-events", "memberships"),
    ("/v2/divisions", "divisions"),
    ("/v2/rounds", "rounds"),
    ("/v2/competition-events", "competition-events"),
    ("/v2/experience-requests", "experience-requests"),
    ("/v2/episode-requests", "episodes"),
    ("/v2/episodes", "episodes"),
    ("/episodes", "episodes"),
    ("/v2/coworlds", "coworlds"),
    ("/v2/reporters", "reporters"),
    ("/v2/posts", "posts"),
]

# Curated group order + human labels + descriptions.
GROUP_META: list[tuple[str, str, str]] = [
    ("auth", "Authentication", "Identity and token checks."),
    ("games-catalog", "Games & catalog", "Discover games, the participation catalog, and schemas."),
    ("leagues", "Leagues", "List leagues and their division ladders."),
    ("divisions", "Divisions & leaderboards", "Divisions, leaderboards, pairings, and standings."),
    ("rounds", "Rounds", "League rounds and commissioner reports."),
    ("submissions", "League submissions", "Submit a policy version to a league."),
    ("memberships", "Memberships", "Active league memberships and their lifecycle events."),
    ("policies", "Policies & uploads", "Upload policy images, register versions, and manage tags/secrets."),
    ("container-images", "Container images", "Register and complete container image uploads."),
    ("episodes", "Episodes & results", "Episode requests, results, artifacts, replays, and logs."),
    ("experience-requests", "Experience requests", "Create and inspect hosted XP/evaluation requests."),
    ("competition-events", "Competition events", "Scheduled and historical competition events."),
    ("coworlds", "Coworlds", "Coworld manifests, certification, secrets, and hosted play sessions."),
    ("reporters", "Reporters", "Reporter registration, runs, outputs, and subscriptions."),
    ("posts", "Feed & posts", "The Observatory social feed."),
    ("players", "Players", "Player identities, credentials, sessions, and avatars."),
]
LABELS = {g: label for g, label, _ in GROUP_META}
DESCRIPTIONS = {g: desc for g, _, desc in GROUP_META}
HTTP_METHODS = {"get", "post", "put", "delete", "patch", "options", "head"}


def group_for(path: str) -> str:
    for prefix, group in RULES:
        if path == prefix or path.startswith(prefix + "/") or path.startswith(prefix + "?"):
            return group
    return "other"


def load(source: str) -> dict:
    if source.startswith("http://") or source.startswith("https://"):
        request = urllib.request.Request(source, headers={"User-Agent": "softmax-docs-openapi-refresh"})
        with urllib.request.urlopen(request, timeout=60) as resp:  # noqa: S310 (trusted host)
            return json.loads(resp.read().decode("utf-8"))
    return json.loads(Path(source).read_text())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=DEFAULT_SOURCE, help="URL or path to the public OpenAPI document.")
    parser.add_argument("--output", default=str(OUTPUT), help="Where to write the transformed snapshot.")
    args = parser.parse_args()

    spec = load(args.source)
    spec["servers"] = SERVERS

    used: set[str] = set()
    for path, operations in spec.get("paths", {}).items():
        group = group_for(path)
        for method, detail in operations.items():
            if method.lower() in HTTP_METHODS and isinstance(detail, dict):
                detail["tags"] = [group]
                used.add(group)

    ordered = [g for g, _, _ in GROUP_META if g in used]
    ordered += sorted(used - set(ordered))
    spec["tags"] = [
        {"name": g, "description": DESCRIPTIONS.get(g, ""), "x-group": LABELS.get(g, g)} for g in ordered
    ]

    out = Path(args.output)
    out.write_text(json.dumps(spec, indent=2) + "\n")
    op_count = sum(1 for ops in spec["paths"].values() for m in ops if m.lower() in HTTP_METHODS)
    print(f"Wrote {out} ({len(spec['paths'])} paths, {op_count} operations, {len(ordered)} groups)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
