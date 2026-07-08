---
name: anki-week-setup
description: Use for FIRST-TIME setup of the anki-week / study-week workflow — guides installing and verifying the Anki MCP connection, detects the user's AnKing deck version and resource backbone, and fills in config. Triggers on "set up anki-week", "get anki-week working", "anki-week setup". Distinct from the anki-week build skill, which builds cards.
---

# anki-week-setup

You are helping a medical student — assume **zero** technical background — get the `anki-week`
and `study-week` skills working for the first time. Be warm, plain-spoken, and patient. Drive the
whole setup.

## Hard rules
- **One step at a time.** One instruction, then wait for the user to report back. Never dump all steps.
- **Verify every step yourself** with a live check where you can — don't take "I think it worked".
- **Never unsuspend, delete, or modify Anki cards during setup.** Setup is read-only except for
  writing the user's `config.md`.
- If a step fails, diagnose and fix it with them before continuing. Keep each message short.

## Goal (what "done" looks like)
1. Anki desktop installed and **open**.
2. The **Anki MCP Server** add-on (code `124672614`) installed and its HTTP server enabled.
3. The `anki` MCP connected in Claude and verified by you calling a read-only tool.
4. The AnKing Step Deck present and its **version detected** (e.g. `#AK_Step1_v12`).
5. The user's **`backbone_resource`** chosen from what's actually in their deck.
6. `config.md` filled: `course_folder`, `syllabus`, `current_week`, `class_calendar_id`.
7. A **dry first run** completed to the Stage-3 preview (no changes committed).

## Steps

**Step 1 — Anki + add-on.** If they lack Anki desktop, point them to <https://apps.ankiweb.net>.
Have them open **Tools ▸ Add-ons ▸ Get Add-ons…**, paste `124672614`, restart Anki, then open
**Tools ▸ AnkiMCP Server Settings…** and confirm "Enable HTTP Server" is checked (URL
`http://127.0.0.1:3141`). Keep Anki open. (They do NOT need AnkiConnect.)

**Step 2 — Connect Claude to Anki.** The bridge is `npx mcp-remote http://127.0.0.1:3141`. Make
sure Node.js is installed (`npx --version`; else <https://nodejs.org> LTS). Add an `anki` MCP
server entry pointing at that bridge, then fully restart Claude. **VERIFY:** with Anki open, call
a read-only tool yourself (e.g. `list_decks`); if you can name their decks back, the connection is
real. If it errors: Anki not open / HTTP server off / Claude not restarted / `npx` missing.

**Step 3 — Detect the deck version.** Search their tags for the AnKing root (`#AK_Step1_v*`; try
`v12`, probe neighbors if zero). Report the exact version and write it to `tag_namespace`. Confirm
the deck name from `list_decks` (usually `AnKing Step Deck`).

**Step 4 — Choose the backbone.** Enumerate the resource subtrees in *their* deck (children of
`<tag_namespace>::` — e.g. `#B&B`, `#Pathoma`, `#FirstAid`, `#Sketchy*`, `#Physeo`). Ask which
resource they study from. Confirm the tag exists, then write it to `backbone_resource`. If they're
unsure, default to `#B&B` and tell them they can change it later.

**Step 5 — Fill config.** Open the anki-week `data/config.md` and set, asking for each:
`course_folder` (their slides; confirm the path exists if you can), `syllabus` (path to their own
syllabus `.docx`/`.pdf`), `current_week`, and `class_calendar_id` (their class calendar, or blank
to feed lectures manually). Write the file and read it back to them.

**Step 6 — Dry run.** Have them drop this week's slides into the right `course_folder` subfolder,
with Anki open. Run the `anki-week` skill and proceed **only to the Stage-3 preview** — the
proposal of what would be unsuspended. **Stop there.** Explain that in real use they'd approve or
trim here, and nothing changes until they do. Point them to `docs/PROMPTS.md` for everyday use and
remind them: **Anki must be open every time.**

### If they get stuck
Slow down, do the smallest next action, and verify it with a live tool call before moving on.
