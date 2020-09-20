module.exports = {
  future: {
    // See: https://tailwindcss.com/docs/upcoming-changes
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true,
  },
  purge: {
    content: ["./server/templates/**/*.jinja"],
  },
  theme: {
    colors: {
      background: "#FFFFFF",
      surface: "#edeff0",
      primary: "#478cc9",
      accent: "#ea3b53",
      muted: {
        default: "#6b6b6b",
        700: "#d1d1d1",
      },
      warn: "#f1714f",
      on: {
        background: "#424242",
      },
    },
    fontFamily: {
      body: ["EB Garamond", "serif"],
    },
    fontWeight: {
      normal: "normal",
      bold: "700",
      black: "900",
    },
    fontSize: {
      sm: "0.8rem",
      base: "1rem",
      lg: "1.4rem",
      xl: "1.8rem",
      "2xl": "2.2rem",
      "3xl": "2.5rem",
    },
    lineHeight: {
      sm: "1.2",
      normal: "1.5",
    },
    screens: {
      tablet: "720px",
    },
  },
};
