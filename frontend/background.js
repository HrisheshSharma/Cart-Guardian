chrome.runtime.onInstalled.addListener(() => {
  console.log("onInstalled...");
});

// Listen for connections from content scripts
let contentScriptPort;
chrome.runtime.onConnect.addListener((port) => {
  console.assert(port.name === "content-script");
  contentScriptPort = port;
  console.log("Connected to content-script");
});


// get message from scripts
chrome.runtime.onMessage.addListener((request, _, __) => {
  if (request.message === "text") {
    const payload = request.payload;
    console.log('Got the text from the page:', payload)
  } else if (request.message === "from_index") {
    const payload = request.payload;
    console.log('Got the switch status from index:', payload)
    if (payload.switch_id === 'DefaultDisabler' && payload.switch_response === true) {
      contentScriptPort.postMessage({ response: "Start Default Disabler" });
    }
  }
});
