#!/usr/bin/env python3
"""Parse the Boards & Beyond Step-1 checklist PDF into structured JSON.

Usage:
    python3 build-bb-videos.py <checklist.pdf> [out.json]

Text is extracted via macOS PDFKit (osascript/JXA) so no pip deps are needed.

Integrity model: the per-video "(N minutes)" lines are ground truth. The
subject-header totals ("N videos; H hours M minutes") in this checklist are
rollup ESTIMATES and frequently do NOT sum to their own listed videos, so we
do not gate on them. Instead the real self-check is structural: EVERY non-noise
source line must classify as a subject header, a section header, or a video —
zero leftovers — which proves no video was silently dropped. That is fatal if
violated. Header-vs-parsed differences are recorded per subject as
`header_discrepancy` (informational) and printed as warnings.
"""
import json
import re
import subprocess
import sys

JXA = r'''
ObjC.import("Quartz");
function run(argv) {
  const url = $.NSURL.fileURLWithPath(argv[0]);
  const doc = $.PDFDocument.alloc.initWithURL(url);
  let out = [];
  for (let i = 0; i < doc.pageCount; i++) out.push(doc.pageAtIndex(i).string.js);
  return out.join("\n");
}
'''


def parse_duration(s):
    """'1 hour 15 minutes' / '16 hours 14 minutes' / '27 minutes' / '3 hours' -> minutes."""
    h = re.search(r'(\d+)\s*hour', s)
    m = re.search(r'(\d+)\s*minute', s)
    return (int(h.group(1)) * 60 if h else 0) + (int(m.group(1)) if m else 0)


SUBJECT_RE = re.compile(r'^([A-Z][A-Za-z/ &\-]+?)\s*\((\d+)\s*videos?;\s*([^)]+)\)\s*$')
SECTION_RE = re.compile(r'^([IVX]+)\.\s+(.+?)\s*\(([^)]+)\)\s*$')   # "I. General Topics (1 hour 15 minutes)"
VIDEO_RE = re.compile(r'^(.+?)\s*\((\d+)\s*minutes?\)\s*$')


def extract_text(pdf_path):
    p = subprocess.run(["osascript", "-l", "JavaScript", "-e", JXA, pdf_path],
                       capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit(f"PDF extraction failed: {p.stderr}")
    return p.stdout


def parse(text):
    """Return (subjects, leftovers). leftovers = content lines that matched no
    pattern (should be empty; a non-empty list is a fatal parser integrity fail)."""
    subjects = {}
    leftovers = []
    cur_subj = cur_sec = None
    for raw in text.splitlines():
        line = raw.strip().lstrip("□").strip()  # strip leading checkbox box
        if not line or line.startswith("Step 1-Preclinical") or line.startswith("Copyright"):
            continue
        # strip a stray trailing copyright glued to a video line (page-break artifact)
        line = re.split(r'\s*Copyright ©', line)[0].strip()
        if not line:
            continue

        m = SUBJECT_RE.match(line)
        if m:
            cur_subj = m.group(1).strip()
            subjects[cur_subj] = {"declared_videos": int(m.group(2)),
                                  "declared_minutes": parse_duration(m.group(3)),
                                  "sections": {}}
            cur_sec = None
            continue

        m = SECTION_RE.match(line)
        if m and cur_subj:
            cur_sec = m.group(2).strip()
            subjects[cur_subj]["sections"][cur_sec] = {"videos": []}
            continue

        m = VIDEO_RE.match(line)
        if m and cur_subj:
            title = m.group(1).strip()
            if cur_sec is None:
                cur_sec = "General"
                subjects[cur_subj]["sections"].setdefault(cur_sec, {"videos": []})
            subjects[cur_subj]["sections"][cur_sec]["videos"].append(
                {"title": title, "minutes": int(m.group(2))})
            continue

        leftovers.append(line)
    return subjects, leftovers


def annotate_discrepancies(subjects):
    """Record header-vs-parsed differences per subject (informational only)."""
    notes = []
    for subj, d in subjects.items():
        vids = [v for s in d["sections"].values() for v in s["videos"]]
        got_n, got_min = len(vids), sum(v["minutes"] for v in vids)
        disc = {}
        if got_n != d["declared_videos"]:
            disc["videos"] = {"parsed": got_n, "header": d["declared_videos"]}
        if got_min != d["declared_minutes"]:
            disc["minutes"] = {"parsed": got_min, "header": d["declared_minutes"]}
        d["parsed_videos"] = got_n
        d["parsed_minutes"] = got_min
        if disc:
            d["header_discrepancy"] = disc
            notes.append(f"{subj}: header says "
                         f"{d['declared_videos']}v/{d['declared_minutes']}m, "
                         f"listed videos sum to {got_n}v/{got_min}m")
    return notes


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: build-bb-videos.py <checklist.pdf> [out.json]")
    pdf = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "bb-videos.json"
    subjects, leftovers = parse(extract_text(pdf))

    # FATAL: a content line that classified as nothing means a video may be lost.
    if leftovers:
        for l in leftovers:
            print("UNCLASSIFIED LINE:", repr(l), file=sys.stderr)
        sys.exit(f"{len(leftovers)} source line(s) matched no pattern — parser integrity fail")

    notes = annotate_discrepancies(subjects)
    for n in notes:
        print("HEADER NOTE (source rollup is approximate):", n, file=sys.stderr)

    total_videos = sum(len(s["videos"]) for d in subjects.values() for s in d["sections"].values())
    payload = {"source": pdf.split("/")[-1],
               "total_subjects": len(subjects),
               "total_videos": total_videos,
               "subjects": subjects}
    with open(out, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"Wrote {out}: {len(subjects)} subjects, {total_videos} videos, "
          f"{len(notes)} subject(s) with approximate headers (non-fatal)")


if __name__ == "__main__":
    main()
