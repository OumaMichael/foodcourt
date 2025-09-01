// next.config.js (for Vercel)
const path = require("path");

/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "export",   // static export mode
  eslint: { ignoreDuringBuilds: true },
  images: {
    unoptimized: true,
    domains: ["images.pexels.com"],
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
  webpack: (config) => {
    config.resolve.alias["@"] = path.resolve(__dirname);
    return config;
  },
};

module.exports = nextConfig;
