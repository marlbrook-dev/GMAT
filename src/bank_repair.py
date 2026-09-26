#!/usr/bin/env python3
"""Lengthen named distractors inside a hand written bank file, in place.

The generated banks and the newer hand written ones are emitted by a generator, so their
length tell is corrected by the LIFT table in src/bank_emit.py before the file is written.
The older hand written banks were never generated: bank_sat_rw.js and its siblings are
source, edited by hand, with comments and formatting worth keeping. Regenerating them
would produce a diff in which the correction is invisible.

So this edits the text. For each entry it finds the item by its id literal, finds the one
choice in that item containing the needle, and inserts the clause before the closing
quote of that string literal. Everything else in the file is left byte identical, which
is what makes the diff readable: every changed line is a distractor that got longer.

Two refusals, both of which mean the table has gone stale rather than the file being
wrong: a needle that matches no choice or more than one inside the item, and a needle
that matches the key. The second is the important one, because lengthening the key makes
the tell worse and the only symptom would be a number that moved the wrong way.

Verification is not optional and is not done here: run node src/test.js, which measures
every hand written file against its recorded value.
"""
import io, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_emit  # noqa: E402


def _item_span(src, iid):
    """The object literal for one item, as a slice of the source text."""
    m = re.search(r"\{\s*id: ?['\"]%s['\"]" % re.escape(iid), src)
    if not m:
        sys.exit('%s: no item with that id' % iid)
    i = m.start()
    depth = 0
    for j in range(i, len(src)):
        if src[j] == '{':
            depth += 1
        elif src[j] == '}':
            depth -= 1
            if depth == 0:
                return i, j + 1
    sys.exit('%s: unbalanced braces after the id' % iid)


def _literal_end(src, at):
    """Index of the closing quote of the string literal containing position `at`."""
    # Walk back to the opening quote, respecting backslash escapes.
    k = at
    while k >= 0:
        if src[k] in '"\'' and (k == 0 or src[k - 1] != '\\'):
            quote = src[k]
            break
        k -= 1
    else:
        sys.exit('no opening quote before offset %d' % at)
    j = at
    while j < len(src):
        if src[j] == '\\':
            j += 2
            continue
        if src[j] == quote:
            return j
        j += 1
    sys.exit('unterminated string literal at offset %d' % at)


def swap(path, table):
    """Replace exact text inside a named item, for choices a clause cannot lengthen.

    A vocabulary in context item offers single words, and there is nowhere to append a
    clause: the fix is a longer distractor of the same register, which is a substitution
    rather than an extension. Same refusals as repair: the old text must occur exactly
    once inside the item.
    """
    src = io.open(path, encoding='utf-8').read()
    plan = []
    for iid, pairs in table.items():
        a, b = _item_span(src, iid)
        seg = src[a:b]
        for old_text, new_text in pairs:
            hits = [m.start() for m in re.finditer(re.escape(old_text), seg)]
            if len(hits) != 1:
                sys.exit('%s: %r matched %d times in the item, not 1'
                         % (iid, old_text, len(hits)))
            # An item is not just its choices. expl and wrong name particular options,
            # and on a vocabulary bank they name them by word, so replacing the choice
            # and nothing else leaves a note explaining an option nobody was shown
            # (INC-0072). The bare word, without the quotes the caller wraps it in, is
            # what such a note would contain.
            bare = old_text.strip('\'"')
            elsewhere = [m.start() for m in re.finditer(re.escape(bare), seg)
                         if m.start() != hits[0] + old_text.index(bare)]
            if elsewhere:
                sys.exit('%s: %r also appears elsewhere in the item, which is where an '
                         'explanation naming it would be. Rewrite that text in the same '
                         'change or the note will describe an option that is not offered.'
                         % (iid, bare))
            plan.append((a + hits[0], len(old_text), new_text))
    for pos, ln, new_text in sorted(plan, reverse=True):
        src = src[:pos] + new_text + src[pos + ln:]
    for ch, name in ((chr(0x2014), 'em dash'), (chr(0x2013), 'en dash')):
        if ch in src:
            sys.exit('%s in the repaired bank' % name)
    bad = sorted(set(c for c in src if ord(c) > 127))
    if bad:
        sys.exit('non-ascii in the repaired bank: %r' % bad)
    io.open(path, 'w', encoding='utf-8').write(src)
    print('%s: %d choices replaced' % (path, sum(len(v) for v in table.values())))
    return src


def repair(path, table, answers=None):
    """Apply {id: [(needle, clause), ...]} to the bank at `path`.

    `answers` maps an id to the key's text, when it is known; a needle matching it is
    refused. Callers that cannot supply it get the weaker check only.
    """
    src = io.open(path, encoding='utf-8').read()
    edits = 0
    # Later edits shift earlier offsets, so collect and apply from the end backwards.
    plan = []
    for iid, pairs in table.items():
        a, b = _item_span(src, iid)
        seg = src[a:b]
        for needle, clause in pairs:
            # A clause is appended at the END of the choice, never at the end of the
            # needle. Text beginning with a letter is a continuation of something, and
            # continuations written against a truncated report produced "in chronological
            # orderorder" and "how it would spend itintends to spend the money"
            # (INC-0071). The refusal is one condition; remembering is a habit.
            if not clause[:1] or clause[0].isalnum():
                sys.exit('%s: clause %r begins with a letter or digit, so it would run '
                         'into the end of the choice. A clause is appended, not '
                         'continued: start it with a space or punctuation.'
                         % (iid, clause))
            hits = [m.start() for m in re.finditer(re.escape(needle), seg)]
            if len(hits) != 1:
                sys.exit('%s: needle %r matched %d times in the item, not 1'
                         % (iid, needle, len(hits)))
            if answers and needle in answers.get(iid, ''):
                sys.exit('%s: needle %r is inside the key, which would worsen the tell'
                         % (iid, needle))
            end = _literal_end(seg, hits[0] + len(needle) - 1)
            # The clause goes in at the end of the literal, so the needle has to reach it.
            # One that stops short lets a clause written to follow the needle land after
            # the words it was written to replace (INC-0119).
            stop = end - 1 if end > 0 and seg[end - 1] == '.' else end
            if hits[0] + len(needle) != stop:
                sys.exit('%s: needle %r stops short of the end of its choice; extend it to '
                         'the end, since the clause is appended there (INC-0119)'
                         % (iid, needle))
            # Refuse a clause that repeats the words it is about to follow. A needle
            # taken from a truncated report can sit well before the end of the choice,
            # and a clause written as though the needle were the end then says the same
            # thing twice: "with pumice replacing heavier aggregate in the upper courses
            # replacing heavier aggregate in the upper courses of the structure".
            tail = seg[max(0, end - 160):end]
            words = clause.strip(' ,.;:').split()
            head = ' '.join(words[:3]).lower()
            if head and head in tail.lower():
                sys.exit('%s: clause %r repeats text already at the end of the choice; '
                         'it is appended at the end, not at the needle'
                         % (iid, clause))
            # And the check bank_emit.extend uses, which also catches a two word overlap
            # and an ending restated in other words: "has been observed" plus " been
            # observed, whatever the relatedness" passed both checks here (INC-0119).
            rep = bank_emit.restates(tail.rstrip(' .'), clause)
            if rep:
                sys.exit('%s: clause %r repeats %r, which the choice already ends with '
                         '(INC-0119)' % (iid, clause, rep))
            # The three word check misses a single repeated word, which is what a needle
            # ending one word short produces: "measure of the company's performance" plus
            # " performance, ahead of cost per call". Compare the first word of the clause
            # with the last word of the choice as well.
            last = tail.strip(' .,;:').split()
            if words and last and words[0].strip('.,;:').lower() == last[-1].strip('.,;:').lower():
                sys.exit('%s: clause %r begins with the word the choice already ends on '
                         '(%r); the clause is appended at the end, not at the needle'
                         % (iid, clause, last[-1]))
            # Insert BEFORE a trailing full stop, which is what bank_emit.extend does.
            # Appending at the closing quote instead put the clause after the sentence's
            # own period and produced "the number of purchases. made" (INC-0070). Any
            # further tool that appends to a choice needs this too.
            if end > 0 and seg[end - 1] == '.':
                end -= 1
            plan.append((a + end, clause))
            edits += 1
    for pos, clause in sorted(plan, reverse=True):
        src = src[:pos] + clause + src[pos:]
    for ch, name in ((chr(0x2014), 'em dash'), (chr(0x2013), 'en dash')):
        if ch in src:
            sys.exit('%s in the repaired bank' % name)
    bad = sorted(set(c for c in src if ord(c) > 127))
    if bad:
        sys.exit('non-ascii in the repaired bank: %r' % bad)
    io.open(path, 'w', encoding='utf-8').write(src)
    print('%s: %d distractors lengthened' % (path, edits))
    return edits
