// Service worker for the trainers. Built per exam by src/build.py, which fills the
// placeholders below; do not edit the generated copy at /app/sw.js.
//
// This exists for two reasons and the second is the one that pays for it.
//
// A student on a train, on a plane, or on a phone that has run out of data should be able
// to keep practising. Everything needed for that is already local: the bank is a static
// file and the engine keeps state in localStorage. The only thing standing between the
// app and full offline use was that nothing cached it.
//
// And App Review Guideline 4.2 rejects apps that are a repackaged website. An app that
// works with the network off is not one, and this is what makes that claim true rather
// than asserted.
//
// Cache strategy, which differs by what the file is:
//
//   bank.js and bank_rest.js   cache first, forever. Immutable per build and the largest
//                              files by an order of magnitude. Re-fetching them on a
//                              warm start would be the whole cost of the app.
//   the shell                  network first, cache fallback. It is small, it changes
//                              every deploy, and stale UI against a fresh bank is the
//                              one combination that breaks.
//   everything else same origin stale while revalidate.
//
// Supabase is never cached. Sync, auth and billing must fail honestly when offline
// rather than replay a stale answer, and a cached auth response is a security problem
// rather than a convenience.

const VERSION = '{{SW_VERSION}}';
const SCOPE_PATH = '{{SCOPE_PATH}}';
const CACHE = 'sfn-' + SCOPE_PATH.replace(/\//g, '-') + '-' + VERSION;

// Fetched on install so the first offline launch works without a prior visit to each one.
const PRECACHE = {{PRECACHE_JSON}};

// Matched by suffix: these are rebuilt every deploy under the same name, so the cache
// name carrying VERSION is what invalidates them rather than any header.
const IMMUTABLE = [/\/bank\.js$/, /\/bank_rest\.js$/, /\/icons\//];

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    // addAll rejects the whole install if any single request fails, which would leave the
    // worker uninstalled and the app online-only. The bank is large enough that a flaky
    // connection during install is a real case, so each file is allowed to fail on its
    // own and be picked up by the fetch handler later.
    await Promise.all(PRECACHE.map(async url => {
      try {
        const res = await fetch(url, { cache: 'reload' });
        if (res.ok) await cache.put(url, res);
      } catch (e) { /* fetch handler will cache it on first use */ }
    }));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    // Drop every cache from an older build of this scope. Scoped by name so the five
    // trainers do not evict each other.
    const prefix = 'sfn-' + SCOPE_PATH.replace(/\//g, '-') + '-';
    const names = await caches.keys();
    await Promise.all(names.map(n => (n.startsWith(prefix) && n !== CACHE) ? caches.delete(n) : null));
    if (self.registration.navigationPreload) {
      await self.registration.navigationPreload.enable();
    }
    await self.clients.claim();
  })());
});

const isImmutable = url => IMMUTABLE.some(re => re.test(url.pathname));

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);

  // Same origin only. Supabase, Stripe and fonts go straight to the network: a cached
  // auth or billing response is worse than an honest failure.
  if (url.origin !== self.location.origin) return;

  // Immutable per build: cache first, and never go to the network on a hit. This is what
  // makes a warm start instant and an offline start possible at all.
  if (isImmutable(url)) {
    event.respondWith((async () => {
      const hit = await caches.match(req);
      if (hit) return hit;
      const res = await fetch(req);
      if (res.ok) (await caches.open(CACHE)).put(req, res.clone());
      return res;
    })());
    return;
  }

  // Navigations: network first so a deploy is picked up immediately, cache fallback so
  // being offline still opens the app rather than the browser's error page.
  if (req.mode === 'navigate') {
    event.respondWith((async () => {
      try {
        const preload = await event.preloadResponse;
        const res = preload || await fetch(req);
        if (res && res.ok) (await caches.open(CACHE)).put(req, res.clone());
        return res;
      } catch (e) {
        const hit = await caches.match(req) || await caches.match(SCOPE_PATH);
        if (hit) return hit;
        throw e;
      }
    })());
    return;
  }

  // Everything else same origin: serve what we have, refresh in the background.
  event.respondWith((async () => {
    const hit = await caches.match(req);
    const net = fetch(req).then(async res => {
      if (res && res.ok) (await caches.open(CACHE)).put(req, res.clone());
      return res;
    }).catch(() => null);
    return hit || (await net) || new Response('', { status: 504, statusText: 'offline' });
  })());
});

// The page asks how much is cached so the Account tab can say whether the app is ready
// to use offline, rather than the student finding out on the train.
self.addEventListener('message', event => {
  if (!event.data || event.data.type !== 'sfn-cache-status') return;
  event.waitUntil((async () => {
    let cached = 0;
    try {
      const cache = await caches.open(CACHE);
      const keys = await cache.keys();
      cached = keys.length;
    } catch (e) {}
    (event.source || {}).postMessage && event.source.postMessage({
      type: 'sfn-cache-status', cached, expected: PRECACHE.length, version: VERSION,
    });
  })());
});
