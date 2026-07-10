/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,ts}"],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eafff6',
          100: '#c5ffea',
          200: '#8effd8',
          300: '#00e5a0',
          400: '#00cc8e',
          500: '#00b37d',
          600: '#009a6b',
          700: '#00805a',
          800: '#006749',
          900: '#004d37',
        },
        surface: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          700: '#1e293b',
          800: '#111827',
          900: '#0a0e17',
          950: '#060a12',
        }
      },
      fontFamily: {
        display: ['Space Grotesk', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
};