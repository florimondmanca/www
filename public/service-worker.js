var CACHE_NAME = 'portfolio-cache-v1';
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
  // Perform install steps
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Cache hit - return response
        if (response) {
          return response;
        }
        return fetch(event.request);
      }
    )
  );
});
