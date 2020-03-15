function setupHotReload(ws) {
  ws.onopen = event => {
    console.debug("Connected:", event);
  };

  ws.onmessage = event => {
    console.debug("Message:", event);
    if (event.data === "reload") {
      document.location.reload(true);
    }
  };

  ws.onclose = event => {
    console.debug("Closed:", event);
  };
}
