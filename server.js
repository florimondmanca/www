const express = require("express");
const path = require("path");
const morgan = require("morgan");

const app = express();
app.use(morgan("combined"));

const PORT = process.env.PORT || 4200;
const HOST = process.env.HOST || "0.0.0.0";
const PUBLIC_FOLDER = path.join(__dirname, "public");

// Serve static files from /public
app.get("*.*", express.static(PUBLIC_FOLDER));

// All other routes go to index.html
app.get("*", function(req, res) {
  res.sendFile(path.join(PUBLIC_FOLDER, "index.html"));
});

// Start up the Node server
app.listen(PORT, HOST, () => {
  console.log(`Server listening on http://${HOST}:${PORT}`);
});
