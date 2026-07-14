# Documentation project instructions

## About this project

- This is the documentation site for **[docs.softmax.com](https://docs.softmax.com)**, built on [Mintlify](https://mintlify.com).
- It is an **API guide + playbooks** that onboard users and agents into the "Softmax universe" — building players for Coworlds and turning games into Coworlds.
- Pages are **MDX** files with YAML frontmatter.
- Site metadata and **navigation** live in `docs.json`.
- Changes deploy to `docs.softmax.com` automatically after merge to the default branch.

## Terminology

- **Coworld** — a packaged, league-runnable game (game + players + roles + manifest). Not "environment".
- **Player / policy** — a Docker image that connects to a game, plays it, and exits. Prefer "policy" for an uploaded/versioned artifact, "player" for the general role.
- **Game** — the authority that defines rules, protocol, results, and replay.
- **Observatory** — the hosted platform/API (auth, players, submissions, standings, replays).
- **Crewrift** — the canonical worked-example Coworld referenced throughout.
- Use `coworld` (lowercase, code font) for the CLI, "Coworld" (capitalized) for the concept.

## Repository layout

```text
docs.json          # Mintlify config: metadata + navigation (tabs → groups → pages)
index.mdx          # Welcome / landing page
universe/          # What a Coworld is; roles and artifacts
build-a-player/    # "Build a Player" playbook track
build-a-coworld/   # "Build a Coworld" playbook track
api-reference/     # coworld CLI + Observatory HTTP API
playbooks/         # Repeatable procedures (incl. how to add docs)
games/crewrift/    # Game-specific rules and strategy for Crewrift
playbooks/add-doc-page.md  # Agent procedure for adding/editing a page (mirrors playbooks/add-docs.mdx)
```

## Adding or editing a page

Follow `playbooks/add-doc-page.md` — the same steps the human-facing
`playbooks/add-docs.mdx` page documents:

1. Add/edit the `.mdx` file in the correct section directory (with frontmatter).
2. Register its path (no `.mdx` extension) in the right `group`/`tab` in `docs.json`.
3. Preview locally: `npm i -g mint` then `mint dev` (http://localhost:3000); run `mint broken-links`.
4. Open a PR against the default branch.

## Content boundaries

- **Platform vs. game separation is mandatory.** Platform participation (auth, upload, submission, standings, replays, hosted APIs) belongs in the tracks and `api-reference/`. Game-specific rules/strategy belong under `games/<game>/`. Do not mix them.
- **Do not invent** API contracts, CLI flags, or source content. Adapt from the source repos below and mark genuinely-missing details with a clear `TODO`.
- Confirm CLI flags with `coworld --help` / `coworld <cmd> --help` and API schemas with the Observatory `openapi.json` rather than trusting copied values (they drift).

## Source repos (content sourcing)

- `Metta-AI/metta` — `packages/coworld/` (`README.md`, `COOKBOOK.md`, `AGENTS.md`, `src/coworld/docs/`), `packages/softmax-cli/`.
- `Metta-AI/players` — `docs/coworld-integration-guide.md`, `docs/coworld-player-packaging.md`, the Player SDK, and `players/crewrift/crewborg/AGENTS.md`.
- `Metta-AI/optimizer-agent` — `skills/seed-a-new-policy/`, `skills/coworld-operations/`, and the optimizer `AGENTS.md`.
- `Metta-AI/coworld-crewrift` — the running example (README + `coworld_manifest.json`).

## Style preferences

- Use active voice and second person ("you").
- Keep sentences concise — one idea per sentence.
- Use sentence case for headings.
- Bold for UI elements: Click **Settings**.
- Code formatting for file names, commands, paths, and code references.
- Prefer Mintlify components (`<Card>`, `<Steps>`, `<Note>`, `<Warning>`, `<ParamField>`) already used across the site.
