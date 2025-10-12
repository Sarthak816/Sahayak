/** @type {import('tailwindcss').Config} */
import { green, blue, red } from '@radix-ui/colors'
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    screens: {
      xs: '480px', // Very small devices (e.g. small phones)
      sm: '640px', // Small phones
      md: '768px', // Tablets
      lg: '992px', // Small laptops / large tablets
      xl: '1200px', // Laptops / desktops
      '2xl': '1440px', // Large desktops / HD monitors
      '3xl': '1600px', // Extra large screens
      '4k': '1920px', // 1080p and above
    },
    extend: {
      fontFamily: {
        sans: ['Manrope', 'sans-serif'],
        serif: ['Source Serif Pro', 'serif'],
      },

      spacing: {},
      borderRadius: {},
      colors: {
        teal: {
          50: 'rgba(25, 96, 98, 0.05)',
          100: 'rgba(25, 96, 98, 0.1)',
          600: '#196062',
          700: '#196062',
          800: '#145154',
        },
        'dark-green': '#196062',
        ...green,
        ...blue,
        ...red,
      },
    },
  },
}
