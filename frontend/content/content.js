window.onload = function () {
  let text = document.body.outerHTML;
  console.log(text);

  fetch("http://127.0.0.1:8000/page", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ pageData: text, pageUrl: window.location.href, pageTitle: document.title }),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
    })
    .catch((err) => {
      console.error(err);
    });
  chrome.runtime.sendMessage({
    message: 'text',
    payload: text
  });
};

// Establish a connection with the background script
const port = chrome.runtime.connect({ name: "content-script" });
port.onMessage.addListener((msg) => {
  if(msg.response === "Start Default Disabler"){
    defaultDisable();
  }
});

function defaultDisable() {
  var inputs = document.querySelectorAll('input, select, textarea');
  inputs.forEach(function(input) {
    if (input.type === 'text' || input.type === 'password' || input.type === 'email' || input.type === 'search' || input.type === 'tel' || input.type === 'url') {
      input.value = '';
    } else if (input.type === 'checkbox' || input.type === 'radio') {
      input.checked = false;
    } else if (input.type === 'number') {
      input.value = '';
    } else if (input.type === 'range') {
        input.value = 0;
    } else if (input.type === 'file') {
      input.value = null;
    } else if (input.type === 'select-one' || input.type === 'select-multiple') {
      input.selectedIndex = -1;
    } else if (input.nodeName === 'TEXTAREA') {
      input.value = '';
    }
  });
}
