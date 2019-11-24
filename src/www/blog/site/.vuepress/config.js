const markdown = require("./markdown");
const sharedConfig = require("./config.shared.json");

module.exports = {
  title: "Florimond Manca",
  description: "A blog about my ongoing journey through software engineering.",
  base: "/blog/",
  markdown,
  plugins: [
    require("./plugin-blog"),
    ["@vuepress/google-analytics", { ga: "UA-122676386-2" }],
    ["vuepress-plugin-sitemap", { hostname: "https://florimond.dev" }],
    [
      "vuepress-plugin-feed",
      {
        canonical_base: "https://florimond.dev/blog",
        posts_directories: ["articles"],
        feeds: {
          // Only expose RSS.
          json1: { enable: false },
          atom1: { enable: false },
          rss2: {
            enable: true,
            file_name: sharedConfig.rss_feed_file_name,
            // Disable automatic RSS head <link> generation
            // as it is added by us.
            head_link: { enable: false }
          }
        }
      }
    ],
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
          },
          // Used by `vuepress-plugin-feed`.
          feed: {
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
    ],
    [
      "link",
      {
        rel: "alternate",
        type: "application/rss+xml",
        href: `https://florimond.dev/blog/${sharedConfig.rss_feed_file_name}`,
        title: "Florimond Manca RSS Feed"
      }
    ]
  ]
};
