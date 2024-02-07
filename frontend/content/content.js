window.onload = function () {
  let text = document.documentElement.outerHTML;
  console.log(text);

  fetch("http://127.0.0.1:8000/page", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ pageData: text, pageUrl: window.location.href, pageTitle: document.title}),
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
