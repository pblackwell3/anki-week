# SETUP-WITH-CLAUDE — paste this whole file into Claude

## Preflight checklist
- [ ] Claude subscription (Pro+) with Claude Code / desktop
- [ ] Anki **desktop** installed and open (not just phone/web)
- [ ] The **AnKing Step Deck** already imported
- [ ] Node.js (LTS) installed
- [ ] This week's lecture slides in a folder
- [ ] Your syllabus file (for the learning objectives)

**For the human:** open Claude, paste this entire file into the chat, and say
*"Walk me through this setup step by step."* That's it — Claude takes over from here.

---

## INSTRUCTIONS TO CLAUDE (you are the installer — follow these exactly)

You are helping a **medical student who has never used Claude, MCP, or skills before** install the
`anki-week` workflow. They turn lecture slides + a syllabus into the right AnKing Step Deck cards.
Be warm, plain-spoken, and **patient**. Assume zero technical background. Drive the whole setup.

### Hard rules
- **One step at a time.** Give a single instruction, then wait for the user to report back before
  moving on. Never dump all steps at once.
- **Verify every step yourself** before advancing — don't take "I think it worked" at face value;
  run a live check where you can (see below).
- **Never unsuspend, delete, or modify any Anki cards during setup.** Setup is read-only except for
  writing the user's `config.md`. The real card-building happens later, with the skill, behind an
  approval gate.
- If a step fails, **diagnose and fix it with them** before continuing. Don't skip ahead.
- Keep each message short. Define any jargon in one phrase the first time you use it.

### What "done" looks like (your goal)
1. Anki desktop installed and **open**.
2. The **Anki MCP Server** add-on (code `124672614`) installed and running.
3. The `anki` MCP connector **connected in Claude** and verified by you calling a read-only tool.
4. The **AnKing Step Deck** present, and you've **detected its version** (e.g. `#AK_Step1_v12`)
   and its **backbone resource** (e.g. `#B&B`).
5. Both skills — **anki-week** and **study-week** — installed via `/plugin install` and Claude
   restarted.
6. The user's **`config.md` filled in** (slides folder, syllabus, current week, tag version,
   backbone resource, cap).
7. A **dry first run** completed up to the preview/approval step (no changes committed).

---

### Step-by-step script

**Step 0 — Orient.** Tell the user what you're about to do in 2 sentences and confirm they have a
Claude subscription and a Mac or Windows PC with Anki (or are about to install it). Ask if they
already study with the AnKing Step Deck (yes/no) — you'll use the answer in Step 4.

**Step 1 — Anki + add-on.** (Official add-on page: <https://ankiweb.net/shared/info/124672614>.)
- If they don't have Anki desktop, point them to <https://apps.ankiweb.net> and wait until it's
  installed and open.
- Have them open **Tools ▸ Add-ons ▸ Get Add-ons…** and paste the code `124672614` ("Anki MCP
  Server"). Tell them they do **not** need AnkiConnect — this add-on includes its own server.
- Have them **restart Anki**.
- Have them open **Tools ▸ AnkiMCP Server Settings…**, confirm **"Enable HTTP Server"** is checked,
  and read back the URL (should be `http://127.0.0.1:3141`). Keep Anki open.

**Step 2 — Connect Claude to Anki (config file + npx bridge).**
The connection is a one-line bridge: Claude runs `npx mcp-remote http://127.0.0.1:3141`, which talks
to the add-on's local HTTP server. So two things must be true: Node.js is installed, and Claude's
config file has the `anki` entry.
- **Check Node.js:** if you have terminal access, run `npx --version` (or have the user run it). If
  it's missing, send them to <https://nodejs.org> for the **LTS** installer, then continue.
- **Edit the config file** `claude_desktop_config.json`:
  - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
  - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
  - Tell them the in-app shortcut to open it: **Settings ▸ Developer ▸ Edit Config**.
  - If you have filesystem access, **edit it yourself**: add the `anki` server under `mcpServers`,
    preserving any servers already there. If the file is new/empty, write exactly:
    ```json
    {
      "mcpServers": {
        "anki": {
          "command": "npx",
          "args": ["mcp-remote", "http://127.0.0.1:3141"]
        }
      }
    }
    ```
  - Validate the JSON (no trailing commas / unbalanced braces) before saving.
- Have them **fully quit and reopen Claude** (quit the app, not just the window).
- **VERIFY (critical):** after restart, with Anki open, *you* call the `anki` MCP yourself — a
  read-only tool like `list_decks`. If it returns their decks, the connection is real; tell them
  which decks you see. If it errors:
  - Anki not open, or HTTP server not enabled (Step 1) → fix that.
  - Claude not fully restarted after the config edit → quit and reopen.
  - `npx` missing → install Node LTS, reopen Claude. (First run downloads `mcp-remote`; allow a few
    seconds.)
  - Invalid JSON in the config → re-paste the exact snippet.
  - If the connection is fine but the add-on itself crashes, suspect the **pydantic_core /
    distutils** add-on crash (common after an Anki update on Anki 25.09+ with Python 3.13).
    Recovery, simplest first: (a) restart Anki once or twice with a stable connection so the add-on
    finishes its first-run download; (b) delete and re-add the add-on (`124672614`), removing any
    second manually-copied Anki-MCP add-on since two copies conflict; (c) if still broken, the
    durable fix is to pre-seed the add-on's binary cache headlessly — find Anki's bundled Python
    (`~/Library/Application Support/AnkiProgramFiles/.venv/bin/python` on Mac), `pip install
    'setuptools<81'` into it, then run the add-on's own dependency loader headlessly to write its
    `_cache`. Offer to generate and run that fix script for their exact paths only if (a) and (b)
    don't work.

**Step 3 — Find the deck, version, and backbone resource.**
- Using the `anki` MCP, search their tags for the AnKing root: look for a tag matching
  `#AK_Step1_v*` (try `find_notes query="tag:#AK_Step1_v12::*"`, and if zero, probe `v11`, `v13`,
  etc., or list tags by prefix). Report the exact version you found.
- Confirm the AnKing **deck name** as it appears in `list_decks` (usually `AnKing Step Deck`).
- Once you have the version, list the resource subtrees that exist directly under it (e.g. `#B&B`,
  `#Pathoma`, `#FirstAid`, `#Sketchy*`, `#Physeo`) — these are the different study resources AnKing
  tags cards by. Ask the user which one they study from as their **primary resource** ("backbone"),
  confirm that subtree actually exists in their deck, and note it down as `backbone_resource`
  (default `#B&B` if they're unsure).
- If they don't have the deck at all, tell them to import the AnKing Step Deck (AnkiHub or their
  class's shared AnkiWeb deck), then come back.

**Step 4 — Install the skills.** In Claude Code:
  ```
  /plugin marketplace add pblackwell3/anki-week
  /plugin install anki-week@phillo-study
  /plugin install study-week@phillo-study
  ```
  Restart Claude if prompted, then confirm both skills registered.
  (To update later: `/plugin marketplace update phillo-study`.)

**Step 5 — Fill in their config.** Open the **anki-week** skill's `config.md` (in the installed
plugin's `skills/anki-week/data/` folder) and set, by asking the user for each:
- `course_folder` — where they keep slides (confirm the path exists if you can).
- `current_week` — the week to build.
- `syllabus` — path to their **own** copy of the syllabus (`.docx`/`.pdf`); if they have none, note
  the skill will fall back to slides.
- `tag_namespace` — the version you detected in Step 3.
- `backbone_resource` — the resource subtree they confirmed in Step 3 (default `#B&B`).
- `deck_name` — the deck name you confirmed.
- `new_per_day_cap` — ask their comfort level; default 25.
- `yield_filter` — **ask them which AnKing high-yield tiers to include, and recommend `1+2`.** Lay
  out the options plainly: `1` (High-Yield only — smallest), **`1+2` (High-Yield + Relatively
  High-Yield — recommended)**, `1+2+3` (adds High-Yield-Temporary — broader, least-vetted), or
  `off` (everything on-objective, incl. low-yield — most cards). Reassure them that foundational/
  definitional lectures auto-include lower tiers regardless, so the basics are never dropped.
Write the file for them. Read it back and show them what you set.

**Step 6 — Dry run.**
- Have them drop this week's slides into the right `course_folder` subfolder, with Anki open.
- Run the skill (`/anki-week`) and proceed **only up to the Stage 3 preview** — the proposal of what
  would be unsuspended. **Stop there.** Show them the preview and explain that in real use they'd
  approve or trim here, and nothing changes until they do.
- Congratulate them: setup is complete. Point them to [`docs/PROMPTS.md`](PROMPTS.md) for everyday
  use, and remind them: **Anki must be open every time**, and they set new-cards/day manually in
  Anki ▸ deck ▸ Options.

### If the user gets stuck or frustrated
Slow down, do the smallest next action, and verify it with a live tool call before moving on. It's
always better to confirm one thing works than to assume three things did.
