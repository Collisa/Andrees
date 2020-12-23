const colors = require("tailwindcss/colors");

module.exports = {
  purge: {
    content: ["templates/*.html", "templates/**/*.html"],
  },
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        teal: colors.teal,
      },
      maxHeight: {
        112: "28rem",
        128: "32rem",
        144: "36rem",
      },
    },
  },
  variants: {
    extend: {
      ringWidth: ["hover", "active"],
      zIndex: ["hover", "active"],
      borderWidth: ["hover", "focus"],
      backgroundColor: ["odd"],
    },
  },
  plugins: [],
};
