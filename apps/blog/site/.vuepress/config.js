module.exports = {
  base: "/blog/",
  plugins: [require("./plugin-blog")],
  head: [
    // Icons.
    [
      "link",
      {
        href: "https://fonts.googleapis.com/icon?family=Material+Icons",
        rel: "stylesheet"
      }
    ],
    // Markdown rendering.
    [
      "script",
      {
        src: "https://unpkg.com/marked@0.7.0"
      }
    ],
    [
      "script",
      {
        src: "https://kit.fontawesome.com/d38a96501e.js",
        crossorigin: "anonymous"
      }
    ]
  ]
};
