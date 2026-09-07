(function bootMermaid() {
  function start() {
    if (!window.mermaid) {
      return;
    }
    window.mermaid.initialize({
      startOnLoad: false,
      securityLevel: "strict",
      theme: "base",
      themeVariables: {
        fontFamily: "Manrope, system-ui, sans-serif",
        fontSize: "16px",
        primaryColor: "#eee9e2",
        primaryTextColor: "#1c1917",
        primaryBorderColor: "#c0452a",
        lineColor: "#8a837b",
        secondaryColor: "#ffffff",
        tertiaryColor: "#f9f7f4",
        background: "#f9f7f4",
        mainBkg: "#eee9e2",
        nodeBorder: "#c0452a",
        clusterBkg: "#eee9e2",
        titleColor: "#1c1917",
        edgeLabelBackground: "#f9f7f4",
        actorBkg: "#eee9e2",
        actorBorder: "#c0452a",
        actorTextColor: "#1c1917",
        signalColor: "#c0452a",
        labelTextColor: "#1c1917",
        noteBkgColor: "#eee9e2",
        noteTextColor: "#1c1917",
      },
    });
    window.mermaid.run().catch(function (err) {
      console.error("Mermaid failed to initialize", err);
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
