# Shared site chrome: one header and one footer, identical on every page.
# Templates carry {{CHROME_CSS}}, {{SITE_HEADER}} and {{SITE_FOOTER}}; build
# scripts call apply_chrome() so the markup can never drift between pages.
import re

SITE_ORIGIN = "https://startfromnowhere.com"

LOGO_SVG = (
    '<svg viewBox="0 0 48 48" width="28" height="28" aria-hidden="true">'
    '<rect width="48" height="48" rx="12" fill="#122B4E"/>'
    '<path d="M13 33 22 22l6 5 8.5-10" fill="none" stroke="#fff" stroke-width="3.4" '
    'stroke-linecap="round" stroke-linejoin="round"/>'
    '<path d="M29.5 16.5H37V24" fill="none" stroke="#fff" stroke-width="3.4" '
    'stroke-linecap="round" stroke-linejoin="round"/></svg>'
)

# --- design tokens --------------------------------------------------------------
# One type and spacing system for the whole site, injected everywhere {{CHROME_CSS}}
# already goes. Before this each template carried its own copy of the font block and
# picked its own sizes, so the site ran on 4 families and 37 font sizes, half of them
# half-pixel values like 12.5px and 14.5px. Nothing shared a baseline because nothing
# shared a scale.
#
# The rules below come from reading what sites that do this well actually ship:
#  - one sans carries everything. Stripe runs sohne for 100 declarations and a mono
#    for 2; Vercel runs Geist for 150 and a mono for 23; Our World in Data, the
#    closest analogue to us because it is a sourced-data site, runs Lato for 396 and
#    a display serif for 117. None of them run two sans-serifs. We did: Manrope for
#    headings and IBM Plex Sans for body, similar enough to read as a mistake. Manrope
#    is gone. IBM Plex Sans carries the UI and pairs with IBM Plex Mono by design.
#  - tracking tightens as type grows, and is never positive except on small uppercase
#    labels. Stripe: -0.025em at 56px easing to 0 by 16px. We had +0.08em on 17
#    elements and no tracking at all on the 60px hero.
#  - spacing lives on a 4px grid. Stripe's scale is every 8px from 8 to 200. Ours had
#    3px, 5px, 7px, 9px, 13px, 17px, 22px, 26px, 34px, 68px and 78px in it.
#  - one measure, repeated. Our World in Data uses max-width:768px 218 times rather
#    than a bespoke width per section.
TOKENS_CSS = """
/* design tokens from src/partials.py; edit there, never per page */
:root{
 /* type: the sans carries the site, the serif is for headings, the mono is for figures */
 --sans:'IBM Plex Sans',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;
 --serif:'Source Serif 4',Georgia,'Times New Roman',serif;
 --mono:'IBM Plex Mono',ui-monospace,SFMono-Regular,Menlo,monospace;
 /* aliases so the 106 var(--display) call sites already in the templates resolve to
    the one sans instead of a second family. New rules should use --sans. */
 --display:var(--sans);--body:var(--sans);
 --font-display:var(--sans);--font-body:var(--sans);--font-mono:var(--mono);
 --font-serif-display:var(--serif);

 /* type scale: 9 steps, fluid where it needs to be, replacing 37 ad-hoc sizes */
 --t-100:12px;   /* tags, captions, table footnotes */
 --t-200:13px;   /* nav, footer, fine print */
 --t-300:14px;   /* card body, secondary text */
 --t-400:16px;   /* body */
 --t-500:18px;   /* lead paragraph */
 --t-600:20px;   /* card heading */
 --t-700:24px;   /* h3 */
 --t-800:clamp(27px,1.4vw + 22px,32px);   /* h2 */
 --t-900:clamp(34px,3.6vw + 20px,52px);   /* h1 */

 /* tracking follows size: tight when large, neutral at body, open only on caps */
 --tr-900:-.032em;--tr-800:-.022em;--tr-700:-.016em;--tr-600:-.011em;
 --tr-500:-.007em;--tr-400:0;--tr-caps:.06em;

 /* leading: tight for display, open for reading */
 --lh-900:1.04;--lh-800:1.12;--lh-700:1.25;--lh-body:1.6;--lh-tight:1.45;

 /* spacing: a 4px grid, nothing off it */
 --s1:4px;--s2:8px;--s3:12px;--s4:16px;--s5:24px;--s6:32px;--s7:48px;
 --s8:64px;--s9:96px;--s10:128px;

 /* layout: one page width, one gutter, one measure, used everywhere */
 --page:1120px;--gutter:24px;--measure:68ch;--measure-lead:54ch;
 /* funding, privacy, scoring and terms set max-width:var(--container-narrow) inline
    on <main>, but nothing ever defined it, so the declaration was invalid and those
    four pages rendered their prose at the full window width: about 175 characters a
    line on a 1440px screen, against the 45 to 90 that is comfortable to read.
    Defining it here fixes all four at once. 768px is the width Our World in Data
    uses for reading columns. */
 --container-narrow:768px;--container-max:1120px;
 --section-y:clamp(48px,5vw,80px);

 --r-sm:6px;--r-md:8px;--r-lg:12px;--r-full:999px;
 /* one light source, from above */
 --sh-1:0 1px 2px rgba(12,31,58,.06);
 --sh-2:0 2px 8px rgba(12,31,58,.08);
 --sh-3:0 12px 32px rgba(12,31,58,.12);
 --dur-1:120ms;--dur-2:200ms;--ease:cubic-bezier(.16,1,.3,1);
}
/* Base typography, so a page inherits the system instead of restating it. */
body{font-family:var(--sans);font-size:var(--t-400);line-height:var(--lh-body);
 -webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;
 font-feature-settings:'kern' 1;text-rendering:optimizeLegibility}
h1,h2,h3,h4,h5,h6{font-family:var(--serif);font-weight:700;margin:0}
h1{font-size:var(--t-900);letter-spacing:var(--tr-900);line-height:var(--lh-900)}
h2{font-size:var(--t-800);letter-spacing:var(--tr-800);line-height:var(--lh-800)}
h3{font-size:var(--t-700);letter-spacing:var(--tr-700);line-height:var(--lh-700)}
h4{font-size:var(--t-600);letter-spacing:var(--tr-600);line-height:var(--lh-700)}
/* Figures are the one place mono belongs: tabular so columns of numbers line up. */
.num,.tabnum{font-family:var(--mono);font-variant-numeric:tabular-nums;
 font-feature-settings:'tnum' 1;letter-spacing:var(--tr-600)}
/* The only positive tracking on the site: small uppercase labels, which need it. */
.eyebrow{font-family:var(--sans);font-weight:600;font-size:var(--t-100);
 letter-spacing:var(--tr-caps);text-transform:uppercase;color:var(--gray-500,#6B7280)}
/* One measure for prose, so every column of text is the same width. */
.prose{max-width:var(--measure)}
.lead{max-width:var(--measure-lead);font-size:var(--t-500);line-height:var(--lh-tight)}
/* --- onward paths on a school page -------------------------------------------- */
/* A school page used to carry two links out of its body, the trainer and the index,
   and 30 of last month's consented sessions landed on one and left without a second
   pageview. */
.onward{margin:var(--s7) 0 0;padding-top:var(--s6);border-top:1px solid var(--gray-200)}
.onward h2{font-size:var(--t-700);letter-spacing:var(--tr-700);margin:0 0 var(--s2)}
.onward h2+.note{margin:0 0 var(--s5);max-width:var(--measure)}
.onward h2:not(:first-child){margin-top:var(--s7)}
.peergrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(232px,1fr));gap:var(--s3)}
.peergrid>*{min-width:0}
.peer{display:grid;grid-template-columns:auto 1fr;grid-template-rows:auto auto;
 gap:var(--s1) var(--s3);align-items:baseline;padding:var(--s4);text-decoration:none;
 border:1px solid var(--gray-200);border-radius:var(--r-lg);background:#fff;
 transition:box-shadow var(--dur-2) var(--ease),transform var(--dur-2) var(--ease),
 border-color var(--dur-2) var(--ease)}
.peer:hover{box-shadow:var(--sh-2);transform:translateY(-2px);border-color:var(--navy-600)}
.peer .pr{grid-row:1/3;font-family:var(--mono);font-variant-numeric:tabular-nums;
 font-size:var(--t-500);color:var(--navy-600);letter-spacing:var(--tr-600)}
.peer .pn{font-family:var(--sans);font-weight:600;font-size:var(--t-300);
 color:var(--navy-900);line-height:var(--lh-tight)}
.peer .pf{font-size:var(--t-100);color:var(--gray-500)}
.peer .pf .num{font-family:var(--mono);font-variant-numeric:tabular-nums;color:var(--gray-700)}
.peer .pq{font-size:var(--t-100);color:var(--gray-500)}
.nextgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(248px,1fr));gap:var(--s3)}
.nextgrid>*{min-width:0}
.nx{display:block;padding:var(--s4);text-decoration:none;border:1px solid var(--gray-200);
 border-radius:var(--r-lg);background:var(--gray-50);
 transition:box-shadow var(--dur-2) var(--ease),border-color var(--dur-2) var(--ease)}
.nx:hover{box-shadow:var(--sh-2);border-color:var(--navy-600);background:#fff}
.nx strong{display:block;font-family:var(--sans);font-weight:600;font-size:var(--t-400);
 color:var(--navy-900);letter-spacing:var(--tr-500);margin-bottom:var(--s2)}
.nx span{display:block;font-size:var(--t-200);color:var(--gray-500);line-height:var(--lh-tight)}
@media(prefers-reduced-motion:reduce){
 *,*::before,*::after{animation-duration:.01ms !important;animation-iteration-count:1 !important;
  transition-duration:.01ms !important;scroll-behavior:auto !important}
}
""".strip()


CHROME_CSS = """
/* shared chrome from src/partials.py; edit there, never per page */
.sfnh{position:sticky;top:0;z-index:50;background:#fff;border-bottom:1px solid #DCE5F1}
.sfnh-in{max-width:var(--page);margin:0 auto;padding:0 var(--gutter);height:60px;display:flex;align-items:center;justify-content:space-between;gap:16px}
.sfnh-l{display:flex;align-items:center;gap:var(--s4);min-width:0}
.sfn-wordmark{display:flex;align-items:center;gap:var(--s2);font-family:'Source Serif 4',Georgia,serif;font-weight:700;font-size:19px;color:#0C1F3A;text-decoration:none;white-space:nowrap;letter-spacing:0}
nav.sfn-nav{display:flex;align-items:center}
.sfn-dd{position:relative}
.sfn-dd>button{display:flex;align-items:center;gap:4px;padding:8px 12px;font-family:var(--sans);font-weight:600;font-size:var(--t-200);color:#374151;background:none;border:none;cursor:pointer;line-height:1.2;transition:color var(--dur-1) var(--ease)}
.sfn-dd>button:hover{color:#0C1F3A}
.sfn-dd .car{font-size:9px;color:#6B7280;transition:transform var(--dur-2) var(--ease)}
.sfn-dd:hover .car,.sfn-dd:focus-within .car{transform:rotate(180deg)}
.sfn-dd-menu{position:absolute;top:100%;left:0;width:276px;background:#fff;border:1px solid #DCE5F1;border-radius:var(--r-lg);box-shadow:var(--sh-3);padding:4px;display:none;z-index:60}
.sfn-dd:hover .sfn-dd-menu,.sfn-dd:focus-within .sfn-dd-menu{display:block}
.sfn-dd-menu a{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:var(--s2) var(--s3);border-radius:var(--r-md);font-family:var(--sans);font-weight:600;font-size:var(--t-200);color:#374151;text-decoration:none;white-space:nowrap}
.sfn-dd-menu a:hover{background:#F2F6FB;color:#0C1F3A}
.sfn-tag{font-family:var(--sans);font-size:var(--t-100);font-weight:700;padding:var(--s1) var(--s2);border-radius:var(--r-full);background:#F2F6FB;color:#6B7280;white-space:nowrap;flex-shrink:0}
.sfn-tag.live{background:#16A34A;color:#fff}
.sfnh-r{display:flex;align-items:center;gap:8px}
.sfn-signin{font-family:var(--sans);font-weight:600;font-size:var(--t-200);color:#6B7280;text-decoration:none;padding:8px 12px;border-radius:var(--r-md);transition:color var(--dur-1) var(--ease)}
.sfn-signin:hover{color:#0C1F3A}
.sfn-cta{font-family:var(--sans);font-weight:700;font-size:var(--t-200);background:#122B4E;color:#fff;text-decoration:none;padding:var(--s2) var(--s4);border-radius:var(--r-md);transition:background var(--dur-1) var(--ease);white-space:nowrap}
.sfn-cta:hover{background:#0C1F3A}
.sfn-burger{display:none;background:none;border:none;cursor:pointer;padding:8px;color:#374151}
.sfn-mobile{display:none;border-top:1px solid #DCE5F1;background:#fff;padding:var(--s3) var(--gutter) var(--s4)}
.sfn-mobile a{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:var(--s3) var(--s3);border-radius:var(--r-md);font-family:var(--sans);font-weight:600;font-size:var(--t-300);color:#374151;text-decoration:none}
.sfn-mobile a:hover{background:#F2F6FB;color:#0C1F3A}
.sfn-mobile .grp{font-family:var(--sans);font-weight:700;font-size:var(--t-100);letter-spacing:var(--tr-caps);text-transform:uppercase;color:#9CA3AF;padding:var(--s3) var(--s3) var(--s1)}
.sfn-mobile .mb-cta{display:block;text-align:center;background:#122B4E;color:#fff;font-weight:700;margin-top:10px}
.sfn-mobile .mb-cta:hover{background:#0C1F3A;color:#fff}
@media(max-width:1023px){nav.sfn-nav,.sfn-signin,.sfn-cta{display:none}.sfn-burger{display:inline-flex}}
.sfnf{border-top:1px solid #DCE5F1;background:#F9FAFB;margin-top:var(--s7)}
.sfnf-in{max-width:var(--page);margin:0 auto;padding:var(--s7) var(--gutter) var(--s5);display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap}
.sfnf-links{display:flex;gap:var(--s5);flex-wrap:wrap;justify-content:center}
.sfnf-links a,.sfnf-links button{font-family:var(--sans);font-weight:600;font-size:var(--t-200);color:#6B7280;text-decoration:none;transition:color var(--dur-1) var(--ease)}
.sfnf-links button{background:none;border:none;padding:0;cursor:pointer;line-height:inherit}
.sfnf-links a:hover,.sfnf-links button:hover{color:#0C1F3A}
.sfnf-copy{font-family:var(--sans);font-size:var(--t-200);color:#9CA3AF;white-space:nowrap}
.sfnf-legal{max-width:var(--page);margin:0 auto;padding:0 var(--gutter) var(--s6);font-size:var(--t-100);color:#9CA3AF;line-height:1.6}
""".strip()

_NAV_GROUPS = [
    ("Exam Prep", [
        ("GMAT Focus Edition", "/exams/gmat/", "Live"),
        ("SAT", "/exams/sat/", "Live"),
        ("GRE General Test", "/exams/gre/", "Live"),
        ("LSAT", "/exams/lsat/", "Live"),
        ("ACT", "/exams/act/", "Live"),
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
    # California wants this link conspicuous on every page, not findable only by someone
    # already reading the privacy policy. Last in the list because it is the one people
    # arrive looking for rather than stumble on.
    ("Do Not Sell or Share My Personal Information", "/do-not-sell/"),
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


SITE_EVENTS_URL = ("https://ftsqwbzhkzuudogkvoqa.supabase.co/rest/v1/site_events"
                   "?apikey=sb_publishable_GToT4fK6RiwCZpPFE3bGiw_ThXq9qel")


def consent_js():
    """The consent banner and the analytics beacon it gates.

    Two things were wrong before this existed. The page analytics beacon fired on
    first paint, before anyone had agreed to anything, and it carries a persistent
    session id, a referrer and a country derived from the address, which is personal
    data under GDPR and needs consent rather than a notice. And the beacon itself was
    copy pasted into eleven templates, which is precisely how a gate gets added to ten
    of them.

    The banner is built to be valid rather than merely present, because a banner that
    is not valid is worse than none: it collects the data and fails anyway.

      Refusing is exactly as easy as accepting. Both are buttons, side by side, the
      same size. Regulators have fined sites for putting Reject two clicks deeper.
      Nothing is pre-ticked, and nothing analytic fires until a choice is made.
      A Global Privacy Control signal is honoured as a refusal without asking.
      The choice is changeable later from the footer on every page.
      The site works identically either way.

    What is deliberately NOT gated is item telemetry, which records that an item was
    answered, which option was chosen and how long it took, with no user, session,
    device or address attached. It cannot be tied to a person, so it is not personal
    data, and it is the entire signal the adaptive engine learns from. The banner says
    so plainly rather than hiding it.
    """
    return (
        "<!-- sfn consent: gates the page analytics beacon; item telemetry is unlinkable and ungated -->\n"
        "<style>#sfn-consent{position:fixed;left:0;right:0;bottom:0;z-index:80;background:#fff;"
        "border-top:1px solid var(--sfn-border,#E5E7EB);box-shadow:0 -6px 24px rgba(8,21,39,.12);"
        "padding:16px 20px calc(16px + env(safe-area-inset-bottom,0px))}\n"
        "#sfn-consent[hidden]{display:none}\n"
        "#sfn-consent .in{max-width:1100px;margin:0 auto;display:flex;gap:18px;align-items:center;flex-wrap:wrap}\n"
        "#sfn-consent p{margin:0;font-size:13.5px;line-height:1.5;color:#374151;flex:1 1 380px;min-width:260px}\n"
        "#sfn-consent .btns{display:flex;gap:8px;flex-wrap:wrap}\n"
        "#sfn-consent button{font:inherit;font-size:13px;font-weight:600;padding:9px 16px;border-radius:8px;"
        "cursor:pointer;border:1px solid #122B4E;white-space:nowrap}\n"
        "#sfn-consent .yes{background:#122B4E;color:#fff}\n"
        "#sfn-consent .no{background:#fff;color:#122B4E}\n"
        "#sfn-consent .more{background:none;border:none;color:#2C4E80;text-decoration:underline;padding:9px 4px}\n"
        "#sfn-consent .detail{flex:1 1 100%;margin:4px 0 0;font-size:12.5px;color:#6B7280;line-height:1.55}\n"
        "#sfn-consent .detail[hidden]{display:none}\n"
        "#sfn-consent .now{flex:1 1 100%;margin:2px 0 0;font-size:12.5px;color:#2C4E80;font-weight:600}\n"
        "#sfn-consent .now[hidden]{display:none}\n"
        ".sfn-consent-link{background:none;border:none;padding:0;font:inherit;color:inherit;"
        "text-decoration:underline;cursor:pointer}</style>\n"
        '<div id="sfn-consent" hidden role="region" aria-label="Privacy choices">\n'
        '  <div class="in">\n'
        "    <p><b>Your choice about analytics.</b> We would like to record which pages are opened, "
        "where visitors arrive from and how long they stay, so we can see what is worth building. "
        "That needs your agreement, and the site works exactly the same if you decline.</p>\n"
        '    <div class="btns">\n'
        '      <button type="button" class="yes" onclick="sfnConsent(true)">Accept Analytics</button>\n'
        '      <button type="button" class="no" onclick="sfnConsent(false)">Reject Non Essential</button>\n'
        '      <button type="button" class="more" onclick="sfnConsentDetail()" aria-expanded="false" '
        'aria-controls="sfn-consent-detail">What We Collect</button>\n'
        "    </div>\n"
        '    <p class="now" id="sfn-consent-now" hidden>'
        '<span data-now="on" hidden>Analytics is on right now. Rejecting stops it from here on.</span>'
        '<span data-now="off" hidden>Analytics is off right now.</span>'
        '<span data-now="gpc" hidden> Your browser sent a Global Privacy Control signal.</span>'
        "</p>\n"
        '    <p class="detail" id="sfn-consent-detail" hidden>'
        "<b>Only if you accept.</b> Pages opened, the site you came from, campaign tags in the link, "
        "whether you are on a phone or a desktop, how long a page was open, and a country worked out "
        "from your network address. A short lived session code ties those together for one visit. "
        "The address itself is never stored: a one way hash is written by the database and the address "
        "is discarded. "
        "<b>Always, and not about you.</b> Which practice item was answered, which option was chosen, "
        "whether it was right, how many seconds it took, how long before you picked anything, and how "
        "often you changed your mind. Those records carry no account, no session, "
        "no device and no address, so they cannot be tied back to anyone; they are how the practice "
        "engine learns which questions work. "
        "<b>Never.</b> We run no third party trackers, and nothing this banner is about is "
        "ever sold or shared: not a page view, not an item answered, not a word you typed. "
        "<b>On adult accounts.</b> If you are 18 or over we may buy details about you from "
        "data partners and add them to your profile, kept separately from what you told us "
        "yourself and deleted with your account. Nothing about anyone under 18 is ever bought, "
        "appended, sold or shared. "
        "<b>Only if you switch it on.</b> Sharing your profile with partners, including data "
        "brokers, is off until an adult account turns it on, and off again in one click from "
        'the <a href="/do-not-sell/">Do Not Sell</a> page linked in every footer. '
        'Full detail is on the <a href="/privacy.html">privacy page</a>.</p>\n'
        "  </div>\n"
        "</div>\n"
        "<script>(function(){try{\n"
        "var K='sfn_consent_v1';\n"
        "function read(){ try{ return JSON.parse(localStorage.getItem(K)||'null'); }catch(e){ return null; } }\n"
        "window.sfnConsentState=read;\n"
        "// Global Privacy Control is a legally recognised refusal in several states. Honour it\n"
        "// without asking, because asking after someone has already said no is the dark pattern.\n"
        "var gpc = (navigator.globalPrivacyControl===true);\n"
        "window.sfnConsent=function(yes){ try{ localStorage.setItem(K,JSON.stringify(\n"
        "  {analytics:!!yes,ts:new Date().toISOString(),v:1})); }catch(e){}\n"
        " var b=document.getElementById('sfn-consent'); if(b) b.hidden=true;\n"
        " if(yes) start(); };\n"
        "window.sfnConsentDetail=function(){ var d=document.getElementById('sfn-consent-detail');\n"
        " var btn=document.querySelector('#sfn-consent .more'); if(!d) return;\n"
        " d.hidden=!d.hidden; if(btn) btn.setAttribute('aria-expanded', String(!d.hidden)); };\n"
        "window.sfnConsentReopen=function(){ var b=document.getElementById('sfn-consent');\n"
        " if(!b) return; var c=read(), n=document.getElementById('sfn-consent-now');\n"
        " if(n){ var on=c&&c.analytics, off=c&&!c.analytics;\n"
        "  n.hidden = (c===null);\n"
        "  n.querySelector('[data-now=\\'on\\']').hidden = !on;\n"
        "  n.querySelector('[data-now=\\'off\\']').hidden = !off;\n"
        "  n.querySelector('[data-now=\\'gpc\\']').hidden = !(off&&c.gpc); }\n"
        " b.hidden=false; var f=b.querySelector('button'); if(f) f.focus(); };\n"
        "function start(){\n"
        " if(window.__sfnBeacon) return; window.__sfnBeacon=1;\n"
        ' var U="' + SITE_EVENTS_URL + '";\n'
        " var s=sessionStorage.getItem('sfn_sid');\n"
        " if(!s){ s=Math.random().toString(36).slice(2)+Math.random().toString(36).slice(2,10);"
        " sessionStorage.setItem('sfn_sid',s); }\n"
        " var p=location.pathname,t0=Date.now(),done=false;\n"
        " function send(o){ var c=read(); if(!c||!c.analytics) return; o.sid=s; o.path=p;\n"
        "  try{ fetch(U,{method:'POST',headers:{'Content-Type':'application/json'},"
        "body:JSON.stringify(o),keepalive:true}); }catch(e){} }\n"
        " send({kind:'pageview',ref:(document.referrer||'').slice(0,290)||null,"
        "utm:location.search.indexOf('utm_')>-1?location.search.slice(1,190):null,"
        "device:/Mobi|Android/i.test(navigator.userAgent)?'mobile':'desktop',vw:innerWidth});\n"
        " function dur(){ if(done) return; done=true; send({kind:'duration',dur_ms:Date.now()-t0}); }\n"
        # Funnel milestones. The visit funnel was measurable up to the moment somebody
        # opened a trainer and no further: item_events records the answering but carries
        # no session id by design, so it can never be joined to a visit, and that stays
        # true. A milestone row carries the same sid a pageview already carries and
        # nothing new. Each step fires once per session, so one long study session
        # cannot outvote a short one in the counts.
        " var seen={};\n"
        " window.sfnStep=function(step){ if(!step||seen[step]) return; seen[step]=1;\n"
        "  send({kind:'milestone',step:String(step).slice(0,40)}); };\n"
        # This script ships with the footer, so the trainer's own boot line runs
        # before sfnStep exists and its app_open was being dropped silently. Callers
        # queue instead of guarding, and the queue is drained here, so the order of
        # the two scripts stops mattering.
        " var q=window.__sfnStepQ; window.__sfnStepQ=null;\n"
        " if(q) for(var i=0;i<q.length;i++) window.sfnStep(q[i]);\n"
        " document.addEventListener('visibilitychange',function(){"
        "if(document.visibilityState==='hidden') dur(); });\n"
        " addEventListener('pagehide',dur);\n"
        "}\n"
        "var c=read();\n"
        "if(gpc){ if(!c) try{ localStorage.setItem(K,JSON.stringify("
        "{analytics:false,ts:new Date().toISOString(),v:1,gpc:true})); }catch(e){} }\n"
        "else if(c===null){ var b=document.getElementById('sfn-consent'); if(b) b.hidden=false; }\n"
        "else if(c&&c.analytics){ start(); }\n"
        "if(!window.sfnStep){ window.sfnStep=function(){}; window.__sfnStepQ=null; }\n"
        "}catch(e){}})();</script>\n"
    )


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
    # A consent choice that cannot be changed later is not a choice. Every page carries
    # the banner, so every page can reopen it; this is the one control that has to be
    # in the footer rather than buried on the privacy page.
    links += ('<button type="button" class="sfn-consent-open" '
              'onclick="sfnConsentReopen()">Privacy Choices</button>')
    legal = LEGAL_LINE + ((" " + extra_legal) if extra_legal else "")
    return (
        '<footer class="sfnf"><div class="sfnf-in">'
        '<a class="sfn-wordmark" href="/" style="font-size:16px">' + LOGO_SVG.replace('width="28" height="28"', 'width="24" height="24"') + "Start From Nowhere</a>"
        '<div class="sfnf-links">' + links + "</div>"
        '<span class="sfnf-copy">2026 Start From Nowhere</span>'
        "</div>"
        '<div class="sfnf-legal">' + legal + "</div></footer>" + consent_js() + sentinel_js()
    )


def apply_chrome_css(css):
    """Resolve {{CHROME_CSS}} inside a stylesheet destined for its own file.

    A vertical with hundreds of pages ships one stylesheet rather than inlining the
    same bytes into every page, but the shared chrome rules still have to reach it.
    """
    return css.replace("{{CHROME_CSS}}", TOKENS_CSS + "\n" + CHROME_CSS)


# --- share cards ----------------------------------------------------------------
# A link posted to X, LinkedIn or anywhere else renders as whatever Open Graph tags the
# page carries. Before this, 1,559 of the site's 1,588 pages carried none at all, so every
# school page, college page and exam guide shared as a bare blue link with no title, no
# description and no image, and the 29 blog posts that did have tags asked for the small
# card and supplied no image. Posting more often through that funnel would only have moved
# more people past a link that looks like nothing.
#
# The tags are derived from what each page already has rather than passed in by every
# builder: the title and description on a school page are already written for exactly this
# job, and deriving them means no page can be added later that quietly ships without a card.
OG_IMAGE_DEFAULT = "/og/default.png"
# Path prefix to card image. First match wins, so order matters.
OG_IMAGES = [
    ("/schools/", "/og/mba.png"),
    ("/colleges/", "/og/colleges.png"),
    ("/exams/", "/og/exams.png"),
    ("/blog/", "/og/blog.png"),
    ("/app/", "/og/trainer.png"),
    ("/sat/app/", "/og/trainer.png"),
    ("/gre/app/", "/og/trainer.png"),
    ("/lsat/app/", "/og/trainer.png"),
    ("/act/app/", "/og/trainer.png"),
    ("/pricing/", "/og/pricing.png"),
    ("/community/", "/og/community.png"),
    ("/apply/", "/og/apply.png"),
    ("/international/", "/og/apply.png"),
    ("/funding/", "/og/funding.png"),
]

_TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S | re.I)
_DESC_RE = re.compile(r'<meta name="description" content="(.*?)"', re.S | re.I)
_CANON_RE = re.compile(r'<link rel="canonical" href="(.*?)"', re.I)


def og_image_for(url):
    for prefix, img in OG_IMAGES:
        if prefix in url:
            return img
    return OG_IMAGE_DEFAULT


def social_meta(html):
    """Open Graph and Twitter card tags derived from the page's own head.

    Returns "" when the page already carries og:title, so a builder that writes its own
    tags is never given a second, conflicting set.
    """
    if "og:title" in html:
        return ""
    t = _TITLE_RE.search(html)
    d = _DESC_RE.search(html)
    c = _CANON_RE.search(html)
    if not (t and d and c):
        return ""
    title = " ".join(t.group(1).split())
    desc = " ".join(d.group(1).split())
    url = c.group(1)
    img = SITE_ORIGIN + og_image_for(url)
    return (
        '\n<meta property="og:type" content="website">'
        '<meta property="og:site_name" content="Start From Nowhere">'
        '<meta property="og:locale" content="en_US">'
        '<meta property="og:title" content="' + title + '">'
        '<meta property="og:description" content="' + desc + '">'
        '<meta property="og:url" content="' + url + '">'
        '<meta property="og:image" content="' + img + '">'
        '<meta property="og:image:width" content="1200">'
        '<meta property="og:image:height" content="630">'
        '<meta name="twitter:card" content="summary_large_image">'
        '<meta name="twitter:title" content="' + title + '">'
        '<meta name="twitter:description" content="' + desc + '">'
        '<meta name="twitter:image" content="' + img + '">'
    )


def apply_social(html):
    """Insert the derived card tags immediately before </head>."""
    tags = social_meta(html)
    if not tags:
        return html
    i = html.lower().find("</head>")
    if i < 0:
        return html
    return html[:i] + tags + html[i:]


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
        html.replace("{{CHROME_CSS}}", TOKENS_CSS + "\n" + CHROME_CSS)
        .replace("{{SITE_HEADER}}", header_html())
        .replace("{{SITE_FOOTER}}", footer_html(extra_legal))
        .replace("{{SENTINEL}}", consent_js() + sentinel_js())
    )
    out = apply_social(out)
    if "—" in out or "–" in out:
        raise SystemExit("partials: em/en dash in chrome output")
    return out
