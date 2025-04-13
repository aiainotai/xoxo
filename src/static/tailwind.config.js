/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [".src/templates/**/*.{html,js}"],
  theme: {
    container: {
      center: true,
      padding: "6rem",
    },
    extend: {
      fontFamily: {
        sans: ["Ubuntu", "sans-serif"],
        poppins: ["Poppins", "sans-serif"],
        playfair: ["Playfair Display", "serif"],
      },
    },
  },
  plugins: [],
};
