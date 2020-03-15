function setupHotReload(ws) {
  let pingInterval;

  ws.onopen = event => {
    console.debug("Connected:", event);
    pingInterval = setInterval(() => ws.send("reload:ping"), 500);
  };

  ws.onmessage = event => {
    console.debug("Message:", event);
    if (event.data === "reload") {
      document.location.reload(true);
    }
  };

  ws.onclose = event => {
    console.debug("Closed:", event);
    clearInterval(pingInterval);
  };
}
