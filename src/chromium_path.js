// Where Chromium is, in whichever environment this is running.
//
// Three cases, and getting this wrong is how a suite ends up running in exactly one
// place. CHROMIUM_PATH wins when set. Otherwise, if this machine keeps browsers in
// /opt/pw-browsers (the agent sandbox does), use the newest one there. Otherwise return
// undefined, which is what Playwright wants: it then resolves the browser it installed
// itself, which is the case on a CI runner.
//
// Returning undefined rather than a path is the important half. An empty string or a
// path that does not exist is a launch failure; undefined is "you decide".
//
// This exists as a shared module because src/smoke_business.js read /opt/pw-browsers
// unconditionally and crashed with ENOENT on the first CI run. One copy of the logic
// cannot drift from itself.
const fs = require('fs');

function chromiumPath() {
  if (process.env.CHROMIUM_PATH) return process.env.CHROMIUM_PATH;
  const dir = '/opt/pw-browsers';
  if (!fs.existsSync(dir)) return undefined;
  const found = fs.readdirSync(dir)
    .filter(d => d.startsWith('chromium-'))
    .sort()
    .reverse()
    .map(d => dir + '/' + d + '/chrome-linux/chrome')
    .find(p => fs.existsSync(p));
  return found || undefined;
}

module.exports = { chromiumPath };
