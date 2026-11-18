const CACHE="streamplus-shell-v2";
const SHELL=["/streamplus/","/streamplus/index.html","/streamplus/icon.svg","/streamplus/manifest.webmanifest"];
self.addEventListener("install",event=>{event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(SHELL)).then(()=>self.skipWaiting()));});
self.addEventListener("activate",event=>{event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(key=>key.startsWith("streamplus-shell-")&&key!==CACHE).map(key=>caches.delete(key)))).then(()=>self.clients.claim()));});
self.addEventListener("fetch",event=>{
 const req=event.request;
 if(req.method!=="GET"||new URL(req.url).origin!==self.location.origin)return;
 if(req.mode==="navigate"){
  event.respondWith(fetch(req).then(response=>{
   if(response.ok){const copy=response.clone();caches.open(CACHE).then(cache=>cache.put("/streamplus/",copy));}
   return response;
  }).catch(()=>caches.match("/streamplus/")));
  return;
 }
 event.respondWith(caches.match(req).then(hit=>hit||fetch(req)));
});