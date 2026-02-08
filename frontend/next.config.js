/** @type {import('next').NextConfig} */
const nextConfig = {
  // ✅ React Strict Mode
  reactStrictMode: true,

  // ✅ Webpack optimization
  webpack: (config, { dev, isServer }) => {
    if (dev && !isServer) {
      // Client-side development cache optimization
      config.cache = {
        type: 'filesystem',
        compression: 'gzip',
        buildDependencies: {
          config: [__filename],
        },
      };
    }
    
    // ✅ Webpack serialization warning fix
    config.infrastructureLogging = {
      level: 'error',
    };
    
    return config;
  },

  // ✅ Supabase env vars
  env: {
    NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
    NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
  },
};

module.exports = nextConfig;
