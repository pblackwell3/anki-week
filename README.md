# anki-week + study-week

Three skills for medical students, on **Claude and ChatGPT/Codex**:

- **anki-week** — turns a week's lectures into the right **AnKing Step Deck** cards to study, by
  unsuspending + tagging cards that already exist (it never creates cards from scratch) and
  building one filtered deck per lecture. Scoped to the **body system you're currently in**, so a
  shared mechanism (say Type IV hypersensitivity in an MSK week) doesn't drag in another block's whole
  disease pathology — those cards are deferred and re-offered when you reach that block.
- **practice-exam-builder** — turns the same slides, review materials and professor-posted questions
  into an **interactive NBME/USMLE-style practice exam**: your faculty's question distribution is
  enforced *before* a question is written, every item traces back to a slide, and the scored report
  routes each miss to a video, a card, or a test-taking fix. Ships inside the `anki-week` plugin, and
  it's the one piece here that **needs no Anki connection** — so it runs anywhere, browser ChatGPT
  included.
- **study-week** — plans the week's study *time* around those decks: maps each lecture to its
  study video(s), reserves daily Anki-review time, and puts pre-lecture blocks on your calendar as
  real events you can move or delete yourself. Ships with **two video libraries — Boards & Beyond and
  Med School Bootcamp** (including Anatomy Bootcamp: gross anatomy, neuroanatomy, histology, OMM) — and
  picks the one matching the backbone resource you set during setup, so Bootcamp users get the same
  plan B&B users do. Override any time with `video_library` in study-week's `config.md`.

Using ChatGPT instead of Claude? The same plugins install into Codex — see [Codex / ChatGPT](#codex--chatgpt) below.

## Install

In Claude Code:

```
/plugin marketplace add pblackwell3/anki-week
/plugin install anki-week@phillo-study
/plugin install study-week@phillo-study
```

Then run first-time setup — just tell Claude: **"set up anki-week."** It walks you through
Anki + the MCP add-on, **writes the `anki` connector into your Claude Desktop config for you** (so it
shows up in Claude Chat and Claude Cowork without you editing JSON), detects your deck, asks which
study resource is your backbone, and fills in your config. A readable version of that walkthrough is
in [`docs/SETUP.md`](docs/SETUP.md).

The connector it installs is just this, merged into your existing config (other MCP servers are kept,
and the file is backed up first):

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

If you ever need to (re)install it by hand, run the same script the skill uses:
`node plugins/anki-week/skills/setup/scripts/install-anki-mcp.mjs` (`--dry-run` to preview), then
fully quit and reopen Claude.

To update later: `/plugin marketplace update phillo-study`. If the Anki connector ever goes missing,
`/anki-connect` reinstalls and re-verifies it.

### Codex / ChatGPT

The same plugins carry a `.codex-plugin/` manifest, so Codex can install them from this repo —
clone it, then point Codex at the marketplace file at `.agents/plugins/marketplace.json`.
The skills themselves are the same files; nothing is duplicated per surface. `practice-exam-builder`
detects which host it's on and builds its exam UI in that host's interactive surface — a Claude
Artifact, or the Codex/ChatGPT in-app app surface — off one identical set of instructions.

> **Anki needs to be reachable.** `anki-week` talks to Anki over `127.0.0.1:3141`, so it only
> works where the agent runs on the same machine as Anki — Claude Code, Claude Cowork, or Codex
> locally. ChatGPT in the browser can't reach your Mac's localhost. `study-week` is calendar-driven
> and less affected, and **`practice-exam-builder` doesn't touch Anki at all** — it reads your slides
> and writes JSON, so it's fully usable in browser ChatGPT.

## Use it in Claude Cowork

Set up once anywhere; **do your weekly builds in [Claude Cowork](https://claude.ai/cowork)**. Cowork
has a browser, so it can log into Blackboard with your existing session and **fetch each week's
lecture slides itself** — which is the whole ballgame here, because both skills scope from the actual
slides rather than the lecture title. In plain Claude Code the skills can still build decks and plan
your week, but you have to download every lecture's materials into `course_folder` by hand first, and
a missing file quietly shrinks what gets carded. Same for the practice exam: a slide you never
downloaded is a blueprint area with no source behind it.

The setup step writes the `anki` connector into your Claude Desktop config, so Cowork already has it
— switching costs you nothing. Both skills will nudge you toward Cowork on any run where a browser
would have saved you the download; that's deliberate.

## What you need

| Requirement | Why |
|---|---|
| Claude subscription (Pro+) with Claude Code / desktop, **or** ChatGPT/Codex | Runs the skills |
| Your lecture slides + a syllabus | Slides + objectives tell the skills what to build — the only hard requirement for `practice-exam-builder` |
| **Anki desktop** (Mac/Windows) | `anki-week` drives Anki locally. Not needed for `practice-exam-builder`. |
| The **AnKing Step Deck**, already imported | The card library `anki-week` operates on |
| Node.js (LTS) | A tiny bridge (`mcp-remote`) connects Claude to Anki |

## Building a practice exam

Point it at the block's materials and say what the exam actually is:

> *"Build me a 60-question practice exam for the cardio block — 20 from Dr. Nguyen, 25 from
> Dr. Okafor, 15 from Dr. Patel. Slides and the review deck are in this week's folder, and here are
> the questions the professors posted."*

What it will and won't do:

- **The faculty counts are checked before anything is written.** If they don't sum to the total you
  asked for, it stops and shows you the difference rather than quietly redistributing them.
- **Every question traces to a slide.** A blueprint area your materials don't cover is reported as a
  source gap, not filled in from general knowledge.
- **~80% second- and third-order vignettes**, five choices, one best answer, and distractor
  explanations that name what each wrong option *would* fit and the clue that rules it out here.
- **Timed, Tutor, Weakness Drill and Review Marked** modes; progress is saved after every answer, so
  you can stop mid-exam and resume without the questions reshuffling.
- **The report routes each miss** — knowledge gap to the slide plus a video, forgotten mechanism to
  the cards, misread question to test-taking review — and ranks what's left to study.
- **It never touches Anki.** Card and tag suggestions in the report are suggestions; nothing is
  unsuspended or edited without you approving that specific action.

Exams are written as plain JSON under `<course_folder>/_practice-exams/<exam_id>/` — yours to keep,
diff, or delete. A checker ships with the skill
(`skills/practice-exam-builder/scripts/validate_exam.py`) and runs before an exam opens; it catches
blueprint arithmetic, malformed items, answer-key bias and pattern clues, but it can't tell you a
question is clinically sound — that read is still the skill's, and yours.

## Notes

Not affiliated with AnKing, AnkiHub, Boards & Beyond, or Med School Bootcamp. These skills
**redistribute no card or video content** — the bundled video libraries are catalogs only (titles,
runtimes, and each site's own keyword index, used to decide what to watch and when); they switch on
cards in the AnKing deck you already own and read a syllabus you already have. Bring your own deck and
subscriptions.

MIT licensed — see [`LICENSE`](LICENSE).
