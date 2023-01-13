module.exports = {
  content: [
    "./server/web/templates/**/*.jinja",
  ],
  theme: {
    colors: {
      background: "#FFFFFF",
      surface: "#edeff0",
      link: "#478cc9",
      primary: {
        DEFAULT: "#3eab9b",
        600: "#47bdaa",
      },
      accent: "#ea3b53",
      muted: {
        500: "#6b6b6b",
        700: "#d1d1d1",
      },
      warn: "#f1714f",
      on: {
        primary: "#000000",
        background: "#424242",
      },
    },
    extend: {
      screens: {
        print: {
          raw: "print" // Allow `class="print:..."` = `@media print { ... }`
        },
      },
    },
    fontFamily: {
      body: [
        "Georgia", // Linux, Mac, iOS, Windows 
        "serif", // The rest (eg Droid Serif on Android)
      ],
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
