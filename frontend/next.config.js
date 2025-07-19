/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  
  // Environment variables
  env: {
    BACKEND_URL: process.env.BACKEND_URL || 'http://localhost:8000',
  },

  // API rewrites for production
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.BACKEND_URL || 'http://localhost:8000'}/api/:path*`,
      },
      {
        source: '/auth/:path*',
        destination: `${process.env.BACKEND_URL || 'http://localhost:8000'}/auth/:path*`,
      },
    ]
  },

  // Image optimization
  images: {
    domains: ['localhost', 'content-creator-pro.railway.app'],
    unoptimized: true,
  },
}

module.exports = nextConfig 