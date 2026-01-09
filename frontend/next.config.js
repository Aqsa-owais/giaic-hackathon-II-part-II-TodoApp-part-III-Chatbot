/** @type {import('next').NextConfig} */
const nextConfig = {
  // appDir is now enabled by default in Next.js 13+ when you have an app directory
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
};

module.exports = nextConfig;