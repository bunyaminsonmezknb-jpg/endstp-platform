/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'end-purple': '#667eea',
        'end-purple-dark': '#764ba2',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'shake': 'shake 0.5s infinite',
        'blink': 'blink 1s infinite',
        'shine': 'shine 3s infinite',
        'slideIn': 'slideIn 0.3s ease',
      },
      keyframes: {
        shake: {
          '0%, 100%': { transform: 'translateX(0)' },
          '25%': { transform: 'translateX(-5px)' },
          '75%': { transform: 'translateX(5px)' },
        },
        blink: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.7' },
        },
        shine: {
          '0%': { left: '-100%' },
          '50%, 100%': { left: '100%' },
        },
        slideIn: {
          from: {
            opacity: '0',
            transform: 'translateY(-50px)',
          },
          to: {
            opacity: '1',
            transform: 'translateY(0)',
          },
        },
      },
    },
  },
  plugins: [],
}
