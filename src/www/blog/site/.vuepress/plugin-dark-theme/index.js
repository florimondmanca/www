const { resolve } = require("path");

module.exports = (options, ctx) => {
  return {
    enhanceAppFiles: [resolve(__dirname, "enhanceApp.js")]
  };
};
