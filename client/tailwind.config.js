/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "node_modules/flowbite-react/**/*.{js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      scale: {
        '200': '2',
        '250': '2.5',
        '300': '3',
        '400': '4',
        
      },
      border: {

      }
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
}