module.exports = {
  base: "/blog/",
  plugins: [
    require("./plugin-blog"),
    require("./plugin-legacy-blog-url-mapping")
  ],
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
