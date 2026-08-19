# Everyday Prompts

Anki must be **open** every time you use these skills — the connection only exists while the
desktop app is running. New cards/day is set manually in Anki (**your deck ▸ Options ▸ New
cards/day**); the MCP can't set it for you — `anki-week` will tell you the number to enter.

**Run these in [Claude Cowork](https://claude.ai/cowork) when you can.** Cowork has a browser, so it
logs into Blackboard and pulls each week's lecture slides down for you — and both skills scope from
those slides, not the lecture title. In plain Claude Code they still work, but you have to download
every lecture's materials into `course_folder` yourself first. The `anki` connector installed during
setup is already live in Cowork; there's nothing extra to set up.

Paste any of these into Claude (tweak the bracketed parts).

## Build & plan

- *"Build this week's Anki from my lecture materials."* (or just `/anki-week`)
- *"Plan my study week."* (or just `/study-week`)

## Pacing

- *"Recompute my new/day so I finish this week's cards by Saturday."*
- *"That's too many new cards a day — cap it at [15] and tell me what spills over."*

## Scope / yield

> Your high-yield filter is chosen **once during setup** (recommended: **1+2**) and saved in
> `config.md`. The skill just uses it silently every run — it won't keep asking. Use the prompts
> below only when you want to *change* it.

- **Reconsider / change your saved filter (paste this):**
  > *"Show me my current yield-filter setting, then explain the tier options and recommend one,
  > and update `config.md` to whatever I pick:*
  > - *Tier 1 only (High-Yield) — smallest, most board-critical set*
  > - ***Tiers 1 + 2 (High-Yield + Relatively High-Yield) — recommended balance of coverage vs. volume***
  > - *Tiers 1 + 2 + 3 (adds High-Yield-Temporary) — broader, but the least-vetted tier*
  > - *All tiers (everything on-objective, including low-yield/unrated) — most complete, most cards*
  > *Also remind me that foundational/definitional lectures auto-include lower tiers regardless,
  > so the basics never get dropped."*
- *"Set my yield filter to [1+2] from now on."*  ·  *"Turn the filter off for this run — everything on-objective."*
- *"This is a foundational lecture — include the basic/definitional cards even if they're low-yield."*
- *"Only build lectures [3 and 5] this week, hold the rest."*

## Custom cards & coverage

- *"Audit coverage for [lecture] — which objectives have no card yet?"*
- *"Make a cloze card for this exact definition the professor gave: [paste it]. Tag it to [lecture]."*
- *"Add custom cards for the professor's named list: [paste the list]."*

## Exam cram

- *"Build me one filtered deck combining all lectures tagged for [exam/block] for a cram session."*
- *"Make a filtered deck of just the cards I've been failing in [lecture]."*

## Block scope (cross-system bleed)

- *"I'm in the [MSK] block now — update `current_block` before you build."*
- *"This deck pulled the whole pathology of [disease] just because the lecture mentioned [mechanism]. Gate it to my block and defer the rest."*
- *"Show me the system split for [lecture]: what's in-block, what's a bridge card, what got deferred."*
- *"I'm starting the [Endo] block — pull the sets you deferred for Endo in earlier weeks."*
- *"Don't cut the [receptor] map — the professor taught the whole table; only defer the disease management."*
- *"Which cards in [block]'s decks aren't actually [block] cards?"* (the bleed check)

## Reconcile / fix

- *"The slides for [lecture] just dropped — reconcile that deck against them and flip it to Final."*
- *"This deck has board tangents the lecture didn't cover — trim [topic] back out."*
- *"Re-run [lecture]; I think it got mapped to the wrong subject."*

## Connector / surface

- *"The `anki` connector is missing — install it into my Claude Desktop config and tell me to restart."*
- *"Show me what's in my `claude_desktop_config.json` right now, then add the `anki` server without
  touching my other MCP servers."*
- *"I'm in Claude Code — what am I giving up by not using Cowork this week?"*

## Housekeeping

- *"List every custom card I've added (tag `Sched::custom`)."*
- *"What did I unsuspend last week, and how do I undo it?"*
- *"Undo this week — re-suspend everything tagged `Sched::<Course>::<Week>`."*
