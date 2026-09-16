# Shared site chrome: one header and one footer, identical on every page.
# Templates carry {{CHROME_CSS}}, {{SITE_HEADER}} and {{SITE_FOOTER}}; build
# scripts call apply_chrome() so the markup can never drift between pages.

LOGO_SVG = (
    '<svg viewBox="0 0 48 48" width="28" height="28" aria-hidden="true">'
    '<rect width="48" height="48" rx="12" fill="#122B4E"/>'
    '<path d="M13 33 22 22l6 5 8.5-10" fill="none" stroke="#fff" stroke-width="3.4" '
    'stroke-linecap="round" stroke-linejoin="round"/>'
    '<path d="M29.5 16.5H37V24" fill="none" stroke="#fff" stroke-width="3.4" '
    'stroke-linecap="round" stroke-linejoin="round"/></svg>'
)

CHROME_CSS = """
/* shared chrome from src/partials.py; edit there, never per page */
.sfnh{position:sticky;top:0;z-index:50;background:#fff;border-bottom:1px solid #DCE5F1}
.sfnh-in{max-width:1200px;margin:0 auto;padding:0 24px;height:60px;display:flex;align-items:center;justify-content:space-between;gap:16px}
.sfnh-l{display:flex;align-items:center;gap:18px;min-width:0}
.sfn-wordmark{display:flex;align-items:center;gap:9px;font-family:'Source Serif 4',Georgia,serif;font-weight:700;font-size:19px;color:#0C1F3A;text-decoration:none;white-space:nowrap;letter-spacing:0}
nav.sfn-nav{display:flex;align-items:center}
.sfn-dd{position:relative}
.sfn-dd>button{display:flex;align-items:center;gap:4px;padding:8px 12px;font-family:Manrope,system-ui,sans-serif;font-weight:600;font-size:13px;color:#374151;background:none;border:none;cursor:pointer;line-height:1.2;transition:color 120ms ease}
.sfn-dd>button:hover{color:#0C1F3A}
.sfn-dd .car{font-size:9px;color:#6B7280;transition:transform 150ms ease}
.sfn-dd:hover .car,.sfn-dd:focus-within .car{transform:rotate(180deg)}
.sfn-dd-menu{position:absolute;top:100%;left:0;width:276px;background:#fff;border:1px solid #DCE5F1;border-radius:12px;box-shadow:0 10px 30px rgba(8,21,39,.12);padding:4px;display:none;z-index:60}
.sfn-dd:hover .sfn-dd-menu,.sfn-dd:focus-within .sfn-dd-menu{display:block}
.sfn-dd-menu a{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:9px 12px;border-radius:8px;font-family:Manrope,system-ui,sans-serif;font-weight:600;font-size:13px;color:#374151;text-decoration:none;white-space:nowrap}
.sfn-dd-menu a:hover{background:#F2F6FB;color:#0C1F3A}
.sfn-tag{font-family:Manrope,system-ui,sans-serif;font-size:10px;font-weight:700;padding:2px 8px;border-radius:999px;background:#F2F6FB;color:#6B7280;white-space:nowrap;flex-shrink:0}
.sfn-tag.live{background:#16A34A;color:#fff}
.sfnh-r{display:flex;align-items:center;gap:8px}
.sfn-signin{font-family:Manrope,system-ui,sans-serif;font-weight:600;font-size:13px;color:#6B7280;text-decoration:none;padding:8px 12px;border-radius:8px;transition:color 120ms ease}
.sfn-signin:hover{color:#0C1F3A}
.sfn-cta{font-family:Manrope,system-ui,sans-serif;font-weight:700;font-size:13px;background:#122B4E;color:#fff;text-decoration:none;padding:9px 16px;border-radius:8px;transition:background 120ms ease;white-space:nowrap}
.sfn-cta:hover{background:#0C1F3A}
.sfn-burger{display:none;background:none;border:none;cursor:pointer;padding:8px;color:#374151}
.sfn-mobile{display:none;border-top:1px solid #DCE5F1;background:#fff;padding:12px 24px 16px}
.sfn-mobile a{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 12px;border-radius:8px;font-family:Manrope,system-ui,sans-serif;font-weight:600;font-size:14px;color:#374151;text-decoration:none}
.sfn-mobile a:hover{background:#F2F6FB;color:#0C1F3A}
.sfn-mobile .grp{font-family:Manrope,system-ui,sans-serif;font-weight:700;font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:#9CA3AF;padding:12px 12px 4px}
.sfn-mobile .mb-cta{display:block;text-align:center;background:#122B4E;color:#fff;font-weight:700;margin-top:10px}
.sfn-mobile .mb-cta:hover{background:#0C1F3A;color:#fff}
@media(max-width:1023px){nav.sfn-nav,.sfn-signin,.sfn-cta{display:none}.sfn-burger{display:inline-flex}}
.sfnf{border-top:1px solid #DCE5F1;background:#F9FAFB;margin-top:48px}
.sfnf-in{max-width:1200px;margin:0 auto;padding:34px 24px 24px;display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap}
.sfnf-links{display:flex;gap:22px;flex-wrap:wrap;justify-content:center}
.sfnf-links a{font-family:Manrope,system-ui,sans-serif;font-weight:600;font-size:12.5px;color:#6B7280;text-decoration:none;transition:color 120ms ease}
.sfnf-links a:hover{color:#0C1F3A}
.sfnf-copy{font-family:Manrope,system-ui,sans-serif;font-size:12.5px;color:#9CA3AF;white-space:nowrap}
.sfnf-legal{max-width:1200px;margin:0 auto;padding:0 24px 28px;font-size:12px;color:#9CA3AF;line-height:1.6}
""".strip()

_NAV_GROUPS = [
    ("Exam Prep", [
        ("GMAT Focus Edition", "/exams/gmat/", "Live"),
        ("SAT", "/exams/sat/", "Live"),
        ("GRE General Test", "/exams/gre/", "Live"),
        ("LSAT", "/exams/lsat/", "Live"),
        ("ACT", "/exams/act/", "Live"),
        ("Executive Assessment", "/exams/executive-assessment/", "In Development"),
        ("MCAT", "/exams/mcat/", "In Development"),
        ("All Exam Guides", "/exams/", None),
    ]),
    ("Lists", [
        ("MBA Rankings", "/schools/", "Live"),
        ("College Rankings", "/colleges/", "Live"),
        ("Law Schools", "/schools/", "Coming Soon"),
        ("Medical Schools", "/schools/", "Coming Soon"),
    ]),
    ("Admissions", [
        ("Application Checklist", "/apply/", "Free"),
        ("International Applicants", "/international/", "New"),
        ("Paying for It", "/funding/", "New"),
        ("MBA Rankings", "/schools/", None),
        ("College Rankings", "/colleges/", None),
    ]),
    ("Resources", [
        ("The Study Room (Blog)", "/blog/", None),
        ("Exam Guides", "/exams/", None),
        ("How Scoring Works", "/scoring/", None),
        ("Compare Plans", "/pricing/", None),
        ("FAQ", "/#faq", None),
        ("Terms of Use", "/terms.html", None),
        ("Privacy Policy", "/privacy.html", None),
    ]),
    ("Community", [
        ("All Forums", "/community/", "Live"),
        ("GMAT Prep", "/community/#/c/gmat-prep", None),
        ("Study Logs", "/community/#/c/study-logs", None),
        ("Admissions", "/community/#/c/admissions", None),
        ("Question of the Day", "/community/#/c/question-of-the-day", None),
        ("Site Feedback", "/community/#/c/site-feedback", None),
    ]),
]


def _tag(label):
    if not label:
        return ""
    cls = "sfn-tag live" if label == "Live" else "sfn-tag"
    return '<span class="' + cls + '">' + label + "</span>"


def _menu(items):
    out = []
    for label, href, tag in items:
        out.append('<a href="' + href + '">' + label + _tag(tag) + "</a>")
    return "".join(out)


def header_html():
    nav = []
    for group, items in _NAV_GROUPS:
        nav.append(
            '<div class="sfn-dd"><button type="button" aria-haspopup="true">' + group +
            ' <span class="car">&#9660;</span></button><div class="sfn-dd-menu">' +
            _menu(items) + "</div></div>"
        )
    mobile = []
    for group, items in _NAV_GROUPS:
        mobile.append('<div class="grp">' + group + "</div>")
        mobile.append(_menu(items))
    mobile.append('<div class="grp">Account</div>')
    mobile.append('<a href="/app/">Sign In</a>')
    mobile.append('<a class="mb-cta" href="/app/#account">Create Account</a>')
    return (
        '<header class="sfnh"><div class="sfnh-in">'
        '<div class="sfnh-l"><a class="sfn-wordmark" href="/">' + LOGO_SVG + 'Start From Nowhere</a>'
        '<nav class="sfn-nav" aria-label="Main">' + "".join(nav) + "</nav></div>"
        '<div class="sfnh-r">'
        '<a class="sfn-signin" href="/app/">Sign In</a>'
        '<a class="sfn-cta" href="/app/#account">Create Account</a>'
        '<button class="sfn-burger" id="sfnBurger" type="button" aria-label="Menu" aria-expanded="false">'
        '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>'
        "</div></div>"
        '<div class="sfn-mobile" id="sfnMobile">' + "".join(mobile) + "</div></header>"
        "<script>(function(){var b=document.getElementById('sfnBurger'),m=document.getElementById('sfnMobile');"
        "if(!b||!m)return;b.addEventListener('click',function(){var on=m.style.display==='block';"
        "m.style.display=on?'none':'block';b.setAttribute('aria-expanded',on?'false':'true');});})();</script>"
    )


FOOTER_LINKS = [
    ("Pricing", "/pricing/"),
    ("Forum", "/community/"),
    ("Exam Guides", "/exams/"),
    ("MBA Rankings", "/schools/"),
    ("College Rankings", "/colleges/"),
    ("Application Checklist", "/apply/"),
    ("International", "/international/"),
    ("Paying for It", "/funding/"),
    ("Privacy", "/privacy.html"),
    ("Terms", "/terms.html"),
]

LEGAL_LINE = (
    "GMAT is a registered trademark of the Graduate Management Admission Council (GMAC). "
    "SAT is a trademark registered by the College Board. Neither organization endorses this "
    "product. Practice items are original; score bands are internal estimates, not official scores."
)


# ---------------------------------------------------------------------------
# Sentinel: the error beacon that every page carries.
#
# Stage one of the self-improving loop. A JavaScript error on a live page used to
# be invisible: the student gave up and left, and nothing recorded that it had
# happened. This reports the error to client_errors, which is insert-only from the
# browser and readable only through the is_admin gated admin_errors RPC.
#
# Three rules it must never break, because a broken error reporter is worse than
# none: it cannot throw (everything sits inside try/catch), it cannot loop (one
# report per signature per page view, ten reports maximum), and it cannot report
# its own failures.
#
# Same privacy posture as the analytics beacon: first party, no third parties, the
# raw IP never leaves the request (country and a salted hash are added by a
# trigger). Messages and stacks are capped server-side.

def build_id():
    """Short git sha when available, otherwise the build date. This is what pins a
    regression to the build that introduced it, so it is worth the subprocess."""
    import subprocess, datetime
    try:
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                             capture_output=True, text=True, timeout=5)
        if sha.returncode == 0 and sha.stdout.strip():
            return sha.stdout.strip()
    except Exception:
        pass
    return datetime.date.today().isoformat()


SENTINEL_URL = ("https://ftsqwbzhkzuudogkvoqa.supabase.co/rest/v1/client_errors"
                "?apikey=sb_publishable_GToT4fK6RiwCZpPFE3bGiw_ThXq9qel")


def sentinel_js(app_version=None):
    ver = app_version or build_id()
    return (
        "<!-- sfn sentinel: first-party error beacon, no third parties, raw IP never stored -->\n"
        "<script>(function(){try{\n"
        'var U="' + SENTINEL_URL + '",V="' + ver + '";\n'
        "var sid;try{sid=sessionStorage.getItem('sfn_sid');}catch(e){}\n"
        "// Collapse the variable parts of a message so the same bug groups as one cluster\n"
        "// however many different numbers, urls or quoted values it happens to carry.\n"
        "function sig(msg,src){var m=String(msg||'').slice(0,200)"
        ".replace(/https?:\\/\\/[^\\s)]+/g,'<url>')"
        ".replace(/0x[0-9a-f]+/gi,'<hex>')"
        ".replace(/\\b\\d+\\b/g,'<n>')"
        ".replace(/(['\"`])(?:(?!\\1).){0,60}\\1/g,'<str>').trim();\n"
        " var f=String(src||'').split('/').pop().split('?')[0].slice(0,60);\n"
        " return (f?f+': ':'')+m;}\n"
        "var seen={},n=0;\n"
        "function report(o){ if(n>=10||seen[o.signature]) return; seen[o.signature]=1; n++;\n"
        " o.path=location.pathname; o.app_version=V; o.sid=sid||null;\n"
        " o.device=/Mobi|Android/i.test(navigator.userAgent)?'mobile':'desktop';\n"
        " o.ua=(navigator.userAgent||'').slice(0,300);\n"
        " try{fetch(U,{method:'POST',headers:{'Content-Type':'application/json'},"
        "body:JSON.stringify(o),keepalive:true});}catch(e){} }\n"
        "addEventListener('error',function(e){ try{\n"
        " if(!e) return;\n"
        " // A resource that failed to load fires here with no message. Report it as its\n"
        " // own kind rather than as a script error, so the two never share a cluster.\n"
        " if(e.target&&e.target!==window&&(e.target.src||e.target.href)){\n"
        "  var u=String(e.target.src||e.target.href).slice(0,200);\n"
        "  return report({kind:'resource',message:'Failed to load '+(e.target.tagName||'?'),"
        "source:u,signature:sig('Failed to load '+(e.target.tagName||'?'),u)}); }\n"
        " var msg=e.message||'Script error.';\n"
        " report({kind:'error',message:String(msg).slice(0,500),source:(e.filename||'').slice(0,300),"
        "lineno:e.lineno||null,colno:e.colno||null,"
        "stack:(e.error&&e.error.stack?String(e.error.stack):'').slice(0,2000),"
        "signature:sig(msg,e.filename)});\n"
        " }catch(x){} },true);\n"
        "addEventListener('unhandledrejection',function(e){ try{\n"
        " var r=e&&e.reason, msg=(r&&(r.message||r))||'unhandled rejection';\n"
        " report({kind:'unhandledrejection',message:String(msg).slice(0,500),"
        "stack:(r&&r.stack?String(r.stack):'').slice(0,2000),signature:sig(msg,'')});\n"
        " }catch(x){} });\n"
        "}catch(e){}})();</script>"
    )


def footer_html(extra_legal=""):
    links = "".join('<a href="' + h + '">' + l + "</a>" for l, h in FOOTER_LINKS)
    legal = LEGAL_LINE + ((" " + extra_legal) if extra_legal else "")
    return (
        '<footer class="sfnf"><div class="sfnf-in">'
        '<a class="sfn-wordmark" href="/" style="font-size:16px">' + LOGO_SVG.replace('width="28" height="28"', 'width="24" height="24"') + "Start From Nowhere</a>"
        '<div class="sfnf-links">' + links + "</div>"
        '<span class="sfnf-copy">2026 Start From Nowhere</span>'
        "</div>"
        '<div class="sfnf-legal">' + legal + "</div></footer>" + sentinel_js()
    )


def apply_chrome_css(css):
    """Resolve {{CHROME_CSS}} inside a stylesheet destined for its own file.

    A vertical with hundreds of pages ships one stylesheet rather than inlining the
    same bytes into every page, but the shared chrome rules still have to reach it.
    """
    return css.replace("{{CHROME_CSS}}", CHROME_CSS)


def apply_chrome(html, extra_legal=""):
    # The sentinel normally rides along with the footer, which every content page carries.
    # A template without a footer (the rankings index builds its own chrome) would silently
    # miss it, so it can ask for the beacon directly with {{SENTINEL}}. A template must not
    # use both: the footer already supplies one, and two beacons would double-report every
    # error. The assertion below enforces that rather than trusting it.
    if "{{SENTINEL}}" in html and "{{SITE_FOOTER}}" in html:
        raise SystemExit("partials: template uses both {{SENTINEL}} and {{SITE_FOOTER}}; "
                         "the footer already carries the sentinel")
    out = (
        html.replace("{{CHROME_CSS}}", CHROME_CSS)
        .replace("{{SITE_HEADER}}", header_html())
        .replace("{{SITE_FOOTER}}", footer_html(extra_legal))
        .replace("{{SENTINEL}}", sentinel_js())
    )
    if "—" in out or "–" in out:
        raise SystemExit("partials: em/en dash in chrome output")
    return out
