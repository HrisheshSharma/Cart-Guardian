let defaultDisablerActive = false;
let iframeActive = false;
let matchActive = false;
let priceTrackingActive = false;
let summarizationActive = false;
let anyToggleActive = false;
let analyseDarkPractice = false;

window.onload = function () {
  console.log("Window loaded");
  console.log("anyToggleActive is: ", anyToggleActive);
  if (anyToggleActive) {
    send_HTML_to_server();
  }
  // Check if default disabler was active before
  if (defaultDisablerActive) {
    defaultDisable();
  }
  // Check if iframe was active before
  console.log("iframe is: ", iframeActive);
  if (iframeActive) {
    init_review();
  }

  if (summarizationActive) {
    init_policy();
  }
};

// Establish a connection with the background script
const port = chrome.runtime.connect({ name: "content-script" });
port.onMessage.addListener((msg) => {
  console.log("Message received in content script: ", msg);
  if (msg.response === "Report") {
    reportWebsite();
    console.log("Report started");
  }
  if (!anyToggleActive) {
    let text = document.documentElement.outerHTML;
    console.log(text);
    fetch("http://127.0.0.1:8000/page", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        pageData: text,
        pageUrl: window.location.href,
        pageTitle: document.title,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        anyToggleActive = true;
        if (msg.response === "Start Default Disabler") {
          defaultDisable();
          defaultDisablerActive = true;
        } else if (msg.response === "Close Default Disabler") {
          defaultDisablerActive = false;
        } else if (msg.response === "Start Review") {
          init_review();
          console.log("Review started");
        } else if (msg.response === "Close Review") {
          close_review();
          console.log("Review closed");
        } else if (msg.response === "Start Match") {
          create_mismatch_modal();
          console.log("Match started");
        } else if (msg.response === "Close Match") {
          matchActive = false;
          var modal = document.getElementById("mismatchModal");
          modal.style.display = "none";
          modal.parentElement.removeChild(modal);
        } else if (msg.response === "Start Summarization") {
          init_policy();
          console.log("Summarization started");
        } else if (msg.response === "Close Summarization") {
          close_policy();
          console.log("Summarization closed");
        } else if (msg.response === "Analyse Dark Practices") {
          analyse_dark_practice();
          analyseDarkPractice = true;
          console.log("Analyse Dark Practice started");
        }
      })
      .catch((err) => {
        console.error(err);
      });
    chrome.runtime.sendMessage({
      message: "text",
      payload: text,
    });
  } else {
    anyToggleActive = true;
    if (msg.response === "Start Default Disabler") {
      defaultDisable();
      defaultDisablerActive = true;
    } else if (msg.response === "Close Default Disabler") {
      defaultDisablerActive = false;
    } else if (msg.response === "Start Review") {
      init_review();
      console.log("Review started");
    } else if (msg.response === "Close Review") {
      close_review();
      console.log("Review closed");
    } else if (msg.response === "Start Match") {
      create_mismatch_modal();
      console.log("Match started");
    } else if (msg.response === "Close Match") {
      matchActive = false;
      var modal = document.getElementById("mismatchModal");
      modal.style.display = "none";
      modal.parentElement.removeChild(modal);
    } else if (msg.response === "Start Summarization") {
      init_policy();
      console.log("Summarization started");
    } else if (msg.response === "Close Summarization") {
      close_policy();
      console.log("Summarization closed");
    } else if (msg.response === "Analyse Dark Practices") {
      analyse_dark_practice();
      analyseDarkPractice = true;
      console.log("Analyse Dark Practice started");
    }
  }
});

function send_HTML_to_server() {
  let text = document.documentElement.outerHTML;
  console.log(text);
  fetch("http://127.0.0.1:8000/page", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      pageData: text,
      pageUrl: window.location.href,
      pageTitle: document.title,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
    })
    .catch((err) => {
      console.error(err);
    });
  chrome.runtime.sendMessage({
    message: "text",
    payload: text,
  });
}

function defaultDisable() {
  var inputs = document.querySelectorAll("input, select, textarea");
  inputs.forEach(function (input) {
    if (
      input.type === "text" ||
      input.type === "password" ||
      input.type === "email" ||
      input.type === "search" ||
      input.type === "tel" ||
      input.type === "url"
    ) {
      input.value = "";
    } else if (input.type === "checkbox" || input.type === "radio") {
      input.checked = false;
    } else if (input.type === "number") {
      input.value = "";
    } else if (input.type === "range") {
      input.value = 0;
    } else if (input.type === "file") {
      input.value = null;
    } else if (
      input.type === "select-one" ||
      input.type === "select-multiple"
    ) {
      input.selectedIndex = -1;
    } else if (input.nodeName === "TEXTAREA") {
      input.value = "";
    }
  });
}

init_review = function () {
  // Inject CSS
  var style = document.createElement("style");
  style.textContent = `
    .side-window {
      height: 100%;
      width: 0;
      position: fixed;
      z-index: 1000;
      top: 0;
      right: 0;
      background-color: white;
      opacity: 1;
      overflow-x: hidden;
      transition: 0.5s;
      // padding-top: 60px;
    }

    .side-window a {
      padding: 8px 8px 8px 32px;
      text-decoration: none;
      font-size: 25px;
      color: #818181;
      display: block;
      transition: 0.3s;
    }

    .side-window a:hover {
      color: #f1f1f1;
    }

    .side-window .closebtn {
      position: absolute;
          top: 0;
          right: 25px;
          font-size: 36px;
          margin-left: 50px;
        }
  `;
  document.head.appendChild(style);
  // Create iframe
  var iframe = document.createElement("iframe");
  iframe.id = "myIframe1";
  iframe.style.position = "fixed";
  iframe.style.height = "100%";
  iframe.style.width = "270px";
  iframe.style.top = "0";
  iframe.style.right = "0";
  iframe.style.zIndex = "1000";
  iframe.style.border = "none";
  iframe.style.overflow = "hidden";
  iframe.style.transition = "0.5s";
  iframe.style.backgroundColor = "white";
  // Create side window div
  var sideWindow = document.createElement("div");
  sideWindow.id = "mySideWindow";
  sideWindow.className = "side-window";

  var reviews;
  // Fetch reviews
  fetch("http://127.0.0.1:8000/reviews", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((data) => {
      reviews = data;
      console.log("Reviews is: ", reviews);
      reviews.forEach(function (review) {
        console.log("Review is: ", review);
        var card = create_card(review, "review");
        sideWindow.appendChild(card);
      });
    })
    .catch((err) => {
      console.error(err);
    });

  // Add additional content to side window

  sideWindow.innerHTML += `
    <h2>Expert Reviews</h2>
    <p>Following are some of the expert reviews from various sources.</p>
    `;
  var closeButton = document.createElement("button");
  closeButton.textContent = "X";
  closeButton.style.position = "absolute";
  closeButton.style.top = "2px";
  closeButton.style.right = "2px";
  closeButton.addEventListener("click", function () {
    iframeActive = false;
    iframe.style.width = "0";
    iframe.parentElement.removeChild(iframe);
  });

  // Append side window to iframe
  iframe.onload = function () {
    iframe.contentDocument.body.appendChild(sideWindow);
    iframe.contentDocument.body.appendChild(closeButton);
  };
  // Append iframe to body
  iframeActive = true;
  iframe.style.width = "250px";
  document.body.appendChild(iframe);
};

close_review = function () {
  var iframe = document.getElementById("myIframe1");
  console.log("iframe is: ", iframe);
  console.log("iframe width is: ", iframe.style.width);
  iframeActive = false;
  iframe.style.width = "0";
  console.log("iframe new width is: ", iframe.style.width);
  iframe.parentElement.removeChild(iframe);
};

create_card = function (review, card_type) {
  var card = document.createElement("div");
  // card.style.width = "100%";
  card.style.border = "1px solid #000";
  card.style.padding = "5px";
  card.style.marginBottom = "10px";
  card.style.borderRadius = "10px";

  // Create a website
  var website = document.createElement("h3");
  website.textContent = review.website; // Assuming review has a website property
  website.style.marginBlockStart = "0.5rem";
  website.style.marginBlockEnd = "0.5rem";
  card.appendChild(website);

  // Create a link
  var link = document.createElement("a");
  link.href = review.link;
  link.target = "_blank";
  link.textContent = "Read More";
  card.appendChild(link);

  console.log(card_type);
  // Create a text area
  if (card_type === "review") {
    var textArea = document.createElement("p");
    textArea.textContent = review.review; // Assuming review has a review property
    textArea.style.fontSize = "14px";
    card.appendChild(textArea);
  } else if (card_type === "policy") {
    var textAll = review.review;
    var textAllList = textAll.split("•");
    console.log("textAllList is: ", textAllList);
    var ul = document.createElement("ul");
    card.appendChild(ul);
    textAllList.slice(1).forEach(function (text) {
      var li = document.createElement("li");
      li.textContent = text;
      li.style.fontSize = "14px";
      ul.appendChild(li);
    });
  }
  // var textArea = document.createElement('p');
  // textArea.textContent = review.review; // Assuming review has a review property
  // textArea.style.fontSize = "14px";
  // card.appendChild(textArea);
  return card;
};

create_mismatch_modal = function () {
  fetch("http://127.0.0.1:8000/match", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((data) => {
      console.log("Match is: ", data);
      if (data === false) {
        createModal();
        matchActive = true;
      } else {
        matchActive = true;
      }
    })
    .catch((err) => {
      console.error(err);
    });
};

const createModal = function () {
  // Create a modal element
  var modal = document.createElement("div");
  modal.id = "mismatchModal";
  modal.style.position = "fixed";
  modal.style.top = "0";
  modal.style.left = "0";
  modal.style.width = "100%";
  modal.style.height = "100%";
  modal.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
  modal.style.display = "flex";
  modal.style.justifyContent = "center";
  modal.style.alignItems = "center";
  modal.style.zIndex = "1000";

  // Create a modal content container
  var modalContent = document.createElement("div");
  modalContent.style.backgroundColor = "#fff";
  modalContent.style.padding = "20px";
  modalContent.style.border = "1px solid #000";
  modalContent.style.position = "relative";
  // Create a close button
  var closeButton = document.createElement("button");
  closeButton.textContent = "X";

  closeButton.style.position = "absolute";
  closeButton.style.top = "2px";
  closeButton.style.right = "2px";
  closeButton.addEventListener("click", function () {
    matchActive = false;
    modal.style.display = "none";
    modal.parentElement.removeChild(modal);
  });

  modalContent.appendChild(closeButton);

  var text = document.createElement("p");
  text.style.color = "red";
  text.textContent = "The Product Image and Description might NOT match !!!";

  modalContent.appendChild(text);

  modal.appendChild(modalContent);

  // Append the modal to the document body
  document.body.appendChild(modal);
};

init_policy = function () {
  // Inject CSS
  var style = document.createElement("style");
  style.textContent = `
    .side-window {
      height: 100%;
      width: 0;
      position: fixed;
      z-index: 1000;
      top: 0;
      right: 0;
      background-color: white;
      opacity: 1;
      overflow-x: hidden;
      transition: 0.5s;
      // padding-top: 60px;
    }

    .side-window a {
      padding: 8px 8px 8px 32px;
      text-decoration: none;
      font-size: 25px;
      color: #818181;
      display: block;
      transition: 0.3s;
    }

    .side-window a:hover {
      color: #f1f1f1;
    }

    .side-window .closebtn {
      position: absolute;
          top: 0;
          right: 25px;
          font-size: 36px;
          margin-left: 50px;
        }
  `;
  document.head.appendChild(style);
  // Create iframe
  var iframe = document.createElement("iframe");
  iframe.id = "myIframe2";
  iframe.style.position = "fixed";
  iframe.style.height = "100%";
  iframe.style.width = "270px";
  iframe.style.top = "0";
  iframe.style.right = "0";
  iframe.style.zIndex = "1000";
  iframe.style.border = "none";
  iframe.style.overflow = "hidden";
  iframe.style.transition = "0.5s";
  iframe.style.backgroundColor = "white";
  // Create side window div
  var sideWindow = document.createElement("div");
  sideWindow.id = "mySideWindow";
  sideWindow.className = "side-window";

  var reviews;
  // Fetch reviews
  fetch("http://127.0.0.1:8000/tandc", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((data) => {
      reviews = data;
      console.log("Reviews is: ", reviews);
      reviews.forEach(function (review) {
        console.log("Review is: ", review);
        var card = create_card(review, "policy");
        sideWindow.appendChild(card);
      });
    })
    .catch((err) => {
      console.error(err);
    });

  // Add additional content to side window

  sideWindow.innerHTML += `
    <h2>Policy Summarization</h2>
    <p>Following are some of the summarized policies from various sources on this page.</p>
    `;
  var closeButton = document.createElement("button");
  closeButton.textContent = "X";
  closeButton.style.position = "absolute";
  closeButton.style.top = "2px";
  closeButton.style.right = "2px";
  closeButton.addEventListener("click", function () {
    summarizationActive = false;
    iframe.style.width = "0";
    iframe.parentElement.removeChild(iframe);
  });

  // Append side window to iframe
  iframe.onload = function () {
    iframe.contentDocument.body.appendChild(sideWindow);
    iframe.contentDocument.body.appendChild(closeButton);
  };
  // Append iframe to body
  summarizationActive = true;
  iframe.style.width = "250px";
  document.body.appendChild(iframe);
};

close_policy = function () {
  var iframe = document.getElementById("myIframe2");
  console.log("iframe is: ", iframe);
  console.log("iframe width is: ", iframe.style.width);
  summarizationActive = false;
  iframe.style.width = "0";
  console.log("iframe new width is: ", iframe.style.width);
  iframe.parentElement.removeChild(iframe);
};

function analyse_dark_practice() {
  var style = document.createElement("style");
  style.textContent = `
  .tooltip {
    position: relative;
    display: inline-block;
    border-bottom: 1px dotted black; /* If you want a dotted underline */
  }
  
  .tooltip .tooltiptext {
    visibility: hidden;
    width: 200px;
    background-color: black;
    color: #fff;
    text-align: center;
    padding: 5px 0;
    border-radius: 6px;
  
    /* Position the tooltip text */
    position: absolute;
    z-index: 1;
    top: 100%;
    left: 50%;
    margin-left: -60px; /* Use half of the width value to center the tooltip */
  
    /* Fade in tooltip */
    opacity: 0;
    transition: opacity 0.3s;
  }
  
  .tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
  }
  `;
  document.head.appendChild(style);
  fetch("http://127.0.0.1:8000/pattern", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((data) => {
      // console.log("Dark practice is: ", data);
      if (data) {
        // for (let i=0; i<data.length; i++){
        console.log("Data is: ", data);
        let elements = document.querySelectorAll("div");
        console.log("Elements are: ", elements);
        let div_list = data.div;
        for (let j = 0; j < div_list.length; j++) {
          let pos = div_list[j].pos;
          console.log("Position is: ", pos);
          //let type_of_practice= div_list[j].type_of_practice;
          elements[pos].style.backgroundColor = "#FFFF00";
          elements[pos].style.border = "2px solid #FF0000";
          elements[pos].style.color = "#FF0000";
          elements[pos].style.fontWeight = "bold";
          elements[pos].className += " tooltip";
          let span = document.createElement("span");
          span.className = "tooltiptext";
          span.textContent = div_list[j].pattern;
          elements[pos].appendChild(span);
          //element[pos].title= type_of_practice;
        }
        // }
        analyseDarkPractice = true;
      } else {
        analyseDarkPractice = true;
      }
    });
}

reportWebsite = function () {
  console.log("Report button clicked");
  // Create a modal element
  var modal = document.createElement("div");
  modal.id = "reportModal";
  modal.style.position = "fixed";
  modal.style.top = "0";
  modal.style.left = "0";
  modal.style.width = "100%";
  modal.style.height = "100%";
  modal.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
  modal.style.display = "flex";
  modal.style.justifyContent = "center";
  modal.style.alignItems = "center";
  modal.style.zIndex = "1000";

  // Create a modal content container
  var modalContent = document.createElement("div");
  modalContent.style.backgroundColor = "#fff";
  modalContent.style.padding = "20px";
  modalContent.style.border = "1px solid #000";
  modalContent.style.position = "relative";
  modalContent.style.width = "50%";
  modalContent.style.display = "flex";
  modalContent.style.flexDirection = "column";
  modalContent.style.justifyContent = "space-between";
  // Create a close button
  var closeButton = document.createElement("button");
  closeButton.textContent = "X";
  closeButton.style.position = "absolute";
  closeButton.style.top = "2px";
  closeButton.style.right = "2px";
  closeButton.style.cursor = "pointer";
  closeButton.addEventListener("click", function () {
    modal.style.display = "none";
    modal.parentElement.removeChild(modal);
  });

  modalContent.appendChild(closeButton);

  // Add a form with one inoput field, one select field and a submit button
  var form = document.createElement("form");
  form.style.display = "flex";
  form.style.flexDirection = "column";
  form.style.gap = "10px";
  // Add an input field
  var input = document.createElement("input");
  input.type = "text";
  input.style.marginBottom = "15px";
  input.style.padding = "10px";
  input.style.border = "1px solid #ccc";
  input.style.borderRadius = "4px";
  input.placeholder = "Enter Pattern";
  form.appendChild(input);
  // Add a select field
  var select = document.createElement("select");
  select.name = "type";
  select.id = "type";
  select.type = "text";
  select.style.marginBottom = "15px";
  select.style.padding = "10px";
  select.style.border = "1px solid #ccc";
  select.style.borderRadius = "4px";
  form.appendChild(select);
  // Add options to select field
  options = [
    "Bait and Switch",
    "False Urgency",
    "Hidden Costs",
    "Misleading Language",
    "Misleading Visuals",
    "Scarcity",
    "Social Proof",
    "Trick Questions",
    "Urgency",
    "Basket Sneaking",
    "Confirm Shaming",
    "Disguised Ads",
    "Forced Continuity",
    "Friend Spam",
    "Hidden Subscription",
    "Misdirection",
    "Price Comparison Prevention",
    "Privacy Zuckering",
    "Roach Motel",
    "Drip Pricing",
    "Interface Interference",
  ];
  options.forEach(function (option) {
    var opt = document.createElement("option");
    opt.value = option;
    opt.textContent = option;
    select.appendChild(opt);
  });
  // Add a submit button
  var submit = document.createElement("button");
  submit.textContent = "Submit";
  submit.style.color = "white";
  submit.style.padding = "10px 20px";
  submit.style.border = "none";
  submit.style.borderRadius = "4px";
  submit.style.cursor = "pointer";
  submit.style.backgroundColor = "#007bff";
  modalContent.appendChild(form);
  modalContent.appendChild(submit);
  modal.appendChild(modalContent);
  document.body.appendChild(modal);
  submit.addEventListener("click", function () {
    var pattern = input.value;
    var type = select.value;
    // Send the report to the server
    fetch("http://127.0.0.1:8000/report", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        websiteURL: window.location.href,
        patternType: type,
        status: "pending",
        pattern: pattern,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
      })
      .catch((err) => {
        console.error(err);
      });
    // Close the modal
    modal.style.display = "none";
    modal.parentElement.removeChild(modal);
  });
};
