module.exports = {
  base: "/blog/",
  plugins: [
    require("./plugin-blog"),
    [
      require("vuepress-frontmatter-lint"),
      {
        abortBuild: true,
        exclude: ["/", "/tag/*"],
        specs: {
          home: {
            type: Boolean,
            required: false
          },
          published: {
            type: Boolean,
            required: true
          },
          permalink: {
            type: String,
            required: false
          },
          title: {
            type: String,
            required: true
          },
          description: {
            type: String,
            required: true
          },
          date: {
            type: String,
            required: true
          },
          legacy_url: {
            type: String,
            required: false
          },
          tags: {
            type: Array,
            required: false
          },
          image: {
            type: Object,
            required: false
          }
        }
      }
    ]
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
