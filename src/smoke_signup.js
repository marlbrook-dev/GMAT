// The signup age gate, checked against what the form actually does.
//
// Run with:
//   CHROMIUM_PATH=/opt/pw-browsers/chromium-*/chrome-linux/chrome node src/smoke_signup.js
//
// Birth month and year moved from the Account page into signup for two reasons, and the
// second would matter even if nothing were ever sold.
//
// The sharing programme keys off age_tier, and 'undeclared' is not '18_plus', so a field
// sitting on a profile page nobody opens meant the shipped default reached nobody.
//
// And we had no idea whether any of our users were children. The SAT and ACT trainers
// are aimed at high schoolers, so some of them certainly are, and COPPA obligations for
// an under 13 attach on collection rather than on selling. A field nobody fills in is
// not an age gate, it is the absence of one.
//
// So the field is REQUIRED, and that is what this file mostly checks: that the form
// refuses to send a sign-in link until both parts are chosen. An optional field here
// would reproduce exactly the problem the move was meant to fix, and it would do it
// quietly.
//
// It also checks that the day is never asked for. A full date of birth is one of the few
// fields that re-identifies most people on its own; the month and year answer the only
// question we need.
const { chromium } = require('playwright');
const { chromiumPath } = require('./chromium_path.js');
const http = require('http'), fs = require('fs'), p0 = require('path');
const ROOT = p0.join(__dirname, '..');
const T = {'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png',
           '.svg':'image/svg+xml','.json':'application/json','.webmanifest':'application/manifest+json'};
const srv = http.createServer((q, r) => {
  let rel = decodeURIComponent(q.url.split('?')[0]); if (rel.endsWith('/')) rel += 'index.html';
  const f = p0.join(ROOT, rel);
  if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { r.writeHead(404); r.end('nf'); return; }
  r.writeHead(200, {'Content-Type': T[p0.extname(f)] || 'application/octet-stream'});
  fs.createReadStream(f).pipe(r);
});
const noise = t => /ERR_CERT_AUTHORITY_INVALID|fonts\.(googleapis|gstatic)\.com|Failed to fetch|net::ERR/.test(t);
const fails = [];
const check = (n, c, d) => {
  console.log((c ? '  ok: ' : '  FAIL: ') + n + (d ? '  -> ' + d : ''));
  if (!c) fails.push(n);
};

(async () => {
  await new Promise(r => srv.listen(0, '127.0.0.1', r));
  const P = srv.address().port;
  const b = await chromium.launch({ executablePath: chromiumPath() });

  // Every trainer shares one template, so a regression in one is a regression in all.
  // The SAT and ACT apps are the ones whose users are most likely to be minors.
  for (const app of ['app', 'sat/app', 'act/app', 'gre/app', 'lsat/app']) {
    const pg = await b.newPage({ viewport: { width: 390, height: 844 } });
    const errs = [];
    pg.on('pageerror', e => { if (!noise(e.message)) errs.push(e.message); });
    await pg.goto('http://127.0.0.1:' + P + '/' + app + '/', { waitUntil: 'load' });
    await pg.evaluate(() => { Cloud.status = 'signed-out'; Cloud.user = null; show('data'); });
    await pg.waitForTimeout(200);

    check('[' + app + '] no page errors', errs.length === 0, errs[0] || '');
    check('[' + app + '] birth month is on the signup form',
      await pg.evaluate(() => !!document.getElementById('authMonth')));
    check('[' + app + '] birth year is on the signup form',
      await pg.evaluate(() => !!document.getElementById('authYear')));
    // The day is never asked for, on any path.
    check('[' + app + '] the day is never asked for',
      await pg.evaluate(() => !document.getElementById('authDay')
        && !/birth day/i.test(document.getElementById('v-data').innerHTML)));

    // Intercept the send rather than trusting the button, so a form that looks like it
    // validates but sends anyway cannot pass.
    await pg.evaluate(() => { window.__sent = []; Cloud.signIn = async e => { window.__sent.push(e); return {}; }; });

    await pg.evaluate(() => { document.getElementById('authEmail').value = 'a@b.co'; sendMagicLink(); });
    await pg.waitForTimeout(120);
    check('[' + app + '] refuses to send with no birth date',
      (await pg.evaluate(() => window.__sent.length)) === 0);

    await pg.evaluate(() => { document.getElementById('authMonth').value = '3'; sendMagicLink(); });
    await pg.waitForTimeout(120);
    check('[' + app + '] refuses to send with only a month',
      (await pg.evaluate(() => window.__sent.length)) === 0);

    await pg.evaluate(() => {
      document.getElementById('authMonth').value = ''; document.getElementById('authYear').value = '1995';
      sendMagicLink();
    });
    await pg.waitForTimeout(120);
    check('[' + app + '] refuses to send with only a year',
      (await pg.evaluate(() => window.__sent.length)) === 0);

    await pg.evaluate(() => { document.getElementById('authMonth').value = '3'; sendMagicLink(); });
    await pg.waitForTimeout(200);
    check('[' + app + '] sends once both are chosen',
      (await pg.evaluate(() => window.__sent.length)) === 1);

    // Held locally until sign-in completes, because the profile row does not exist yet.
    check('[' + app + '] the birth date is kept for the profile push',
      await pg.evaluate(() => {
        const a = state.settings.about || {};
        return a.birth_month === 3 && a.birth_year === 1995;
      }));

    // An invalid email must still not send, with the birth date filled in.
    await pg.evaluate(() => { window.__sent = []; document.getElementById('authEmail').value = 'nope'; sendMagicLink(); });
    await pg.waitForTimeout(120);
    check('[' + app + '] still validates the email',
      (await pg.evaluate(() => window.__sent.length)) === 0);

    // --- social sign in -----------------------------------------------------------
    const oauth = await pg.evaluate(() =>
      [...document.querySelectorAll('.oauth button')].map(b => b.textContent.trim()));
    check('[' + app + '] all four providers offered', oauth.length === 4, oauth.join(', '));
    // Guideline 4.8: Sign in with Apple must be at least as prominent as any other
    // social login. First in the row is the unambiguous way to satisfy that.
    check('[' + app + '] Apple is listed first', oauth[0] === 'Apple', oauth[0]);

    // The age gate must hold across OAuth too. No provider returns a birth date, so an
    // ungated social button is how every account ends up age undeclared.
    await pg.evaluate(() => {
      window.__oauth = [];
      Cloud.client = { auth: { signInWithOAuth: async o => { window.__oauth.push(o); return {}; } } };
      document.getElementById('authMonth').value = '';
      document.getElementById('authYear').value = '';
      oauthSignIn('google');
    });
    await pg.waitForTimeout(120);
    check('[' + app + '] social sign-in refuses without a birth date',
      (await pg.evaluate(() => window.__oauth.length)) === 0);

    await pg.evaluate(() => {
      document.getElementById('authMonth').value = '6';
      document.getElementById('authYear').value = '1998';
      oauthSignIn('google');
    });
    await pg.waitForTimeout(150);
    check('[' + app + '] social sign-in proceeds once the age is given',
      (await pg.evaluate(() => window.__oauth.length)) === 1);
    check('[' + app + '] the birth date is kept across the redirect',
      await pg.evaluate(() => {
        const a = state.settings.about || {};
        return a.birth_month === 6 && a.birth_year === 1998;
      }));
    // Extra scopes would put the app through provider security review and show a consent
    // screen listing access we have no use for.
    check('[' + app + '] no extra OAuth scopes requested',
      await pg.evaluate(() => !(window.__oauth[0] && window.__oauth[0].options
        && window.__oauth[0].options.scopes)));

    const wide = await pg.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 2);
    check('[' + app + '] no horizontal overflow at 390px', !wide);
    await pg.close();
  }

  await b.close(); srv.close();
  console.log(fails.length ? '\nFAILURES: ' + fails.join(', ')
                           : '\nall signup age gate checks passed');
  process.exit(fails.length ? 1 : 0);
})();
