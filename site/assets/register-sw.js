if ('serviceWorker' in navigator && location.protocol === 'https:') {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js').catch((error) => {
      console.warn('A gyorsítótár-szolgáltatás nem indult el:', error);
    });
  });
}
