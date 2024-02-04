chrome.runtime.onInstalled.addListener(() => {
  console.log("onInstalled...");
});

// get message from content script
chrome.runtime.onMessage.addListener((request, _, __) => {
  if (request.message === "text") {
    const payload = request.payload;
    console.log('Got the text from the page:', payload)
  }
});
