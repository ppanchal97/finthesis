module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Roboto', 'sans-serif']  // Ensures Roboto is the default sans-serif font
      },
      fontSize: {
        'news-title': '32px',  // Custom font size for news titles
        'news-description': '24px',  // Custom font size for descriptions
        'navbar-text': '18px', // Custom font size for the navbar
      },
      colors: {
        'active-bg': '#464B53', // Background for selected card
        'inactive-bg': '#17191B', // Background for unselected card
        darkgray: '#27292D',
        darkblue: '#464B53',
        titleorange: '#FFAF50',
        'lightblue': '#F5F8FD',
        'gray-500': '#626466',
      }
    },
  },
  plugins: [],
}
