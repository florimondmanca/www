module.exports = {
  base: "/blog/",
  plugins: [require("./plugin-blog")],
  head: [
    // Icons.
    [
      "script",
      {
        src: "https://kit.fontawesome.com/d38a96501e.js",
        crossorigin: "anonymous"
      }
    ]
  ]
};
