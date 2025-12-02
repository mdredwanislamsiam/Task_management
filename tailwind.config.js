/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // top-level templates folder
    "./**/templates/**/*.html", // templates inside apps
    "./**/*.html", // any other HTML anywhere
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};

