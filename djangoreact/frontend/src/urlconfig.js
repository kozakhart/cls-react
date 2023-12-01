const urlConfig = {
    production: {
      apiUrl: 'https://hartcloud.life:8081/',
      // Other production configuration variables if needed
    },
    development: {
      apiUrl: 'http://localhost:8000/api',
      // Other development configuration variables if needed
    },
    // You can add more environments (e.g., staging, testing) if necessary
  };
  
  export default urlConfig;