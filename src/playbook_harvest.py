#!/usr/bin/env python3
"""Notice when the defect ledger has fallen behind the repository.

THE PROBLEM THIS SOLVES
=======================
The playbook regenerates itself from the ledger on every build, so the document can never
be out of step with the ledger. Nothing, however, keeps the LEDGER in step with reality.
A session fixes three bugs, writes them up beautifully in a commit message, and forgets to
append the records. The book then reports 47 defects with total confidence while the
repository has seen sixty, and a document that is confidently incomplete is worse than one
that admits a gap.

So this reads the commits that have landed since the newest commit the ledger cites, scans
them for the language people use when they are describing something that broke, and says
which ones look like they contain an unrecorded incident. It does not write records: it
cannot know the root cause, the detection route or the lesson, and guessing those would
fill the ledger with plausible fiction, which is the one thing the ledger must not contain.
It produces a skeleton per candidate and a human or a session fills it in.

Run:
  python3 src/playbook_harvest.py            report candidates
  python3 src/playbook_harvest.py --check    exit 1 if any are unrecorded
  python3 src/playbook_harvest.py --json     skeleton records to paste and fill in
"""
import io, os, re, sys, json, subprocess, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, 'data', 'playbook', 'incidents.jsonl')
# Commits looked at and found to carry no unrecorded defect. Kept as a file rather than as
# a silent skip, because "we checked this and it was fine" is information, and the ledger
# is the place that remembers what was looked at. Without it the same false positive is
# re-investigated every week forever.
CLEARED = os.path.join(ROOT, 'data', 'playbook', 'cleared.jsonl')

# The vocabulary of a defect, as it actually appears in this repository's commit messages.
# Deliberately generous: a false positive costs someone thirty seconds of reading, and a
# false negative costs a permanently missing record.
SIGNALS = [
    r'\bbugs?\b', r'\bbroke(?:n)?\b', r'\bregression', r'\bsilently\b', r'\bmisfire',
    r'\bcrash', r'\bwas wrong\b', r'\bwere wrong\b', r'\bgot wrong\b', r'\bwould have\b',
    r'\bfixe?[sd]? (?:a|the|three|two|four|five)\b', r'\bcaught (?:it|before|in draft)\b',
    r'\bshipping\b.*\bwrong\b', r'\bnever (?:ran|fired|worked)\b', r'\bdefects?\b',
    r'\bfound (?:a|three|two|four|five)\b', r'\bpre-existing\b',
]
SIGNAL_RE = re.compile('|'.join(SIGNALS), re.I)

# Commits that are content or copy drops rather than engineering, where defect words in a
# blog title would be noise.
SKIP_SUBJECT = re.compile(r'^(Add \d+ scheduled posts|Merge |Revert )', re.I)


def sh(*a):
    return subprocess.run(a, cwd=ROOT, capture_output=True, text=True).stdout


def ledger_rows():
    if not os.path.exists(LEDGER):
        return []
    return [json.loads(l) for l in io.open(LEDGER, encoding='utf-8') if l.strip()]


def main():
    rows = ledger_rows()
    cited = {r['commit'] for r in rows if r.get('commit')}
    cleared = set()
    if os.path.exists(CLEARED):
        for l in io.open(CLEARED, encoding='utf-8'):
            if l.strip():
                cleared.add(json.loads(l)['commit'])
    cited |= cleared
    next_id = 1
    for r in rows:
        m = re.match(r'INC-(\d+)$', r.get('id', ''))
        if m:
            next_id = max(next_id, int(m.group(1)) + 1)

    # Every commit, newest first, with its body. Walking the whole history rather than
    # only since the last entry, because a backfill can leave older gaps and those are
    # exactly the ones nobody goes looking for.
    raw = sh('git', 'log', '--format=%H%x01%h%x01%ad%x01%s%x01%b%x02', '--date=short')
    commits = []
    for chunk in raw.split('\x02'):
        chunk = chunk.strip('\n')
        if not chunk:
            continue
        parts = chunk.split('\x01')
        if len(parts) < 5:
            continue
        full, short, date, subject, body = parts[0], parts[1], parts[2], parts[3], parts[4]
        commits.append({'sha': short, 'date': date, 'subject': subject, 'body': body})

    candidates = []
    for c in commits:
        if c['sha'] in cited or SKIP_SUBJECT.search(c['subject']):
            continue
        text = c['subject'] + '\n' + c['body']
        hits = []
        for ln in text.split('\n'):
            ln = ln.strip()
            if len(ln) > 15 and SIGNAL_RE.search(ln):
                hits.append(ln)
        if hits:
            candidates.append({'commit': c['sha'], 'date': c['date'],
                               'subject': c['subject'], 'lines': hits[:6]})

    if '--json' in sys.argv:
        out = []
        for i, c in enumerate(candidates):
            out.append({
                'id': 'INC-%04d' % (next_id + i),
                'date': c['date'], 'commit': c['commit'], 'pr': None,
                'title': 'TODO from: ' + c['subject'][:80],
                'area': 'TODO one of: build frontend css db payments content algorithm testing infra seo privacy uiux',
                'severity': 'TODO one of: site-down data-wrong silent-loss degraded cosmetic',
                'symptom': 'TODO what a person saw',
                'root_cause': 'TODO why it happened',
                'detection': 'TODO how it surfaced',
                'detection_class': 'TODO one of: user-visible test review measurement render build-guard adversarial-review',
                'fix': 'TODO what changed',
                'guard': None, 'guard_file': None,
                'lesson': 'TODO the transferable rule, stated without reference to this codebase',
                'cost': None,
                '_evidence': c['lines'],
            })
        print(json.dumps(out, indent=2))
        return 0

    print('ledger: %d incidents, %d commits cited, %d cleared as not-a-defect'
          % (len(rows), len(cited) - len(cleared), len(cleared)))
    print('history: %d commits' % len(commits))
    if not candidates:
        print('\nNo unrecorded commits carry defect language. The ledger is level with the '
              'repository.')
        return 0

    print('\n%d commit(s) look like they describe a defect that is not in the ledger:\n'
          % len(candidates))
    for c in candidates:
        print('  %s  %s  %s' % (c['commit'], c['date'], c['subject'][:72]))
        for ln in c['lines'][:3]:
            print('      %s' % ln[:110])
        print('')
    print('Write each one up in data/playbook/incidents.jsonl, then run '
          'python3 src/build_playbook.py.')
    print('python3 src/playbook_harvest.py --json prints skeletons to fill in.')
    print('\nA commit here is a CANDIDATE, not a verdict. If it carries no real defect, the '
          'honest resolution is a record with a plain note, not a silent skip: the ledger '
          'is the place that remembers what was looked at.')

    if '--check' in sys.argv:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
