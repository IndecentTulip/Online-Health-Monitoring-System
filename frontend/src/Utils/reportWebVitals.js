const reportWebVitals = (onPerfEntry) => {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
      // Log each metric's name and value (simplified)
      
      getCLS((metric) => {
        console.log('CLS (Cumulative Layout Shift):', metric.value);
        onPerfEntry(metric);  // Optional: callback for further processing
      });

      getFID((metric) => {
        console.log('FID (First Input Delay):', metric.value);
        onPerfEntry(metric);
      });

      getFCP((metric) => {
        console.log('FCP (First Contentful Paint):', metric.value, 'ms');
        onPerfEntry(metric);
      });

      getLCP((metric) => {
        console.log('LCP (Largest Contentful Paint):', metric.value, 'ms');
        onPerfEntry(metric);
      });

      getTTFB((metric) => {
        console.log('TTFB (Time to First Byte):', metric.value, 'ms');
        onPerfEntry(metric);
      });
    });
  }
};

export default reportWebVitals;

