document.getElementById("copyBtn").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      const text = document.documentElement.innerText || "No readable text found.";

      fetch("http://localhost:5000/save-text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text })
      }).then(() => {
        alert("✅ Search result text sent to your app!");
      }).catch(err => {
        alert("❌ Failed to send text.");
      });
    }
  });
});
