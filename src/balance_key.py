#!/usr/bin/env python3
"""Even out the answer key of a bank file.

A bank written in one sitting drifts: the writer reaches for the same slot without
noticing, and the key becomes guessable. This project has been here before, with 225 of
302 GMAT answers sitting at position A. Rather than re-detect it by hand each time, this
rotates the choices of single-answer items so the correct slot is spread evenly, and
updates the answer index to match.

It only touches items whose choices carry no natural order, which in practice means items
whose choices are words or phrases rather than numbers. A numeric list that reads 4, 5, 6,
25 is ordered on purpose, and shuffling it would look wrong to a test taker, so any item
whose choices all parse as numbers is left exactly as written. Items with an array answer
(GRE Sentence Equivalence, which wants two of six) are also left alone.

Usage:  python3 src/balance_key.py src/bank_gre_verbal.js [--apply]
Without --apply it reports what it would change and writes nothing.
"""
import re, sys, io, collections

ITEM = re.compile(r"\{id:'([A-Z]{2}\d{3})'.*?\n(?=\{id:'|\];)", re.S)

def numeric(choices):
    def isnum(c):
        return bool(re.fullmatch(r"-?[\d,]+(\.\d+)?%?", c.strip()))
    return all(isnum(c) for c in choices)

def parse_choices(block):
    m = re.search(r"choices:\[(.*?)\],answer:(\d+)", block, re.S)
    if not m:
        return None
    raw, ans = m.group(1), int(m.group(2))
    parts, buf, q, esc = [], "", None, False
    for ch in raw:
        if esc:
            buf += ch; esc = False; continue
        if ch == "\\":
            buf += ch; esc = True; continue
        if q:
            if ch == q:
                parts.append(buf); buf = ""; q = None
            else:
                buf += ch
        elif ch in "'\"":
            q = ch
    return parts, ans, m

def main():
    path = sys.argv[1]
    apply = "--apply" in sys.argv
    text = io.open(path, encoding="utf-8").read()
    blocks = ITEM.findall(text)
    ids = [b for b in blocks]
    before, after, changes = collections.Counter(), collections.Counter(), 0
    out = text
    # Walk items in order, assigning target slots round-robin so the key comes out flat.
    targets = {}
    eligible = []
    for m in re.finditer(r"\{id:'([A-Z]{2}\d{3})'(.*?)(?=\n\{id:'|\n\];)", text, re.S):
        iid, block = m.group(1), m.group(2)
        if "answerType:'se'" in block or "answer:[" in block:
            continue
        # Quantitative Comparison choices are fixed and ordered by meaning: A greater,
        # B greater, equal, cannot be determined. Rotating them would produce nonsense,
        # so QC items are balanced by writing them with varied answers, not by rotation.
        if "type:'QC'" in block:
            continue
        p = parse_choices(block)
        if not p:
            continue
        choices, ans, _ = p
        before[ans] += 1
        if numeric(choices):
            continue
        eligible.append((iid, block, choices, ans))
    n_slots = max((len(c) for _, _, c, _ in eligible), default=5)
    for i, (iid, block, choices, ans) in enumerate(eligible):
        targets[iid] = i % len(choices)
    for iid, block, choices, ans in eligible:
        want = targets[iid]
        if want == ans:
            after[ans] += 1
            continue
        # Rotate so the correct choice lands on the target slot, preserving relative order.
        shift = (ans - want) % len(choices)
        new = choices[shift:] + choices[:shift]
        assert new[want] == choices[ans], "rotation lost the correct answer for " + iid
        old_frag = re.search(r"choices:\[(.*?)\],answer:(\d+)", block, re.S).group(0)
        new_frag = "choices:[" + ",".join("'" + c + "'" for c in new) + "],answer:" + str(want)
        out = out.replace(old_frag, new_frag, 1)
        after[want] += 1
        changes += 1
    for _, _, c, a in eligible:
        pass
    print("answer positions before:", dict(sorted(before.items())))
    print("items rotated:", changes, "of", len(eligible), "eligible")
    if apply:
        io.open(path, "w", encoding="utf-8").write(out)
        print("written to", path)
    else:
        print("(dry run; pass --apply to write)")

if __name__ == "__main__":
    main()
