/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'performance-excellent': '#FF00FF',
        'performance-pass': '#99FA99',
        'performance-marginal-fail': '#FFFF00',
        'performance-fail': '#FF0000',
        'performance-cannot-evaluate': '#D3D3D3',
        'performance-unknown': '#D3D3D3',
        'table-header-bg': '#808080',
        'table-header-text': '#F5F5F5',
        'table-body-bg': '#F5F5DC',
        'table-grid': '#000000',
      },
    },
  },
  plugins: [],
}
