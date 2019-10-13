// Increase version to force-refresh assets.
var VERSION = 1;
var CACHE_NAME = `www-cache-v${VERSION}`;

var urlsToCache = [
  "/",
  "/static/css/bootstrap.min.css",
  "/static/css/bootstrap.min.css.map",
  "/static/css/custom.css",
  "/static/js/jquery-3.4.1.slim.min.js",
  "/static/js/bootstrap.min.js",
  "/static/js/bootstrap.min.js.map",
  "/static/js/popper.min.js"
];

self.addEventListener("install", function(event) {
  event.waitUntil(installCache());
});

self.addEventListener("fetch", function(event) {
  // Return response right away.
  event.respondWith(fromCache(event.request));
  // Fetch potential update in the background.
  event.waitUntil(update(event.request));
});

function openCache() {
  return caches.open(CACHE_NAME);
}

function installCache() {
  return openCache().then(function(cache) {
    return cache.addAll(urlsToCache);
  });
}

function fromCache(request) {
  return openCache().then(function(cache) {
    return cache.match(request).then(function(response) {
      if (response) {
        // Cache hit.
        return response;
      }
      return fetch(request);
    });
  });
}

function update(request) {
  return openCache().then(function(cache) {
    return fetch(request).then(function(response) {
      return cache.put(request, response);
    });
  });
}
