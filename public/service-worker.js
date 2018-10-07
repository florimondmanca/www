var CACHE = 'portfolio-cache-v1';
var urlsToCache = [
  '/',
  '/styles/fonts.css',
  '/styles/styles.css',
  '/styles/variables.css',
  '/styles/fonts/agane-heavy.ttf',
  '/styles/fonts/agane-light.ttf',
  '/styles/fonts/agane-regular.ttf',
  '/scripts/subtitle.js',
  '/scripts/register-service-worker.js',
];

self.addEventListener('install', function(event) {
  event.waitUntil(installCache());
});


self.addEventListener('fetch', function(event) {
  // Return response right away
  event.respondWith(fromCache(event.request));
  // Fetch potential update in the background
  event.waitUntil(update(event.request));
});


function installCache() {
  return caches.open(CACHE).then(function(cache) {
    return cache.addAll(urlsToCache);
  });
}

function fromCache(request) {
  return caches.open(CACHE).then(function(cache) {
    return cache.match(request).then(function(response) {
      if (response) {
        // Cache hit - return response
        return response;
      }
      return fetch(request);
    });
  });
}

function update(request) {
  return caches.open(CACHE).then(function(cache) {
    return fetch(request).then(function(response) {
      return cache.put(request, response);
    });
  });
}
