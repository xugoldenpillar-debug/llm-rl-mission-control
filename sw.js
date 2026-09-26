/* Versioned application shell only. Personal data stays in IndexedDB, not this cache. */
const BASE=new URL('./',self.location.href);
const PREFIX='rlmc-shell:'+BASE.pathname+':';
const CACHE=PREFIX+'1.0.0';
const FILES=['./','index.html','styles.css','icon.svg','manifest.webmanifest','js/app.js','js/core.js','js/storage.js','js/views.js','js/plan.js'];
const URLS=new Set(FILES.map(p=>new URL(p,BASE).href));
self.addEventListener('install',event=>{event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll([...URLS])));});
// Deliberately do not skipWaiting: never replace a running app with a mixed module version.
self.addEventListener('activate',event=>{event.waitUntil((async()=>{const keys=await caches.keys();await Promise.all(keys.filter(k=>k.startsWith(PREFIX)&&k!==CACHE).map(k=>caches.delete(k)));await self.clients.claim();})());});
self.addEventListener('fetch',event=>{
 const req=event.request,url=new URL(req.url);if(req.method!=='GET'||url.origin!==BASE.origin)return;
 if(req.mode==='navigate'&&url.pathname.startsWith(BASE.pathname)){
  event.respondWith((async()=>{const cache=await caches.open(CACHE);return await cache.match(new URL('index.html',BASE).href)||fetch(req);})());return;
 }
 if(!URLS.has(url.href))return;
 event.respondWith((async()=>{const cache=await caches.open(CACHE);const saved=await cache.match(req);return saved||fetch(req);})());
});
