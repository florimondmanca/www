const markdown = require("./markdown");

module.exports = {
  base: "/blog/",
  markdown,
  plugins: [
    ["@vuepress/google-analytics", { ga: "UA-122676386-2" }],
    [
      "vuepress-plugin-autometa",
      {
        site: {
          name: "Florimond Manca",
          twitter: "florimondmanca"
        },
        // NOTE: this is broken for now, see:
        // https://github.com/webmasterish/vuepress-plugin-autometa/pull/6
        canonical_base: "https://florimond.dev/blog"
      }
    ],
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
            type: String,
            required: false
          },
          image_caption: {
            type: String,
            required: false
          },
          // Added by the autometa plugin.
          meta: {
            type: Object,
            required: true
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
