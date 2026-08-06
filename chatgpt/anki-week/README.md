# anki-week — ChatGPT Custom GPT

A ChatGPT port of the **anki-week** Claude Code skill. It turns a med-school week's lecture materials
into the right **AnKing Step Deck** cards to study — by finding the right cards by tag, unsuspending +
tagging them, building a filtered deck per lecture, and coverage-auditing every concept the lecture
teaches (adding a few custom cards where AnKing has none).

**Materials-first.** The calendar is only an *index* telling you which lectures exist; the **lecture
materials are read first** and define the scope. Each lecture's concept inventory is a **coverage
floor** — the deck may go bigger than the materials, never smaller.

Because ChatGPT can't reach the Anki desktop app on your Mac (it runs in the cloud; Anki's add-on
listens on `localhost`), this port runs in **advisory mode** by default: it produces the exact Anki
search queries, unsuspend/tag lists, filtered-deck definitions, and custom cards for you to run in
Anki. A live-Actions mode is available if you expose Anki behind an HTTPS endpoint (see
[Optional: live Actions](#optional-live-actions-mode)).

> This is the same methodology as the Claude Code plugin in
> [`plugins/anki-week/`](../../plugins/anki-week/) — just repackaged for ChatGPT. If you use Claude
> Code, that version can drive Anki directly and is the fuller experience.

---

## What's in this folder

| File | Use |
|---|---|
| `instructions.md` | Paste into the GPT's **Instructions** field. Identity, hard gates, invariants, and pointers into the manual. Deliberately short. |
| `knowledge/anki-week-manual.md` | **Upload to Knowledge.** The authoritative ruleset, written for ChatGPT. |
| `knowledge/tag-map.md` | **Upload to Knowledge.** *Your* growing brain: course concept → AnKing leaf tag. Starts near-empty. |
| `knowledge/synonym-map.md` | **Upload to Knowledge.** *Your* alias list: slide word → AnKing word. Starts near-empty. |
| `conversation-starters.md` | The four starter chips + alternates. |
| `openapi.yaml` | **Optional** Actions schema for live mode. Skip it for advisory mode. |
| `README.md` | This setup guide. |

Upload **all three** Knowledge files. The manual is fixed — it's the method, and you never edit it. The
other two are yours, they start almost empty, and they're what turns this from a generic tool into
*your course's* tool. See [Growing your map](#growing-your-map-the-memory-loop) below.

### Why there's a manual (and why Instructions is short)

ChatGPT splits a GPT's brain into two places that behave very differently:

- **Instructions** — *always* in context, hard **8,000-character** limit. Reliable, but small.
- **Knowledge** — effectively unlimited, but **retrieval-based**: the GPT pulls chunks only when it
  decides to look. Not guaranteed for "always apply this rule."

Cramming every rule into Instructions hits the ceiling fast (this file was once at **7,961/8,000** and
real rules were being cut to fit new ones). So the split is:

- **Instructions** keeps only what must hold *without* a retrieval call — identity, the Stage-3 gate,
  the coverage floor, the Selection Protocol (*scope = tags ∩ slides*) in one line, and the resource
  rules — plus an explicit table telling the GPT **which manual section to open before each action**.
- **`anki-week-manual.md`** carries the full detail: tag roots, altitude numbers, tier rules, both
  audits, deck/tag/custom-card mechanics, pacing, undo, edge cases.

**Add new detail to the manual, not to Instructions.** Instructions now sits around 5,400/8,000, so it
has room to grow — but the manual is the right home for anything that isn't a non-negotiable.

> **Do not upload the Claude Code `config.md` / `playbook.md` as Knowledge.** They were the old
> approach and are actively harmful here: they contain **superseded dated principle blocks** (one says
> tier-1-only, a later one says 1+2) plus git/Cowork/localhost-MCP transport instructions that don't
> apply to ChatGPT. Retrieval can surface a rule that was overturned. The manual replaces both.

---

## Prerequisites

- A **ChatGPT plan that can create GPTs** (Plus, Pro, Team, or Enterprise). Free tier can't build GPTs.
- **Anki desktop** with the **AnKing Step Deck** loaded and the **Anki MCP Server** add-on
  (AnkiWeb code `124672614`) installed — needed to *run* the plans the GPT gives you, and required for
  live mode.

---

## Setup (advisory mode — recommended)

1. **Open the GPT builder.** ChatGPT → left sidebar → **GPTs** → **+ Create**, then click the
   **Configure** tab (skip the chat-based "Create" flow).

2. **Name & description.**
   - Name: `anki-week`
   - Description: `Turns a week's med-school lectures into the right AnKing Step Deck cards — maps objectives to AnKing tags, gives you the unsuspend/tag/filtered-deck plan, and coverage-audits every objective.`

3. **Instructions.** Open `instructions.md`, copy everything from the `## What you are` heading to the
   end of the file, and paste it into the **Instructions** box (~6.5k characters, under the 8k limit).

4. **Knowledge — upload all three.** Drag these into the **Knowledge** uploader:
   - **`knowledge/anki-week-manual.md`** — the authoritative ruleset. Fixed; you never edit it.
   - **`knowledge/tag-map.md`** — *yours.* Course concept → AnKing leaf tag. Ships nearly empty.
   - **`knowledge/synonym-map.md`** — *yours.* Slide word → AnKing word. Ships nearly empty, and is the
     one that carries coverage from ~90% toward ~95% as it grows.

   The last two starting empty is normal — they fill in as you build weeks, via the
   [memory loop](#growing-your-map-the-memory-loop). Each has example rows at the bottom showing the
   format; delete those once you have your own.

   A `run-log.md` is *optional* and you create it yourself if you want the GPT to have precedent from
   past builds. Long history retrieves poorly, so skip it if answers get noisy.

   > Use the copies under **`chatgpt/anki-week/knowledge/`** — not the ones under
   > `plugins/anki-week/…/data/`. Those belong to the Claude Code plugin and hold *its author's* course
   > vocabulary, which isn't yours.

   > **Do NOT upload `config.md` or `playbook.md`** — see *Why there's a manual* above. They carry
   > superseded rules and CLI-only transport instructions; the manual supersedes both.

5. **Conversation starters.** Copy the four from `conversation-starters.md` into the four slots.

6. **Capabilities.** Turn **off** DALL·E and Canvas (not needed). Leave **Code Interpreter & Data
   Analysis** *on* if you want the GPT to parse uploaded PPTX/PDF slide text; otherwise off. Web
   Search: optional (off is fine — the GPT works from what you give it).

7. **Save.** Top-right **Create** → **Only me**. (Keep it private — the knowledge files contain your
   personal study history.)

That's it. Start a chat, click a starter, and paste your week's lecture list + objectives + slides.

---

## Using it each week

The advisory flow mirrors the skill's stages:

1. Give it the **week's lecture list** (from your Calendar) so it knows what to read, then **the
   materials themselves** — paste the slide text or upload the PPTX/PDF. Add the **syllabus
   objectives** as a cross-check. It reads the materials and builds a **concept inventory** per
   lecture; that inventory is the coverage floor.
2. It maps each lecture's concepts → **AnKing leaf tags** (Boards & Beyond first), checking
   `tag-map.md` for known mappings, and **proposes** a build: concepts × candidate leaves, counts,
   sample cards, pacing, and the **uncovered-concept list**.
3. You **approve / trim**. Then it hands you the exact Anki steps: the `find_notes` queries, the cards
   to unsuspend, the `Sched::…` tags to add, the filtered-deck definition, and any **custom cards** to
   author (with the required `Back Extra:""` for Cloze).
4. Run them in Anki, then **sync**.
5. It gives you a **run summary**, the one-line undo (`re-suspend tag:Sched::<week>::*`), and an
   **`APPEND BLOCK`** of new rows for `tag-map.md` / `synonym-map.md`. Paste those in and re-upload —
   see [Growing your map](#growing-your-map-the-memory-loop).

### Growing your map (the memory loop)

**A Custom GPT has no persistent memory of its own.** Knowledge is a **static upload**, not a live repo,
and the GPT *cannot* edit it. Nothing it learns in a chat survives into the next one unless **you** carry
it across. So the memory is a loop you run — it takes about thirty seconds, and it's the difference
between a generic tool and one that knows your course:

1. **Every build ends with an `APPEND BLOCK`** — a fenced block of ready-to-paste table rows. New
   concept→leaf mappings go to `tag-map.md`; new aliases go to `synonym-map.md`. The GPT is instructed to
   emit this every run, and to say so explicitly when a run turned up nothing new.
2. **Paste the rows** into your local copies of those two files, under the *Your mappings* / *Your
   aliases* tables.
3. **Re-upload both files** in Configure ▸ Knowledge — delete the old copy, add the new one. Replacing
   matters; adding a second copy leaves the stale one retrievable.
4. Next run the GPT checks `tag-map.md` **first**, and expands entities through `synonym-map.md` before
   intersecting. What you saved is now permanent.

Skip step 3 and the work is lost — the GPT re-derives the same mapping next week and may land at a
different altitude. **The aliases are the highest-value rows**: they're what carries coverage from ~90%
toward ~95%, because a missing alias shows up as a *phantom* gap that looks like a missing resource but
isn't. Confirmed **Sketchy organism → leaf** mappings are the next most expensive to rediscover.

Also worth knowing:

- **Each conversation starts cold.** Give it the week's materials every time; don't assume it remembers
  last week's build.
- **Editing the files by hand is fine and encouraged** — they're plain Markdown tables. Delete the
  example rows once you have your own.
- **Re-paste `instructions.md` whenever it changes.** An existing GPT keeps the old text forever
  otherwise. If it ever ignores a rule you know is in the manual, check this first.

---

## Optional: live Actions mode

To let the GPT drive Anki directly instead of handing you commands:

1. **Expose Anki over HTTPS.** ChatGPT Actions call a public HTTPS URL from OpenAI's cloud and
   **cannot reach `localhost`**, and the add-on speaks **MCP (JSON-RPC)**, not REST. So you need a
   small **HTTPS → Anki shim** (a reverse proxy / bridge in front of the add-on at
   `127.0.0.1:3141`, or the add-on's optional `wss://tunnel.ankimcp.ai` fronted by an HTTPS-to-MCP
   bridge) that implements the REST shape in `openapi.yaml`. **Only expose it with authentication** —
   it can modify your collection.
2. **Add the Action.** GPT builder → **Configure** ▸ **Actions** ▸ **Create new action** ▸ paste
   `openapi.yaml`. Set `servers[0].url` to your endpoint.
3. **Auth.** Set **Authentication** to **API Key** (header) and paste the key your shim expects. Never
   run the shim open to the internet.
4. The GPT will now call `find_notes` / `card_management` / `tag_management` / `filtered_deck` /
   `add_note` / `sync` itself — but it **still proposes and waits for your approval** before any write,
   per the instructions.

If you haven't set this up, **remove the Action** and stay in advisory mode — everything still works,
you just run the final steps in Anki yourself.

---

## Notes & limitations

- **No new/day setter.** Neither the add-on nor these Actions can set a deck's New-cards/day. The GPT
  reports the recommended number; set it once in **Anki ▸ AnKing Step Deck ▸ Options**.
- **Scope = AnKing Step Deck, Step 1 tags (`#AK_Step1_v12`).** Anatomy decks and `#AK_Step2_v12` are
  out of scope, same as the source skill.
- **Privacy.** Keep the GPT **private** — the uploaded run-log/tag-map are your personal study record.
- **No `study-week` handoff.** The Claude Code skill ends by invoking the sibling `study-week` skill to
  schedule the week. That's a separate tool; here the GPT will remind you to run study-week (or your
  calendar planner) after the cards are built.
