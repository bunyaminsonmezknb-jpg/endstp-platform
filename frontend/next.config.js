/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  // ✅ Development'ta browser cache'i devre dışı bırak
  async headers() {
    if (process.env.NODE_ENV === 'development') {
      return [
        {
          source: '/:path*',
          headers: [
            {
              key: 'Cache-Control',
              value: 'no-store, no-cache, must-revalidate, proxy-revalidate',
            },
            {
              key: 'Pragma',
              value: 'no-cache',
            },
            {
              key: 'Expires',
              value: '0',
            },
          ],
        },
      ];
    }
    return [];
  },

  webpack: (config, { dev, isServer }) => {
    if (dev && !isServer) {
      config.cache = {
        type: 'filesystem',
        compression: 'gzip',
        buildDependencies: {
          config: [__filename],
        },
      };
    }
    
    config.infrastructureLogging = {
      level: 'error',
    };
    
    return config;
  },

  env: {
    NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
    NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
  },
};

module.exports = nextConfig;
