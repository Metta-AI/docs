# Playbook: add or update a docs page

Agent procedure for adding or editing a page on **docs.softmax.com**
(`metta-ai/docs`). This mirrors the human-facing page
[`playbooks/add-docs.mdx`](./add-docs.mdx) — keep the two in sync, and keep both
aligned with the reusable Devin Playbook for this repo. If you change the
workflow in one, update all three.

## When to use

Use this when asked to add a new documentation page, edit an existing page, or
restructure navigation for `metta-ai/docs`.

## Procedure

1. **Clone the repo.**
   ```bash
   git clone https://github.com/metta-ai/docs.git
   cd docs
   ```

2. **Read the conventions.** Read `AGENTS.md` (terminology, layout, content
   boundaries, style). Respect the **platform-vs-game boundary**: platform
   participation (auth, upload, submission, standings, replays, hosted APIs) goes
   in the tracks (`build-a-player/`, `build-a-coworld/`) or `api-reference/`;
   game-specific rules/strategy go under `games/<game>/`.

3. **Add or edit the `.mdx` file** in the correct section directory. Every page
   needs YAML frontmatter:
   ```mdx
   ---
   title: "Page title"
   description: "One-sentence summary."
   ---
   ```
   Do not invent API contracts or source content. Adapt from the source repos
   listed in `AGENTS.md` and mark genuinely-missing details with a clear `TODO`.

4. **Register the page in `docs.json`.** Add the page path (without `.mdx`) to
   the correct `group` inside the correct `tab` under `navigation.tabs`. A page
   not listed in `docs.json` will not appear in the sidebar.

5. **Preview and validate locally.**
   ```bash
   npm i -g mint       # once
   mint dev            # serves http://localhost:3000
   mint broken-links   # validate links
   ```
   Confirm the page renders, appears in the nav, and has no broken links.

6. **Open a PR.**
   ```bash
   git checkout -b docs/<short-name>
   git add <files>
   git commit -m "<what changed>"
   git push -u origin docs/<short-name>
   ```
   Open a PR against the default branch. After merge, the change deploys to
   `docs.softmax.com` automatically — verify on the live site.

## Checklist

- [ ] Page has `title` + `description` frontmatter.
- [ ] Page is in the right section directory (platform vs. game boundary respected).
- [ ] Page path is registered in `docs.json` navigation.
- [ ] `mint dev` renders the page and it appears in the nav.
- [ ] `mint broken-links` passes.
- [ ] PR opened against the default branch.
