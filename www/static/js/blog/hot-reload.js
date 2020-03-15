function wsContentReload(ws) {
  let pingInterval;

  ws.onopen = message => {
    console.debug("Connected:", message);
    pingInterval = setInterval(() => ws.send("reload:ping"), 500);
  };

  ws.onmessage = message => {
    console.debug("Message:", message);
    if (message.data === "reload") {
      document.location.reload(true);
    }
  };

  ws.onclose = message => {
    console.debug("Closed:", message);
    clearInterval(pingInterval);
  };
}
