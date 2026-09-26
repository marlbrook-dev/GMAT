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
  python3 src/playbook_harvest.py --citations report records citing no commit
  python3 src/playbook_harvest.py --backfill  write those citations in from git
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


# --- citation backfill --------------------------------------------------------------
# The ledger's own design says every record cites the commit that fixed it, so a claim in
# the playbook can be checked against the repository. Fifty of the first hundred records
# cited nothing, and the reason is structural rather than careless: CLAUDE.md requires the
# record to be written BEFORE the fix, so at the moment of writing the commit does not
# exist yet. Nobody ever goes back.
#
# It does not have to be remembered, because the fact is recoverable. Sessions name the
# incident in the commit message that fixes it, so git already holds the mapping. This
# reads it out rather than asking anyone to maintain it.
#
# Two rules keep it honest, and they are the same rule twice: only write what is read.
#   Only commits reachable from main count. Branch commits are squashed away on merge and
#   citing one gives a SHA that will not resolve for anyone else.
#   Where several main commits name an incident, the EARLIEST is the fix and the rest are
#   back-references; a defect cannot be referred to before it is recorded. That was
#   checked against all eight ambiguous cases in this repository rather than assumed: the
#   later mentions read "was the same", "exactly", "recurring inside".
INC_RE = re.compile(r'INC-\d{4}')


def incident_commits(rev='origin/main'):
    """incident id -> the earliest commit reachable from rev whose message names it."""
    out = sh('git', 'log', rev, '--format=%H%x1f%ct%x1f%s%x1f%b%x1e')
    if not out.strip():
        out = sh('git', 'log', 'HEAD', '--format=%H%x1f%ct%x1f%s%x1f%b%x1e')
    found = {}
    for entry in out.split('\x1e'):
        if not entry.strip():
            continue
        parts = (entry.strip().split('\x1f') + ['', '', ''])[:4]
        sha, ts, subj, body = parts
        try:
            when = int(ts)
        except ValueError:
            continue
        for inc in set(INC_RE.findall(subj + ' ' + body)):
            prev = found.get(inc)
            if prev is None or when < prev[0]:
                found[inc] = (when, sha, subj)
    return found


def main_commit_by_pr(rev='origin/main'):
    """PR number -> the squash commit on main, read from the (#NN) suffix git writes."""
    out = sh('git', 'log', rev, '--format=%H%x1f%s%x1e')
    by_pr = {}
    for entry in out.split('\x1e'):
        if not entry.strip():
            continue
        parts = (entry.strip().split('\x1f') + [''])[:2]
        sha, subj = parts
        m = re.search(r'\(#(\d+)\)\s*$', subj)
        if m:
            by_pr.setdefault(int(m.group(1)), sha)
    return by_pr


def unreachable(rev='origin/main'):
    """Records whose cited commit is not an ancestor of main.

    These resolve in the clone that wrote them and nowhere else. A squash merge replaces
    the branch commits with one new commit, so a citation written against a branch SHA
    points at an object that a fresh clone of main has never heard of. The citation looks
    fine locally and is worthless to the reader it exists for, which is the same shape as
    a source that only the author can open.
    """
    rows = ledger_rows()
    by_pr = main_commit_by_pr(rev)
    out = []
    for r in rows:
        sha = r.get('commit')
        if not sha:
            continue
        anc = subprocess.run(['git', 'merge-base', '--is-ancestor', sha, rev],
                             cwd=ROOT, capture_output=True)
        if anc.returncode == 0:
            continue
        out.append((r, by_pr.get(r.get('pr'))))
    return out


def repoint(write=False, rev='origin/main'):
    """Move citations off squashed-away branch commits onto the merge that landed them."""
    rows = ledger_rows()
    index = {r['id']: r for r in rows}
    moved, stuck = [], []
    for r, target in unreachable(rev):
        if not target:
            stuck.append(r['id'])
            continue
        old_sha = r['commit']
        index[r['id']]['commit'] = target
        moved.append((r['id'], old_sha[:8], target[:8], r.get('pr')))
    if write and moved:
        with io.open(LEDGER, 'w', encoding='utf-8') as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + '\n')
    return moved, stuck


def backfill(write=False):
    """Fill in commit and pr on records that cite neither, from the git history.

    Returns (filled, still_missing). Writes nothing unless asked, so it can be run as a
    report or as a check.
    """
    rows = ledger_rows()
    found = incident_commits()
    filled, missing = [], []
    for r in rows:
        if r.get('commit'):
            continue
        hit = found.get(r.get('id'))
        if not hit:
            missing.append(r.get('id'))
            continue
        _, sha, subj = hit
        r['commit'] = sha
        if not r.get('pr'):
            m = re.search(r'\(#(\d+)\)\s*$', subj)
            if m:
                r['pr'] = int(m.group(1))
        filled.append((r['id'], sha[:8], r.get('pr')))
    if write and filled:
        with io.open(LEDGER, 'w', encoding='utf-8') as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + '\n')
    return filled, missing


def main():
    # Citation backfill runs first and on its own, because it answers a different question
    # from the rest of this tool: not "is the ledger missing a record" but "does a record
    # we already have still fail to point at the commit that fixed it".
    if '--backfill' in sys.argv or '--citations' in sys.argv:
        write = '--backfill' in sys.argv
        filled, missing = backfill(write=write)
        verb = 'filled' if write else 'would fill'
        print('%s %d citation(s) from the git history' % (verb, len(filled)))
        for inc, sha, pr in filled:
            print('  %s  %s%s' % (inc, sha, ('  PR #%d' % pr) if pr else ''))
        moved, stuck = repoint(write=write, )
        if moved:
            print('%s %d citation(s) off a squashed branch commit onto its merge'
                  % ('moved' if write else 'would move', len(moved)))
            for inc, was, now, pr in moved:
                print('  %s  %s -> %s  PR #%s' % (inc, was, now, pr))
        if stuck:
            print('%d citation(s) are unreachable from main and name no PR: %s'
                  % (len(stuck), ', '.join(stuck)))
        if missing:
            print('\n%d record(s) name no commit and no commit names them:' % len(missing))
            print('  ' + ', '.join(missing))
            print('  These need a human: either the fix landed without naming the '
                  'incident, or it has not landed yet.')
        return 0
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


def stale_citations():
    """Records that cite no commit while git already names one.

    This is the drift the backfill exists to remove, reported so it cannot silently
    return. A record with no citation is not necessarily wrong: the fix may not have
    landed yet, which is the normal state for the record written minutes ago. What is
    wrong is a record with no citation when the commit that fixed it is sitting in main
    naming it, because that is a fact nobody has to remember and nobody is reading.
    """
    filled, _ = backfill(write=False)
    return [inc for inc, _sha, _pr in filled]


if __name__ == '__main__':
    sys.exit(main())
