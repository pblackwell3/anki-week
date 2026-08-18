# Run log

One entry per weekly build: week, block, date, leaves + counts, new/day applied, source inputs,
the deferred cross-system sets, and the one-line undo. Appended by the skill at Stage 5.

## Entry format

```
### <YYYY-Www> · block: <current_block> · built <YYYY-MM-DD>
materials: <files read>            inventory: <n> concepts        coverage: <covered>/<total>
IM<##> <Lecture>  →  <leaf tag(s)>   core <n> · bridge <n> · custom <n>   (new/day <n>)
…
deferred (cross-system, NOT built — offer these when that block starts):
  | system | entity | query | notes |
  |---|---|---|---|
  | Endo | Type IV hypersensitivity | tag:#AK_Step1_v12::^Systems::Endo::* "hypersensitivity" | 22 |
undo: re-suspend tag:Sched::<Class>::M<n>-W<nn>::*
```

**The deferred table is the point of deferring rather than dropping** — Stage 5 step 4 replays the rows
whose `system` matches the new `current_block`, so nothing gated out is ever lost, only postponed.

<!-- Entries appended below, newest last. (Starts empty.) -->
