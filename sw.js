const CACHE_NAME = 'chengdu-travel-v4';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './manifest.json',
  'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap',
  // 高德地圖 API 核心檔案 (盡可能快取，但動態圖磚可能無法全部離線)
  'https://webapi.amap.com/maps?v=2.0&key=b53b95a8647efb6d1b77cecbdb7419aa'
];

// 安裝時，快取靜態資源
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
  self.skipWaiting();
});

// 啟動時，清除舊版快取
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            return caches.delete(cache);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// 攔截請求：Stale-While-Revalidate 策略
self.addEventListener('fetch', (event) => {
  // 只攔截 GET 請求
  if (event.request.method !== 'GET') return;

  // 特殊處理第三方 API (如天氣、航班資訊) - Network First, fallback to cache
  if (event.request.url.includes('api.open-meteo.com') || event.request.url.includes('aviationstack.com') || event.request.url.includes('opensky-network.org') || event.request.url.includes('allorigins.win')) {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          // 若成功，更新快取
          const responseClone = response.clone();
          caches.open('chengdu-api-cache').then((cache) => {
            cache.put(event.request, responseClone);
          });
          return response;
        })
        .catch(() => {
          // 斷網時，回傳最後一次的 API 快取
          return caches.match(event.request);
        })
    );
    return;
  }

  // 一般靜態資源：Cache First, fallback to network
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request).then((response) => {
        // 動態將新抓到的資源也加入快取 (避免離線時點擊其他頁面破圖)
        if (response && response.status === 200 && response.type === 'basic') {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        return response;
      });
    })
  );
});
