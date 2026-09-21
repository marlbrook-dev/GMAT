#!/usr/bin/env python3
"""Build the Build Playbook: one deliverable, assembled rather than maintained.

WHY THIS IS A BUILD AND NOT A DOCUMENT
======================================
A handwritten guide rots. It is accurate the week it is written and quietly wrong a month
later, which is worse than having none at all, because a wrong playbook gets followed. So
this is built the same way the site is built, from three sources that are already kept
true for other reasons:

  docs/playbook/*.md            prose. The judgement, the reasoning, the tradeoffs.
  data/playbook/incidents.jsonl the defect ledger. One record per bug, error or misfire.
  the repository itself         every figure. Counts, file lists, guards, schema, history.

No number in the output is typed. Chapters carry {{PLACEHOLDERS}} which are filled from a
harvest of the real repository, and an unresolved placeholder fails the build. That is the
same rule the site follows for school statistics, applied to the document about building
the site: a figure nobody can regenerate is a figure that will eventually be wrong.

WHAT MAKES IT ADAPTIVE
======================
Every incident record names the guard it produced. The checklist chapter is GENERATED from
those fields, so a new defect automatically becomes a line on the checklist the next time
the document is built, and recurrence is countable: two incidents pointing at one guard is
a guard that is not working. The document gets better because the ledger grows, not
because somebody remembers to rewrite a chapter.

OUTPUTS
=======
  playbook/BUILD_PLAYBOOK.md      the assembled source
  playbook/index.html             self contained, styled, prints well
  playbook/BUILD_PLAYBOOK.pdf     via headless Chromium, if available
  playbook/BUILD_PLAYBOOK.docx    written directly as OOXML, no dependencies

Run: python3 src/build_playbook.py
"""
import os, re, io, json, sys, glob, subprocess, zipfile, datetime, html, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTERS = os.path.join(ROOT, 'docs', 'playbook')
LEDGER = os.path.join(ROOT, 'data', 'playbook', 'incidents.jsonl')
OUT = os.path.join(ROOT, 'playbook')

TITLE = 'The Build Playbook'
SUBTITLE = 'How one person and a set of AI sessions built a multi-exam test-prep platform, every defect hit on the way, and the recipe for doing it again for something else'


def sh(*args):
    """Read a value from the world rather than typing one."""
    try:
        return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=120).stdout.strip()
    except Exception:
        return ''


# --------------------------------------------------------------------------- harvest ---
#
# Everything here is measured now, at build time. If a harvest key stops resolving, that
# is the document telling you the codebase moved, which is the entire point of harvesting
# rather than writing the number down.

def harvest():
    h = {}
    h['BUILT_ON'] = datetime.date.today().isoformat()
    h['COMMITS'] = sh('git', 'rev-list', '--count', 'HEAD')
    h['FIRST_COMMIT_DATE'] = sh('git', 'log', '--reverse', '--format=%ad', '--date=short').split('\n')[0]
    h['LAST_COMMIT_DATE'] = sh('git', 'log', '-1', '--format=%ad', '--date=short')
    h['HEAD_SHA'] = sh('git', 'rev-parse', '--short', 'HEAD')

    first = h['FIRST_COMMIT_DATE']
    last = h['LAST_COMMIT_DATE']
    try:
        d0 = datetime.date.fromisoformat(first)
        d1 = datetime.date.fromisoformat(last)
        h['ELAPSED_DAYS'] = str((d1 - d0).days)
    except Exception:
        h['ELAPSED_DAYS'] = '0'

    # Source inventory. Only files that are tracked, so build artefacts never inflate it.
    tracked = [f for f in sh('git', 'ls-files').split('\n') if f]
    h['TRACKED_FILES'] = str(len(tracked))

    def lines_of(paths):
        n = 0
        for p in paths:
            fp = os.path.join(ROOT, p)
            if os.path.isfile(fp):
                try:
                    with io.open(fp, encoding='utf-8', errors='replace') as fh:
                        n += sum(1 for _ in fh)
                except Exception:
                    pass
        return n

    py = [f for f in tracked if f.endswith('.py')]
    js = [f for f in tracked if f.endswith('.js') or f.endswith('.mjs')]
    sql = [f for f in tracked if f.endswith('.sql')]
    md = [f for f in tracked if f.endswith('.md')]
    ts = [f for f in tracked if f.endswith('.ts')]
    banks = [f for f in js if '/bank_' in f or f.startswith('src/bank_')]
    tests = sorted(f for f in js if re.search(r'/(smoke|test|review_bot|weekly_audit)', f))

    h['PY_FILES'], h['PY_LINES'] = str(len(py)), '{:,}'.format(lines_of(py))
    h['JS_FILES'], h['JS_LINES'] = str(len(js)), '{:,}'.format(lines_of(js))
    h['TS_FILES'] = str(len(ts))
    h['SQL_FILES'] = str(len(sql))
    h['MD_FILES'] = str(len(md))
    h['BANK_FILES'] = str(len(banks))
    h['TEST_FILES'] = str(len(tests))
    h['TEST_LIST'] = '\n'.join('- `%s`' % t for t in tests)

    # Migrations, read from the directory rather than counted by hand.
    migs = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, 'supabase', 'migrations', '*.sql')))
    h['MIGRATIONS'] = str(len(migs))

    # Edge functions.
    fns = sorted(d for d in os.listdir(os.path.join(ROOT, 'supabase', 'functions'))
                 if os.path.isdir(os.path.join(ROOT, 'supabase', 'functions', d))) \
        if os.path.isdir(os.path.join(ROOT, 'supabase', 'functions')) else []
    h['EDGE_FUNCTIONS'] = str(len(fns))
    h['EDGE_FUNCTION_LIST'] = ', '.join('`%s`' % f for f in fns)

    # Tables, taken from create table statements across every migration. This undercounts
    # tables made outside a migration, which is itself worth knowing.
    tbls = set()
    for p in glob.glob(os.path.join(ROOT, 'supabase', 'migrations', '*.sql')):
        try:
            txt = io.open(p, encoding='utf-8', errors='replace').read()
        except Exception:
            continue
        for m in re.finditer(r'create\s+table\s+(?:if\s+not\s+exists\s+)?(?:public\.)?([a-z_][a-z0-9_]*)', txt, re.I):
            tbls.add(m.group(1).lower())
    h['TABLES_IN_MIGRATIONS'] = str(len(tbls))

    # Schools and colleges, counted from the data directory.
    h['SCHOOL_FILES'] = str(len(glob.glob(os.path.join(ROOT, 'data', 'schools', '*.json'))))

    # Design tokens, read out of the one place they are defined.
    part = os.path.join(ROOT, 'src', 'partials.py')
    if os.path.isfile(part):
        t = io.open(part, encoding='utf-8', errors='replace').read()
        h['TOKEN_COUNT'] = str(len(set(re.findall(r'--[a-z0-9-]+\s*:', t))))
    else:
        h['TOKEN_COUNT'] = '0'

    # Exams, read from the engine registry rather than listed by hand.
    eng = os.path.join(ROOT, 'src', 'engine.js')
    exams = []
    if os.path.isfile(eng):
        t = io.open(eng, encoding='utf-8', errors='replace').read()
        m = re.search(r'EXAMS\s*=\s*\{(.*?)\n\}', t, re.S)
        if m:
            exams = sorted(set(re.findall(r"^\s{2}([a-z_][a-z0-9_]*)\s*:\s*\{", m.group(1), re.M)))
    h['EXAM_COUNT'] = str(len(exams)) if exams else 'unknown'
    h['EXAM_LIST'] = ', '.join(exams) if exams else 'see src/engine.js'

    return h


# ---------------------------------------------------------------------------- ledger ---

AREA_LABEL = {
    'build': 'Build system', 'frontend': 'Front end', 'css': 'CSS and layout',
    'db': 'Database', 'payments': 'Payments', 'content': 'Content generation',
    'algorithm': 'Scoring and selection', 'testing': 'Tests and guards',
    'infra': 'Infrastructure and deploy', 'seo': 'Search and metadata',
    'privacy': 'Privacy and consent', 'uiux': 'Interface and data display',
}
SEV_LABEL = {
    'site-down': 'Site down', 'data-wrong': 'Wrong data shown or stored',
    'silent-loss': 'Silent loss', 'degraded': 'Degraded', 'cosmetic': 'Cosmetic',
}
DET_LABEL = {
    'user-visible': 'A person hit it', 'test': 'A test caught it',
    'review': 'Found by reading the code or the output',
    'measurement': 'Found by measuring something',
    'render': 'Found by rendering it and looking',
    'build-guard': 'A build guard caught it',
    'adversarial-review': 'Found by a review bot or an adversarial pass',
}


def load_incidents():
    rows = []
    for i, line in enumerate(io.open(LEDGER, encoding='utf-8'), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception as e:
            raise SystemExit('incidents.jsonl line %d is not valid JSON: %s' % (i, e))
    rows.sort(key=lambda r: (r.get('date', ''), r.get('id', '')))
    return rows


def validate_incidents(rows):
    """Every citation has to resolve. A playbook that cites a file nobody can open is a
    playbook nobody can check, and an unverifiable claim is the thing this whole project
    exists to avoid."""
    need = ['id', 'date', 'title', 'area', 'severity', 'symptom', 'root_cause',
            'detection', 'detection_class', 'fix', 'lesson']
    # A clone with no history reports every citation as broken, which is a checker crying
    # wolf, and a tool that cries wolf gets muted. "Is this shallow" is the wrong question,
    # because a shallow clone usually still holds every commit the ledger cites. The
    # question that separates the two is whether ANY citation resolved at all.
    cited = [r['commit'] for r in rows if r.get('commit')]
    resolved = sum(1 for c in cited if sh('git', 'cat-file', '-t', c) == 'commit')
    no_history = bool(cited) and resolved == 0
    problems = []
    if no_history:
        print('  note: no cited commit resolved, so this clone has no history; '
              'citations not verified')
    seen = set()
    for r in rows:
        for k in need:
            if not r.get(k):
                problems.append('%s is missing %s' % (r.get('id', '?'), k))
        if r['id'] in seen:
            problems.append('duplicate id %s' % r['id'])
        seen.add(r['id'])
        if r.get('area') not in AREA_LABEL:
            problems.append('%s has unknown area %s' % (r['id'], r.get('area')))
        if r.get('severity') not in SEV_LABEL:
            problems.append('%s has unknown severity %s' % (r['id'], r.get('severity')))
        if r.get('detection_class') not in DET_LABEL:
            problems.append('%s has unknown detection_class %s' % (r['id'], r.get('detection_class')))
        c = r.get('commit')
        if c and not no_history and sh('git', 'cat-file', '-t', c) != 'commit':
            problems.append('%s cites commit %s, which does not exist' % (r['id'], c))
        g = r.get('guard_file')
        if g and not os.path.exists(os.path.join(ROOT, g)):
            problems.append('%s cites guard_file %s, which does not exist' % (r['id'], g))
    return problems


def ledger_chapter(rows):
    """The ledger, as prose a person can read, grouped by the part of the system it hit."""
    out = ['# The Defect Ledger\n']
    out.append(
        'Every entry here happened. Each one is a record of something that broke, how it was '
        'found, what fixed it, and what now stops it coming back. The last field is the one '
        'that matters for a different business: the transferable lesson, stated without '
        'reference to this codebase.\n')
    out.append(
        'They are grouped by the part of the system, and within a group by date. The `guard` '
        'field feeds the checklist chapter automatically, so nothing here has to be copied '
        'anywhere by hand.\n')

    by_area = {}
    for r in rows:
        by_area.setdefault(r['area'], []).append(r)

    for area in sorted(by_area, key=lambda a: -len(by_area[a])):
        items = by_area[area]
        out.append('\n## %s (%d)\n' % (AREA_LABEL[area], len(items)))
        for r in items:
            cite = []
            if r.get('commit'):
                cite.append('`%s`' % r['commit'])
            if r.get('pr'):
                cite.append('PR #%s' % r['pr'])
            head = '### %s. %s' % (r['id'], r['title'])
            out.append('\n%s\n' % head)
            out.append('*%s, %s%s*\n' % (r['date'], SEV_LABEL[r['severity']],
                                         (', ' + ' '.join(cite)) if cite else ''))
            out.append('- **What was seen.** %s' % r['symptom'])
            out.append('- **Why.** %s' % r['root_cause'])
            out.append('- **How it surfaced.** %s (%s)' % (r['detection'], DET_LABEL[r['detection_class']]))
            out.append('- **Fix.** %s' % r['fix'])
            if r.get('guard'):
                gf = (' in `%s`' % r['guard_file']) if r.get('guard_file') else ''
                out.append('- **What stops it now.** %s%s' % (r['guard'], gf))
            else:
                out.append('- **What stops it now.** Nothing automated. This one is still carried by attention.')
            if r.get('cost'):
                out.append('- **Cost.** %s' % r['cost'])
            out.append('- **Lesson.** %s' % r['lesson'])
            out.append('')
    return '\n'.join(out)


def analysis_chapter(rows):
    """What the ledger says about itself. This is the part a handwritten guide cannot do,
    because it requires counting the whole ledger every time it changes."""
    n = len(rows)
    by_det = {}
    by_sev = {}
    by_area = {}
    for r in rows:
        by_det[r['detection_class']] = by_det.get(r['detection_class'], 0) + 1
        by_sev[r['severity']] = by_sev.get(r['severity'], 0) + 1
        by_area[r['area']] = by_area.get(r['area'], 0) + 1

    guarded = [r for r in rows if r.get('guard')]
    unguarded = [r for r in rows if not r.get('guard')]

    # Two incidents pointing at one guard means the guard is not working. This is the
    # recurrence signal, and it is computed rather than remembered.
    byguard = {}
    for r in guarded:
        byguard.setdefault(r['guard_file'] or r['guard'], []).append(r['id'])
    repeats = {k: v for k, v in byguard.items() if len(v) > 1}

    pre = [r for r in rows if r['detection_class'] in ('review', 'test', 'measurement', 'render', 'adversarial-review', 'build-guard')]

    o = ['# What the Ledger Says About Itself\n']
    o.append('%d recorded defects, over %s days of building. This chapter is computed from the '
             'ledger every time the document is built, so it cannot fall out of step with it.\n' % (n, '{{ELAPSED_DAYS}}'))

    o.append('\n## How defects were actually found\n')
    o.append('| How | Count | Share |')
    o.append('| --- | ---: | ---: |')
    for k, v in sorted(by_det.items(), key=lambda kv: -kv[1]):
        o.append('| %s | %d | %d%% |' % (DET_LABEL[k], v, round(v * 100.0 / n)))
    o.append('')
    o.append('**This is the most useful table in the book.** %d of %d defects, %d percent, were '
             'caught by something other than a person hitting them in production. The single '
             'largest category is not a clever tool: it is reading the built output instead of '
             'the source that produced it. The second is measuring a number nobody had measured '
             'before. Neither requires infrastructure, and both are habits rather than tools.\n'
             % (len(pre), n, round(len(pre) * 100.0 / n)))
    o.append('**Read that percentage with the bias it carries.** This ledger is written by the '
             'people who found the defects, so it counts what was caught and cannot count what '
             'was not. A defect a user hit and nobody recorded does not appear here. The honest '
             'reading is not "97 percent of all defects were caught early"; it is "of the '
             'defects we know about, almost all surfaced through one of these five habits", '
             'which is still the useful claim, because it says where to spend attention.\n')

    o.append('\n## By severity\n')
    o.append('| Severity | Count |')
    o.append('| --- | ---: |')
    for k, v in sorted(by_sev.items(), key=lambda kv: -kv[1]):
        o.append('| %s | %d |' % (SEV_LABEL[k], v))
    o.append('')
    sl = by_sev.get('silent-loss', 0)
    o.append('**Silent loss is the dominant failure mode**, at %d of %d. Not a crash, not an error '
             'page: something quietly did less than it claimed. A loop over an empty list, a filter '
             'that dropped rows, a guard that stopped checking, a table that never received a write. '
             'None of these announce themselves, and none are caught by error monitoring, which is '
             'why the guard ladder in this book is built around asserting counts rather than '
             'catching exceptions.\n' % (sl, n))

    o.append('\n## By area\n')
    o.append('| Area | Count |')
    o.append('| --- | ---: |')
    for k, v in sorted(by_area.items(), key=lambda kv: -kv[1]):
        o.append('| %s | %d |' % (AREA_LABEL[k], v))
    o.append('')

    o.append('\n## Guard coverage\n')
    o.append('%d of %d defects produced an automated guard. %d did not, and are carried by '
             'attention alone, which means they are the ones most likely to recur.\n'
             % (len(guarded), n, len(unguarded)))
    if unguarded:
        o.append('Carried by attention:\n')
        for r in unguarded:
            o.append('- **%s** %s' % (r['id'], r['title']))
        o.append('')
    if repeats:
        o.append('\n## Guards that fired twice\n')
        o.append('A guard named by two incidents is a guard that did not hold the first time. '
                 'These are the places to spend effort.\n')
        for k, v in sorted(repeats.items(), key=lambda kv: -len(kv[1])):
            o.append('- `%s` appears in %s' % (k, ', '.join(v)))
        o.append('')
    else:
        o.append('\nNo guard appears in more than one incident yet. When one does, it will be '
                 'listed here automatically, and it will mean that guard needs rebuilding rather '
                 'than trusting.\n')
    return '\n'.join(o)


def checklist_chapter(rows):
    """Generated from the ledger, never written by hand. A new incident becomes a line here
    the next time this runs."""
    o = ['# The Checklist\n']
    o.append('Generated from the defect ledger. Every line exists because something went wrong '
             'once. Nothing is here for completeness.\n')
    o.append('Read it before starting a piece of work in the matching area, and again before '
             'you push.\n')
    by_area = {}
    for r in rows:
        by_area.setdefault(r['area'], []).append(r)
    for area in sorted(by_area, key=lambda a: AREA_LABEL[a]):
        o.append('\n## %s\n' % AREA_LABEL[area])
        for r in by_area[area]:
            o.append('- [ ] %s  \n  <small>%s (%s)</small>' % (r['lesson'], r['title'], r['id']))
        o.append('')
    return '\n'.join(o)


# ---------------------------------------------------------------------------- render ---

def md_to_html(md):
    """A small, predictable Markdown subset. Not a general renderer: it handles exactly the
    constructs the chapters use, and anything it does not handle would be a silent
    mis-render, so unknown syntax is left as literal text rather than guessed at."""
    lines = md.split('\n')
    out, i = [], 0
    in_ul = in_ol = False
    in_code = False
    in_table = False

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            out.append('</ul>'); in_ul = False
        if in_ol:
            out.append('</ol>'); in_ol = False

    def close_table():
        nonlocal in_table
        if in_table:
            out.append('</tbody></table></div>'); in_table = False

    def inline(s):
        s = html.escape(s, quote=False)
        s = re.sub(r'`([^`]+)`', lambda m: '<code>%s</code>' % m.group(1), s)
        s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
        s = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', s)
        s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
        return s

    while i < len(lines):
        ln = lines[i]
        if ln.strip().startswith('```'):
            if in_code:
                out.append('</code></pre>'); in_code = False
            else:
                close_lists(); close_table()
                out.append('<pre><code>'); in_code = True
            i += 1
            continue
        if in_code:
            out.append(html.escape(ln, quote=False))
            i += 1
            continue

        if re.match(r'^\|.*\|\s*$', ln) and i + 1 < len(lines) and re.match(r'^\|[\s:\-|]+\|\s*$', lines[i + 1]):
            close_lists()
            cells = [c.strip() for c in ln.strip().strip('|').split('|')]
            aligns = [c.strip() for c in lines[i + 1].strip().strip('|').split('|')]
            def al(a):
                return 'right' if a.endswith(':') and not a.startswith(':') else ('center' if a.startswith(':') and a.endswith(':') else 'left')
            out.append('<div class="tw"><table><thead><tr>' + ''.join(
                '<th style="text-align:%s">%s</th>' % (al(aligns[k] if k < len(aligns) else ''), inline(c))
                for k, c in enumerate(cells)) + '</tr></thead><tbody>')
            in_table = True
            i += 2
            while i < len(lines) and re.match(r'^\|.*\|\s*$', lines[i]):
                rc = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                out.append('<tr>' + ''.join(
                    '<td style="text-align:%s">%s</td>' % (al(aligns[k] if k < len(aligns) else ''), inline(c))
                    for k, c in enumerate(rc)) + '</tr>')
                i += 1
            close_table()
            continue

        m = re.match(r'^(#{1,4})\s+(.*)$', ln)
        if m:
            close_lists(); close_table()
            lvl = len(m.group(1))
            txt = m.group(2).strip()
            anchor = re.sub(r'[^a-z0-9]+', '-', txt.lower()).strip('-')
            out.append('<h%d id="%s">%s</h%d>' % (lvl, anchor, inline(txt), lvl))
            i += 1
            continue

        m = re.match(r'^\s*[-*]\s+(.*)$', ln)
        if m:
            close_table()
            if in_ol:
                out.append('</ol>'); in_ol = False
            if not in_ul:
                out.append('<ul>'); in_ul = True
            out.append('<li>%s</li>' % inline(m.group(1)))
            i += 1
            continue

        m = re.match(r'^\s*\d+\.\s+(.*)$', ln)
        if m:
            close_table()
            if in_ul:
                out.append('</ul>'); in_ul = False
            if not in_ol:
                out.append('<ol>'); in_ol = True
            out.append('<li>%s</li>' % inline(m.group(1)))
            i += 1
            continue

        if ln.strip() == '---':
            close_lists(); close_table()
            out.append('<hr>')
            i += 1
            continue

        if not ln.strip():
            close_lists(); close_table()
            i += 1
            continue

        close_lists(); close_table()
        buf = [ln]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#{1,4}\s|\s*[-*]\s|\s*\d+\.\s|\||```|---$)', lines[i]):
            buf.append(lines[i])
            i += 1
        out.append('<p>%s</p>' % inline(' '.join(x.strip() for x in buf)))

    close_lists(); close_table()
    if in_code:
        out.append('</code></pre>')
    return '\n'.join(out)


CSS = """
:root{--ink:#111827;--ink2:#374151;--mut:#6b7280;--rule:#e5e7eb;--navy:#122B4E;
--bg:#ffffff;--soft:#f8fafc;--code:#f1f5f9;--accent:#0072B2;--max:46rem}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);
 font:16px/1.65 "IBM Plex Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:var(--max);margin:0 auto;padding:0 20px 120px}
h1,h2,h3,h4{font-family:"Source Serif 4",Georgia,"Times New Roman",serif;
 color:var(--navy);line-height:1.2;letter-spacing:-.02em;margin:2.2em 0 .5em}
h1{font-size:2.1rem;letter-spacing:-.028em;margin-top:2.6em;padding-top:1.4em;border-top:2px solid var(--navy)}
h2{font-size:1.45rem}h3{font-size:1.12rem;letter-spacing:-.012em}h4{font-size:1rem}
p,li{color:var(--ink2)}
p{margin:0 0 1em}
ul,ol{margin:0 0 1.1em;padding-left:1.3em}
li{margin:.3em 0}
li>small{color:var(--mut);font-size:.82em}
code{font-family:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
 font-size:.86em;background:var(--code);padding:.12em .35em;border-radius:4px;
 word-break:break-word}
pre{background:var(--code);border:1px solid var(--rule);border-radius:8px;
 padding:14px 16px;overflow-x:auto;margin:0 0 1.2em}
pre code{background:none;padding:0;font-size:.8rem;line-height:1.55}
.tw{overflow-x:auto;margin:0 0 1.3em}
table{border-collapse:collapse;width:100%;font-size:.92rem}
th,td{border-bottom:1px solid var(--rule);padding:8px 10px;vertical-align:top}
th{color:var(--navy);font-weight:600;text-align:left;border-bottom:2px solid var(--rule);
 font-size:.78rem;letter-spacing:.06em;text-transform:uppercase}
td{color:var(--ink2)}
hr{border:0;border-top:1px solid var(--rule);margin:2.4em 0}
strong{color:var(--ink);font-weight:600}
a{color:var(--accent)}
.cover{padding:16vh 0 8vh;border-bottom:1px solid var(--rule);margin-bottom:1em}
.cover h1{border:0;padding:0;margin:0 0 .35em;font-size:2.9rem;letter-spacing:-.032em}
.cover .sub{font-size:1.06rem;color:var(--mut);max-width:34rem;margin:0 0 2.2em}
.cover .meta{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.78rem;
 color:var(--mut);letter-spacing:.02em}
.eyebrow{font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);
 margin:0 0 1.4em;font-weight:600}
.toc{background:var(--soft);border:1px solid var(--rule);border-radius:10px;padding:18px 22px;margin:0 0 2em}
.toc ol{margin:0;padding-left:1.2em}
.toc a{color:var(--navy);text-decoration:none}
.toc a:hover{text-decoration:underline}
@media print{
 body{font-size:10.5pt}
 .wrap{max-width:none;padding:0}
 h1{page-break-before:always;border-top:0;padding-top:0;margin-top:0}
 .cover h1,.toc+h1{page-break-before:avoid}
 h1,h2,h3{page-break-after:avoid}
 pre,table,li{page-break-inside:avoid}
 .cover{padding:6cm 0 2cm;page-break-after:always;border:0}
 a{color:var(--ink);text-decoration:none}
}
@media (max-width:640px){.wrap{padding:0 16px 80px}.cover{padding:8vh 0 5vh}.cover h1{font-size:2.1rem}}
"""


def build_html(body_html, h, nchapters, nincidents):
    toc_items = re.findall(r'<h1 id="([^"]+)">(.*?)</h1>', body_html)
    toc = '\n'.join('<li><a href="#%s">%s</a></li>' % (a, t) for a, t in toc_items)
    return """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>%s</title><style>%s</style></head><body><div class="wrap">
<div class="cover">
<p class="eyebrow">Start From Nowhere</p>
<h1>%s</h1>
<p class="sub">%s</p>
<p class="meta">Built %s from commit %s &middot; %s commits over %s days &middot; %s recorded defects &middot; %s chapters<br>
This document is generated. Edit the chapters in docs/playbook/ and the ledger in data/playbook/incidents.jsonl, then run python3 src/build_playbook.py.</p>
</div>
<div class="toc"><ol>%s</ol></div>
%s
</div></body></html>""" % (html.escape(TITLE), CSS, html.escape(TITLE), html.escape(SUBTITLE),
                           h['BUILT_ON'], h['HEAD_SHA'], h['COMMITS'], h['ELAPSED_DAYS'],
                           nincidents, nchapters, toc, body_html)


# ------------------------------------------------------------------------- bootstrap ---
#
# The pack that starts a new project with this one's scars already loaded. Generated from
# the same ledger as the book, so the digest cannot drift from the chapter that explains
# it. See docs/playbook/16_bootstrap.md for why it is layered this way rather than pasted
# whole: reference material and operating instructions are different artefacts and need
# different delivery.

CLAUDE_TEMPLATE = """# [PROJECT NAME]: standing rules for every session

Owner: [OWNER NAME]. Live site: [DOMAIN]. Read ROADMAP.md for the current build schedule
before writing anything.

[ONE SENTENCE ON WHAT THIS PRODUCT IS AND WHO IT IS FOR.]

Nothing in this file is settled while the product is still being built. These are the
current decisions and the reasons behind them, not law: say so when one of them looks
wrong, and change it when the owner says to rather than quoting it back at them.

## Never invent a value (non-negotiable)

- Every identifier, hash, id, count, price, date, URL and statistic that goes into a tool
  call, a commit, a page or a message must be READ from real output first: a command
  result, a file, a tool response. Never type one from memory, pattern, or plausibility.
- If the real value is not to hand, run the command that produces it. That costs one tool
  call. Guessing costs correctness.
- A number that looks right is the hardest kind of wrong to catch.

## Communication (non-negotiable)

- If a link, site, or service cannot be accessed for any reason, say so IMMEDIATELY and
  ask how to proceed BEFORE doing the work another way. Never quietly substitute partial
  information for the source that was pointed to.
- Report what broke on the way, not only what was built. That is the most valuable part of
  a report and the easiest to omit because it reads as failure.

## House style (the build enforces these)

- NO em dashes and NO en dashes anywhere: pages, posts, code strings, data files, commit
  messages. A single grep then decides whether copy was written or pasted.
- Headers are Title Case. Body copy, descriptions and table cells are sentence case.
- [YOUR OTHER STYLE RULES HERE. Only ones a build can check.]

## Sourcing (delete this whole block if you publish no external facts)

- Never state an external statistic, price or fact from memory. Every published figure
  carries source, year and URL; unverifiable means null or a dash, never a guess.
- Banned sources: [LIST THEM]. The build fails if one appears.
- Never fabricate product stats, user counts, testimonials or efficacy claims.
- Never present an internal threshold or heuristic as official.

## Engineering workflow

- Develop on a feature branch; ship via PR; squash merge; main deploys.
- The build is the guard rail. Every guard lives in the build, because the build is the
  only thing that sees the artefact.
- Sources of truth live in one place. Generated output is gitignored so nothing is
  hand-edited.
- Reach for a design token before a number.
- Grid and flex children need min-width:0.
- Row Level Security on every table from creation. Revoke from PUBLIC as well as anon and
  authenticated. Every privileged read goes through a SECURITY DEFINER function.
- Never take an id from a request body; read it from the caller's own scoped row.
- Never commit a secret key or signing secret.

## The defect ledger

- When something breaks, append a record to data/playbook/incidents.jsonl BEFORE fixing
  it, while you still remember what you believed was true five minutes ago. That belief is
  the actual defect and it is the first thing you lose.
- python3 src/build_playbook.py regenerates the playbook, the checklist and the rules
  digest from those records. Nothing is copied by hand.

## Architecture, and the parts that will surprise you

[EMPTY AT THE START. Add only facts that are expensive to rediscover, as you discover
them. Not documentation: the handful of things that would cost a session an hour.]
"""

KICKOFF = """# Kickoff

You are building a new product with me. Before anything else, read RULES_DIGEST.md in
this project: it is {N} real defects from a previous build of a comparable platform,
compressed to one rule each. Those rules are the accumulated cost of {DAYS} days of
building, and following them is cheaper than rediscovering them.

## The working agreement

- I decide what to build, what it means and what is acceptable. You decide how.
- You do not check in on each item. Work continuously and batch the reporting.
- Anything irreversible or outward-facing, ask first: deleting data, changing a live
  payment configuration, publishing something, sending anything to a third party.
- Merge your own work once the checks are green. Stop immediately when I say stop.
- Never invent a value. Read every id, hash, count, date and URL from real output.
- If something is blocked or unreachable, tell me at the moment it happens.

## The order of work

Do these in order. Most of what goes wrong goes wrong because something was done before
the thing that would have caught it.

1. **The rules file.** Copy CLAUDE.template.md to CLAUDE.md and fill in the blanks with me.
2. **The build.** A script that turns sources into output, even if it does almost nothing
   on day one. Every guard will live here.
3. **One page, deployed to the real host on the real domain.** Learn the platform's limits
   now: per-file size, which directories the uploader walks, whether www and the apex are
   one origin, whether the headers file applies to responses your own code generates.
4. **The data layer**, with RLS on every table from creation, and one SQL smoke test that
   asserts a guarantee and rolls itself back.
5. **The design token file.** The complete palette in both themes, the type scale, the
   spacing grid. All of it, before the second page exists.
6. **The product.**
7. **Instrumentation**, before spending anything on acquisition.
8. **Payments**, last. The append-only billing event ledger goes in BEFORE the first real
   subscriber, because it cannot be reconstructed afterwards.

## What to report back

Not a list of files changed. Report:

1. What was built, in one paragraph.
2. What broke on the way, and why. Append each one to data/playbook/incidents.jsonl.
3. What is now guarded against, and in which file.
4. What was left undone, and whether that is a decision or a blocker.
5. Numbers, with the command that produced them.

## Now

Here is what I want to build:

[DESCRIBE THE BUSINESS IDEA. What it is, who it is for, how it makes money, and what
would make it obviously better than what exists. Do not worry about technical detail; ask
me what you need.]

Before you write any code, tell me: the stack you propose and why, the first week's plan
against the order above, and the three things most likely to go wrong with this
particular idea.
"""


def rules_digest(rows, h):
    """The ledger compressed to operative rules. One line each, imperative, with the
    specifics of this codebase stripped out, because a rule competing with ten thousand
    words of context is a rule that gets applied inconsistently."""
    by_area = {}
    for r in rows:
        by_area.setdefault(r['area'], []).append(r)

    o = ['# Rules Digest',
         '',
         '%d defects from a previous build, each reduced to the rule that prevents it. '
         'Every line is the residue of something that actually broke and cost real time. '
         'The reasoning behind each is in BUILD_PLAYBOOK.md; look it up when a rule seems '
         'wrong rather than guessing at it.' % len(rows),
         '',
         'Generated %s from a ledger spanning %s days and %s commits.'
         % (h['BUILT_ON'], h['ELAPSED_DAYS'], h['COMMITS']),
         '']

    det = {}
    for r in rows:
        det[r['detection_class']] = det.get(r['detection_class'], 0) + 1
    top = sorted(det.items(), key=lambda kv: -kv[1])[:3]
    o.append('## Read this first')
    o.append('')
    o.append('The three ways defects were most often found, in order: %s. '
             'None of them is a tool. All three are habits: read the built output rather '
             'than the source that produced it, measure a number nobody has measured '
             'before, and render the thing and look at it.'
             % ', '.join('%s (%d)' % (DET_LABEL[k].lower(), v) for k, v in top))
    o.append('')
    sl = sum(1 for r in rows if r['severity'] == 'silent-loss')
    o.append('The dominant failure mode is silent loss, %d of %d: something quietly did '
             'less than it claimed. A loop over an empty list, a filter that dropped rows, '
             'a guard that stopped checking, a table that never received a write. None of '
             'these raise an error. Assert counts, not the absence of exceptions.'
             % (sl, len(rows)))
    o.append('')

    for area in sorted(by_area, key=lambda a: -len(by_area[a])):
        o.append('## %s' % AREA_LABEL[area])
        o.append('')
        for r in by_area[area]:
            o.append('- %s' % r['lesson'])
        o.append('')
    return '\n'.join(o)


def write_bootstrap(rows, h):
    d = os.path.join(OUT, 'bootstrap')
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, 'CLAUDE.template.md'), 'w', encoding='utf-8').write(CLAUDE_TEMPLATE)
    io.open(os.path.join(d, 'KICKOFF.md'), 'w', encoding='utf-8').write(
        KICKOFF.replace('{N}', str(len(rows))).replace('{DAYS}', h['ELAPSED_DAYS']))
    io.open(os.path.join(d, 'RULES_DIGEST.md'), 'w', encoding='utf-8').write(rules_digest(rows, h))
    shutil.copyfile(LEDGER, os.path.join(d, 'incidents.jsonl'))
    io.open(os.path.join(d, 'README.md'), 'w', encoding='utf-8').write(
        '# Bootstrap Pack\n\n'
        'Generated by src/build_playbook.py. Do not edit these by hand; edit the ledger '
        'and the chapters and rebuild.\n\n'
        '| File | Where it goes |\n| --- | --- |\n'
        '| `CLAUDE.template.md` | The new repository root, renamed CLAUDE.md, with the four blanks filled in. '
        'On claude.ai, the project custom instructions. |\n'
        '| `KICKOFF.md` | The first message of the first conversation, with your idea pasted underneath. |\n'
        '| `RULES_DIGEST.md` | Project knowledge, or pasted before the kickoff if there is no project. |\n'
        '| `incidents.jsonl` | The new repository at data/playbook/incidents.jsonl, so it starts appending rather than starting empty. |\n'
        '| `../BUILD_PLAYBOOK.md` | Project knowledge, retrieved on demand. Do not paste it into the prompt. |\n\n'
        'Copy `src/build_playbook.py` across as well, so the new project turns its own '
        'ledger into its own book from the first defect.\n')
    return d


# ------------------------------------------------------------------------------ docx ---
#
# Written directly as Office Open XML. A .docx is a zip of XML parts, and writing it by
# hand costs about a hundred lines and removes a dependency the rest of this repository
# does not have. The site itself ships with no runtime dependencies; the document about
# building it should not need one either.

def xml_esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def docx_runs(text):
    """Inline markup to Word runs. Handles bold, italic and code, which is all the chapters
    use. Anything else is emitted as plain text rather than silently dropped."""
    parts = re.split(r'(\*\*[^*]+\*\*|`[^`]+`|\*[^*\n]+\*|\[[^\]]+\]\([^)]+\))', text)
    runs = []
    for p in parts:
        if not p:
            continue
        if p.startswith('**') and p.endswith('**') and len(p) > 4:
            runs.append('<w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % xml_esc(p[2:-2]))
        elif p.startswith('`') and p.endswith('`') and len(p) > 2:
            runs.append('<w:r><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="19"/></w:rPr>'
                        '<w:t xml:space="preserve">%s</w:t></w:r>' % xml_esc(p[1:-1]))
        elif p.startswith('*') and p.endswith('*') and len(p) > 2:
            runs.append('<w:r><w:rPr><w:i/></w:rPr><w:t xml:space="preserve">%s</w:t></w:r>' % xml_esc(p[1:-1]))
        else:
            m = re.match(r'\[([^\]]+)\]\(([^)]+)\)', p)
            if m:
                runs.append('<w:r><w:t xml:space="preserve">%s</w:t></w:r>' % xml_esc(m.group(1)))
            else:
                runs.append('<w:r><w:t xml:space="preserve">%s</w:t></w:r>' % xml_esc(p))
    return ''.join(runs) or '<w:r><w:t/></w:r>'


def docx_body(md):
    lines = md.split('\n')
    body, i = [], 0
    in_code = False
    code_buf = []
    while i < len(lines):
        ln = lines[i]
        if ln.strip().startswith('```'):
            if in_code:
                for cl in code_buf:
                    body.append('<w:p><w:pPr><w:pStyle w:val="Code"/></w:pPr>'
                                '<w:r><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="18"/></w:rPr>'
                                '<w:t xml:space="preserve">%s</w:t></w:r></w:p>' % xml_esc(cl))
                code_buf = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue
        if in_code:
            code_buf.append(ln)
            i += 1
            continue

        if re.match(r'^\|.*\|\s*$', ln) and i + 1 < len(lines) and re.match(r'^\|[\s:\-|]+\|\s*$', lines[i + 1]):
            rows = []
            hdr = [c.strip() for c in ln.strip().strip('|').split('|')]
            rows.append((hdr, True))
            i += 2
            while i < len(lines) and re.match(r'^\|.*\|\s*$', lines[i]):
                rows.append(([c.strip() for c in lines[i].strip().strip('|').split('|')], False))
                i += 1
            cells = '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/>' \
                    '<w:tblW w:w="5000" w:type="pct"/>' \
                    '<w:tblBorders>' + ''.join(
                        '<w:%s w:val="single" w:sz="4" w:space="0" w:color="D9D9D9"/>' % e
                        for e in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV')) + \
                    '</w:tblBorders></w:tblPr>'
            for rc, is_h in rows:
                cells += '<w:tr>'
                for c in rc:
                    runs = docx_runs('**%s**' % c if is_h else c)
                    cells += '<w:tc><w:tcPr><w:tcW w:w="0" w:type="auto"/></w:tcPr>' \
                             '<w:p><w:pPr><w:spacing w:before="40" w:after="40"/></w:pPr>%s</w:p></w:tc>' % runs
                cells += '</w:tr>'
            cells += '</w:tbl><w:p/>'
            body.append(cells)
            continue

        m = re.match(r'^(#{1,4})\s+(.*)$', ln)
        if m:
            lvl = min(len(m.group(1)), 4)
            body.append('<w:p><w:pPr><w:pStyle w:val="Heading%d"/>%s</w:pPr>%s</w:p>'
                        % (lvl, '<w:pageBreakBefore/>' if lvl == 1 else '', docx_runs(m.group(2).strip())))
            i += 1
            continue

        m = re.match(r'^\s*[-*]\s+(.*)$', ln)
        if m:
            body.append('<w:p><w:pPr><w:pStyle w:val="ListParagraph"/>'
                        '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr></w:pPr>%s</w:p>'
                        % docx_runs(re.sub(r'<small>|</small>', '', m.group(1))))
            i += 1
            continue

        m = re.match(r'^\s*\d+\.\s+(.*)$', ln)
        if m:
            body.append('<w:p><w:pPr><w:pStyle w:val="ListParagraph"/>'
                        '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="2"/></w:numPr></w:pPr>%s</w:p>'
                        % docx_runs(m.group(1)))
            i += 1
            continue

        if not ln.strip() or ln.strip() == '---':
            i += 1
            continue

        buf = [ln]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#{1,4}\s|\s*[-*]\s|\s*\d+\.\s|\||```|---$)', lines[i]):
            buf.append(lines[i])
            i += 1
        body.append('<w:p>%s</w:p>' % docx_runs(' '.join(x.strip() for x in buf)))
    return ''.join(body)


DOCX_STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr>
<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="21"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="140" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault>
</w:docDefaults>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:pPr><w:spacing w:after="240"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Georgia" w:hAnsi="Georgia"/><w:b/><w:color w:val="122B4E"/><w:sz w:val="56"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/>
<w:rPr><w:color w:val="6B7280"/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:pPr><w:spacing w:before="360" w:after="180"/><w:outlineLvl w:val="0"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Georgia" w:hAnsi="Georgia"/><w:b/><w:color w:val="122B4E"/><w:sz w:val="40"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:pPr><w:spacing w:before="300" w:after="140"/><w:outlineLvl w:val="1"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Georgia" w:hAnsi="Georgia"/><w:b/><w:color w:val="122B4E"/><w:sz w:val="30"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:pPr><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="2"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Georgia" w:hAnsi="Georgia"/><w:b/><w:color w:val="122B4E"/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading4"><w:name w:val="heading 4"/><w:pPr><w:spacing w:before="200" w:after="100"/><w:outlineLvl w:val="3"/></w:pPr>
<w:rPr><w:b/><w:color w:val="122B4E"/><w:sz w:val="22"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/>
<w:pPr><w:ind w:left="480"/><w:spacing w:after="80"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Code"><w:name w:val="Code"/>
<w:pPr><w:shd w:val="clear" w:fill="F1F5F9"/><w:spacing w:after="0"/><w:ind w:left="240"/></w:pPr></w:style>
<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/></w:style>
</w:styles>"""

DOCX_NUMBERING = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/>
<w:lvlText w:val="&#8226;"/><w:lvlJc w:val="left"/>
<w:pPr><w:ind w:left="480" w:hanging="240"/></w:pPr></w:lvl></w:abstractNum>
<w:abstractNum w:abstractNumId="1"><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/>
<w:lvlText w:val="%1."/><w:lvlJc w:val="left"/>
<w:pPr><w:ind w:left="480" w:hanging="240"/></w:pPr></w:lvl></w:abstractNum>
<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>
<w:num w:numId="2"><w:abstractNumId w:val="1"/></w:num>
</w:numbering>"""


def write_docx(path, md, h):
    cover = ('<w:p><w:pPr><w:pStyle w:val="Title"/></w:pPr><w:r><w:t>%s</w:t></w:r></w:p>'
             '<w:p><w:pPr><w:pStyle w:val="Subtitle"/></w:pPr><w:r><w:t>%s</w:t></w:r></w:p>'
             '<w:p><w:r><w:rPr><w:color w:val="6B7280"/><w:sz w:val="18"/></w:rPr><w:t>%s</w:t></w:r></w:p>'
             % (xml_esc(TITLE), xml_esc(SUBTITLE),
                xml_esc('Built %s from commit %s. %s commits over %s days. This document is generated: '
                        'edit docs/playbook/ and data/playbook/incidents.jsonl, then run '
                        'python3 src/build_playbook.py.'
                        % (h['BUILT_ON'], h['HEAD_SHA'], h['COMMITS'], h['ELAPSED_DAYS']))))
    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
           '<w:body>%s%s<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
           '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"/></w:sectPr>'
           '</w:body></w:document>' % (cover, docx_body(md)))

    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
          '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
          '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
          '</Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '</Relationships>')
    drels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
             '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'
             '</Relationships>')
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', ct)
        z.writestr('_rels/.rels', rels)
        z.writestr('word/document.xml', doc)
        z.writestr('word/_rels/document.xml.rels', drels)
        z.writestr('word/styles.xml', DOCX_STYLES)
        z.writestr('word/numbering.xml', DOCX_NUMBERING)


# ------------------------------------------------------------------------------ main ---

def main():
    if not os.path.isdir(CHAPTERS):
        raise SystemExit('no chapters at %s' % CHAPTERS)
    h = harvest()
    rows = load_incidents()

    problems = validate_incidents(rows)
    if problems:
        print('The defect ledger does not check out:')
        for p in problems:
            print('  ' + p)
        raise SystemExit(1)

    files = sorted(glob.glob(os.path.join(CHAPTERS, '*.md')))
    parts = []
    for f in files:
        txt = io.open(f, encoding='utf-8').read()
        if '{{LEDGER}}' in txt:
            txt = txt.replace('{{LEDGER}}', ledger_chapter(rows))
        if '{{ANALYSIS}}' in txt:
            txt = txt.replace('{{ANALYSIS}}', analysis_chapter(rows))
        if '{{CHECKLIST}}' in txt:
            txt = txt.replace('{{CHECKLIST}}', checklist_chapter(rows))
        parts.append(txt.rstrip() + '\n')
    md = '\n\n'.join(parts)

    h['INCIDENT_COUNT'] = str(len(rows))
    h['CHAPTER_COUNT'] = str(len(files))

    # Substitute after assembly so a generated chapter can use a harvest key too.
    for k, v in h.items():
        md = md.replace('{{%s}}' % k, v)

    # Prose legitimately talks about placeholders as a concept, and the chapters quote
    # real ones by name. Anything inside a code span or a fenced block is an example, not
    # a substitution site, so it is blanked before the leftover check rather than being
    # allowlisted, which would go stale.
    scan = re.sub(r'```.*?```', '', md, flags=re.S)
    scan = re.sub(r'`[^`\n]*`', '', scan)
    left = sorted(set(re.findall(r'\{\{([A-Z_]+)\}\}', scan)))
    if left:
        raise SystemExit('unresolved placeholders, nothing was written: %s' % ', '.join(left))

    # The house rule, applied to the document about the house rules.
    for ch in ('\u2014', '\u2013'):
        if ch in md:
            n = md.count(ch)
            raise SystemExit('%d em or en dash(es) in the playbook; CLAUDE.md bans them' % n)

    os.makedirs(OUT, exist_ok=True)
    io.open(os.path.join(OUT, 'BUILD_PLAYBOOK.md'), 'w', encoding='utf-8').write(md)

    body = md_to_html(md)
    page = build_html(body, h, len(files), len(rows))
    io.open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page)

    write_docx(os.path.join(OUT, 'BUILD_PLAYBOOK.docx'), md, h)
    bdir = write_bootstrap(rows, h)

    words = len(re.findall(r'\S+', re.sub(r'`[^`]*`', ' ', md)))
    print('playbook: %d chapters, %d incidents, %s words' % (len(files), len(rows), '{:,}'.format(words)))
    print('  playbook/BUILD_PLAYBOOK.md    %6.1f KB' % (os.path.getsize(os.path.join(OUT, 'BUILD_PLAYBOOK.md')) / 1024.0))
    print('  playbook/index.html           %6.1f KB' % (os.path.getsize(os.path.join(OUT, 'index.html')) / 1024.0))
    print('  playbook/BUILD_PLAYBOOK.docx  %6.1f KB' % (os.path.getsize(os.path.join(OUT, 'BUILD_PLAYBOOK.docx')) / 1024.0))
    print('  playbook/bootstrap/           %d files, %.1f KB'
          % (len(os.listdir(bdir)), sum(os.path.getsize(os.path.join(bdir, f)) for f in os.listdir(bdir)) / 1024.0))
    return 0


if __name__ == '__main__':
    sys.exit(main())
