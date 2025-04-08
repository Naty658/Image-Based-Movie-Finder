window.addEventListener("load", async () => {
  const text = document.body.innerText;

  try {
    await fetch("http://localhost:5000/save-text", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text })
    });

    console.log("✅ Text sent to server");
  } catch (err) {
    console.error("❌ Failed to send text:", err);
  }
});
