# anki-week + study-week

Two Claude Code skills for medical students:

- **anki-week** — turns a week's lectures into the right **AnKing Step Deck** cards to study, by
  unsuspending + tagging cards that already exist (it never creates cards from scratch) and
  building one filtered deck per lecture.
- **study-week** — plans the week's study *time* around those decks: maps each lecture to its
  study video(s), reserves daily Anki-review time, and stages pre-lecture blocks on your calendar
  as proposed events.

## Install

In Claude Code:

```
/plugin marketplace add pblackwell3/anki-week
/plugin install anki-week@phillo-study
/plugin install study-week@phillo-study
```

Then run first-time setup — just tell Claude: **"set up anki-week."** It walks you through
Anki + the MCP add-on, detects your deck, asks which study resource is your backbone, and fills
in your config. A readable version of that walkthrough is in [`docs/SETUP.md`](docs/SETUP.md).

To update later: `/plugin marketplace update phillo-study`.

## What you need

| Requirement | Why |
|---|---|
| Claude subscription (Pro+) with Claude Code / desktop | Runs the skills |
| **Anki desktop** (Mac/Windows) | The skills drive Anki locally |
| The **AnKing Step Deck**, already imported | The card library these operate on |
| Node.js (LTS) | A tiny bridge (`mcp-remote`) connects Claude to Anki |
| Your lecture slides + a syllabus | Slides + objectives tell the skill what to build |

## Notes

Not affiliated with AnKing, AnkiHub, or Boards & Beyond. These skills **redistribute no card
content** — they only switch on cards in the AnKing deck you already own, and read a syllabus you
already have. Bring your own deck and resources.

MIT licensed — see [`LICENSE`](LICENSE).
