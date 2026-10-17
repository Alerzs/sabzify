/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './website/templates/**/*.html',
    './website/forms.py',
  ],
  theme: {
    extend: {
      colors: {
        sabz: {
          DEFAULT: '#1C7E68',
          dark: '#146454',
          deep: '#0E3D34',
        },
        gold: {
          DEFAULT: '#FFDD00',
          soft: '#FFF4A8',
        },
      },
      fontFamily: {
        sans: ['Vazirmatn', 'Tahoma', 'sans-serif'],
      },
      boxShadow: {
        card: '0 16px 40px rgba(16, 40, 32, 0.08)',
        nav: '0 10px 40px rgba(0, 0, 0, 0.08)',
      },
    },
  },
  plugins: [],
}
