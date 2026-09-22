#!/usr/bin/env python3
"""Shared machinery for the hand written bank generators.

Two generators use this and a third will. What it holds is not scaffolding: it is the
three corrections that every hand written bank needs and that were each learned the hard
way, in one place so a new bank cannot ship without them.

  permute      The items are written key first, because that is how a person writes one.
               Shipping them that way puts every answer at position A (INC-0039). The
               seed is zlib.crc32 of the item id, never hash(), which Python randomises
               per process and which once made every build produce a different bank
               (INC-0003).

  extend       A correct answer is usually the most fully qualified statement on offer,
               so a bank written naturally has a length tell: on the first LSAT reading
               pass the longest option was the key on 66 percent of items against a
               chance rate of 20 (INC-0044). Distractors are extended with clauses the
               author supplies. Extending exactly one distractor per item moves the tell
               one position over rather than removing it, so measure() reports the whole
               rank distribution and not only the extremes.

  emit         Strings go through json.dumps. An unescaped apostrophe in generated JS
               once took the entire trainer down at parse time (INC-0001). Ids stay
               single quoted, because the build counts items by pattern and a file that
               quotes them differently counts as zero (INC-0059).
"""
import io, json, sys, zlib, random
from collections import Counter


def permute(items):
    """Move each key off position A, deterministically, and recompute the index."""
    for it in items:
        key = it['choices'][it['answer']]
        rnd = random.Random(zlib.crc32(it['id'].encode('ascii')))
        ch = list(it['choices'])
        rnd.shuffle(ch)
        it['choices'] = ch
        it['answer'] = ch.index(key)
    return items


def extend(items, table, label='EXTEND'):
    """Append an author supplied clause to one named distractor per item.

    The clause is matched by a substring of the choice so it survives permutation. Two
    things are refused rather than warned about: a needle that matches no choice or more
    than one, which means the table has gone stale, and a needle that matches the key,
    which would make the tell worse rather than better.
    """
    for it in items:
        ext = table.get(it['id'])
        if not ext:
            continue
        needle, clause = ext
        hits = [i for i, c in enumerate(it['choices']) if needle in c]
        if len(hits) != 1:
            sys.exit('%s %s: needle %r matched %d choices, not 1'
                     % (label, it['id'], needle, len(hits)))
        i = hits[0]
        if i == it['answer']:
            sys.exit('%s %s: the clause targets the key, which would worsen the tell'
                     % (label, it['id']))
        c = it['choices'][i]
        dot = c.endswith('.')
        it['choices'][i] = (c[:-1] if dot else c) + clause + ('.' if dot else '')
    return items


def measure(items):
    """Report the distributions a hand written bank gets wrong, as numbers.

    Both extremes, which the recorded ratchet in test.js checks, and the full length rank,
    which it does not. The rank matters because correcting the extreme moves the tell one
    position over: after the first LSAT reading pass 25 of 35 keys sat second longest, so
    a student picking the second longest option scored 71 percent (recorded in the commit
    for PR 65).
    """
    n = len(items)
    pos = Counter(it['answer'] for it in items)
    rank = [0] * max(len(it['choices']) for it in items)
    scored = longest = shortest = 0
    for it in items:
        L = [len(c) for c in it['choices']]
        order = sorted(range(len(L)), key=lambda i: L[i])
        rank[order.index(it['answer'])] += 1
        mx, mn = max(L), min(L)
        if L.count(mx) != 1 or L.count(mn) != 1:
            continue
        scored += 1
        if L[it['answer']] == mx:
            longest += 1
        if L[it['answer']] == mn:
            shortest += 1
    k = len(items[0]['choices'])
    print('  items %d, %d choices each' % (n, k))
    print('  key position   %s  (even would be %.1f each)'
          % (dict(sorted(pos.items())), n / float(k)))
    print('  longest is key %d%% of %d scored, shortest %d%%  (cap 36, chance %d)'
          % (round(longest * 100.0 / max(1, scored)), scored,
             round(shortest * 100.0 / max(1, scored)), round(100.0 / k)))
    print('  length rank    %s  (even would be %.1f each)'
          % (' '.join(str(r) for r in rank), n / float(k)))
    print('  best single-rank strategy scores %d%%' % round(max(rank) * 100.0 / n))
    print('  per skill      %s' % dict(sorted(Counter(it['skill'] for it in items).items())))
    return {'longest': longest, 'shortest': shortest, 'scored': scored, 'rank': rank}


def check_house_rules(js):
    """The rules the build enforces, checked here so a failure names the generator."""
    for ch, name in ((chr(0x2014), 'em dash'), (chr(0x2013), 'en dash')):
        if ch in js:
            sys.exit('%s in the generated bank' % name)
    bad = sorted(set(c for c in js if ord(c) > 127))
    if bad:
        sys.exit('non-ascii in the generated bank: %r' % bad)


def write(dest, header, consts, items, const_name, passage_var=None, group_key=None):
    """Emit the bank file.

    consts is an ordered list of (js_name, value) written above the array, for passages.
    passage_var maps an item's passage key to one of those names; omit it for a bank
    whose items carry no passage.
    """
    out = [header]
    for name, val in consts:
        out.append('const %s = %s;' % (name, json.dumps(val)))
    if consts:
        out.append('')
    out.append('const %s = [' % const_name)
    cur = None
    for it in items:
        if group_key:
            g = it.get(group_key)
            if g != cur:
                cur = g
                out.append('// ---------- %s ----------' % g)
        fields = ["id:'%s'" % it['id'], "section:'%s'" % it['section'],
                  "type:'%s'" % it['type']]
        if it.get('sub'):
            fields.append('sub:%s' % json.dumps(it['sub']))
        if it.get('passageId'):
            fields.append("passageId:'%s'" % it['passageId'])
        if passage_var and it.get('_p'):
            fields.append('passage:%s' % passage_var[it['_p']])
        fields.append("skill:'%s'" % it['skill'])
        fields.append('diff:%d' % it['diff'])
        out.append('{' + ','.join(fields) + ',')
        out.append(' stem:%s,' % json.dumps(it['stem']))
        out.append(' choices:[' + ','.join(json.dumps(c) for c in it['choices'])
                   + '],answer:%d,' % it['answer'])
        out.append(' expl:%s,' % json.dumps(it['expl']))
        out.append(' wrong:%s},' % json.dumps(it['wrong']))
    out.append('];')
    out.append('')
    js = '\n'.join(out)
    check_house_rules(js)
    io.open(dest, 'w', encoding='utf-8').write(js)
    print('wrote %s' % dest)
    return js
