/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
    screens: {
      '2xl': '1800px',
    }
  },
  plugins: [
    require('@vueform/slider/tailwind'),
  ],
}
