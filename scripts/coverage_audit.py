"""
scripts/coverage_audit.py

For every subject, checks which "important" questions are NOT backed by the
comprehensive report, and writes data/<subject>/coverage_gaps.json.

Run from anywhere:  python scripts/coverage_audit.py
Run it after predictive_picker.py and before build_site.py.

Method (heuristic, vocabulary-based): take the distinctive terms in a question's
title + answer, and measure what fraction appear in the report text.
Low coverage = the report probably doesn't help with that question.
Treat it as a to-do list to eyeball, not as ground truth (e.g. "E-R" vs "ER").
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent      # no hard-coded C:\Users\... path
SUBJECTS = ["dbms", "java", "os", "daa", "ml", "maths"]
THRESHOLD = 0.40                                    # below this = "gap"

STOP = set("""what which write explain define differentiate between discuss with following
given using example examples that this their about from into your have does each list state
describe short note briefly various types type name compare find show how why when where
whether also used use uses consider suppose statement statements give any four three two five
its are the and for can will not all has may make""".split())


def terms(text):
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&\w+;", " ", text).lower()
    text = text.replace("e-r", "er")               # normalise common spelling variants
    return [w for w in re.findall(r"[a-z][a-z0-9_+\-]{2,}", text) if w not in STOP]


def load_cheat_terms(subject):
    html = (ROOT / "subjects" / subject / "comprehensive-report.html").read_text(encoding="utf-8")
    html = re.sub(r"<script.*?</script>|<style.*?</style>", "", html, flags=re.S | re.I)
    return set(terms(html))


def main():
    for s in SUBJECTS:
        qpath = ROOT / "data" / s / f"{s}_questions.json"
        if not qpath.exists():
            continue
        questions = json.loads(qpath.read_text(encoding="utf-8"))
        cheat = load_cheat_terms(s)
        gaps = []
        for q in questions:
            if not q.get("important"):
                continue
            title_terms = list(dict.fromkeys(terms(q["title"])))
            if not title_terms:
                continue
            missing = [t for t in title_terms if t not in cheat]
            cov = 1 - len(missing) / len(title_terms)
            if cov < THRESHOLD:
                gaps.append({
                    "id": q["id"], "unit": q.get("unit"), "marks": q.get("marks"),
                    "bloom": q.get("bloom"), "coverage": round(cov, 2),
                    "missing_terms": missing[:8], "title": q["title"][:140],
                })
        gaps.sort(key=lambda g: (g["coverage"], -(g["marks"] or 0)))
        out = ROOT / "data" / s / "coverage_gaps.json"
        out.write_text(json.dumps(gaps, indent=2, ensure_ascii=False), encoding="utf-8")
        n_imp = sum(1 for q in questions if q.get("important"))
        print(f"[{s}] {len(gaps)}/{n_imp} important questions poorly covered -> {out.name}")


if __name__ == "__main__":
    main()
