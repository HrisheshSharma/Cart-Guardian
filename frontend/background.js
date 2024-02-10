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
chrome.runtime.onMessage.addListener((request, sender, _) => {
  if (request.message === "text") {
    const payload = request.payload;
    console.log('Got the text from the page:', payload)
  } else if (request.message === "from_index") {
    const payload = request.payload;
    console.log('Got the switch status from index:', payload)
    if (payload.switch_id === 'DefaultDisabler' && payload.switch_response === true) {
      contentScriptPort.postMessage({ response: "Start Default Disabler" });
    } else if (payload.switch_id === 'DefaultDisabler' && payload.switch_response === false) {
      contentScriptPort.postMessage({ response: "Close Default Disabler" });
    } else if (payload.switch_id === 'Review' && payload.switch_response === true) {
      contentScriptPort.postMessage({ response: "Start Review" });
    } else if (payload.switch_id === 'Review' && payload.switch_response === false) {
      contentScriptPort.postMessage({ response: "Close Review" });
    } else if (payload.switch_id === 'Match' && payload.switch_response === true) {
      contentScriptPort.postMessage({ response: "Start Match" });
    } else if (payload.switch_id === 'Match' && payload.switch_response === false) {
      contentScriptPort.postMessage({ response: "Close Match" });
    } else if (payload.switch_id === 'Summarization' && payload.switch_response === true) {
      contentScriptPort.postMessage({ response: "Start Summarization" });
    } else if (payload.switch_id === 'Summarization' && payload.switch_response === false) {
      contentScriptPort.postMessage({ response: "Close Summarization" });
    } else if (payload.switch_id === 'AnalyseDarkPattern' && payload.switch_response === true) {
      contentScriptPort.postMessage({ response: "Analyse Dark Practices" });
    } else if (payload.switch_id === 'PriceTracking' && payload.switch_response === true) {
      contentScriptPort.postMessage({ response: "PriceTracking" });
    }
  }
  else if(request.action === 'pushData') {
    var websiteName = extractDomain(sender.tab.url);

    chrome.storage.local.get(function(result) {
      // console.log(request.data);
      if(websiteName in result){
        result[websiteName].push(request.data);
      }
      else{
        result[websiteName] = [request.data];
      }

      chrome.storage.local.set(result);
    });
  }
  else if(request.action === 'clearData'){
    var websiteName = extractDomain(sender.tab.url);    
    chrome.storage.local.get(function(result) {
      result[websiteName] = [];
      // console.log("cleared the data");
      chrome.storage.local.set(result);
    });
  }
});

function extractDomain(url) {
  var domain;
  try {
    domain = new URL(url).hostname;
  } catch (error) {
    console.error('Error extracting domain:', error);
  }
  return domain;
}

