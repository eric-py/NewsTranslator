/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/*.{html,}",
    "./app/templates/**/*.{html,}",
    "./app/static/js/*.{js,}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: '#6366F1',
        secondary: '#8B5CF6',
        accent: '#F59E0B',
      },
      fontFamily: {
        'vazirmatn': ['Vazirmatn', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        }
      },
    }
  },
  plugins: [],
}