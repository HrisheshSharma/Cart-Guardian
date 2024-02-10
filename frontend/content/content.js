
window.onload = function () {
  let text = document.documentElement.outerHTML;
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

  var docTitle = document.title;

  var addToCartButtons = [];
  var cartWordList = ["to add cart", "add to bag"];
  var cartButtons = getTagList(cartWordList);
  // console.log(cartButtons.length);
  for(var i = 0; i < cartButtons.length; i++){
    if(! cartButtons[i].textContent.toLowerCase().includes("added")){
      addToCartButtons.push(cartButtons[i]);
    }
  }

  for(var i = 0; i < addToCartButtons.length; i++){
    // console.log(addToCartButtons[i].textContent);
    addToCartButtons[i].addEventListener('click', () => {
      var bodyContent = document.body.textContent;
      var dataToPush = longestCommonSubstring(docTitle,bodyContent);
      // console.log(dataToPush);
      chrome.runtime.sendMessage({ action: 'pushData', data: dataToPush });
    });
  }

  var checkoutWordList = ["proceed to pay", "checkout", "pay now", "buy now", "proceed to buy"];
  var checkoutButtons = getTagList(checkoutWordList);


  var lowercaseDocTitle = docTitle.toLowerCase();
  if(lowercaseDocTitle.includes("cart") || lowercaseDocTitle.includes("checkout")){
  
    var extraProducts = [];
    var quantityTags = document.querySelectorAll('select');
    quantityTags.forEach(function(tag){
      var tagContent = tag.textContent;
      var lowercaseTagContent = tagContent.toLowerCase();
      if(lowercaseTagContent.includes('1')){
        var parent = tag;
        for(var i = 0; i < 3; i++) parent = parent.parentNode;
        var parentContent = parent.textContent;
        var lowercaseContent = parentContent.toLowerCase();
        if(lowercaseContent.includes("qty") || lowercaseContent.includes("quantity")){
          var finalTag = tag;
          var finalContent = finalTag.innerHTML;
          // console.log("Quantity found!");
          while(! finalContent.includes("₹") && ! finalContent.includes("Rs") && ! finalContent.includes("INR")){
            finalTag = finalTag.parentNode;
            finalContent = finalTag.innerHTML;
          }
          // console.log("\n\n\n rupee symbol found \n\n\n");

          var finalTextContent = finalTag.textContent;
          var productName = findFirstNonBlankSentence(finalTextContent);
          var websiteName = extractDomain(document.URL);

          // console.log(chrome.storage.local);

          chrome.storage.local.get([websiteName], function(result) {
            var websiteList = result[websiteName] || [];
            var valid = false;
            var n = productName.length;
            productName = productName.replaceAll('…','');
            productName = productName.replaceAll('...','');
            // console.log(productName);
            var zfunc = calculateZFunction(productName);
            productName = productName.slice(0,productName.length - zfunc);
            var breakedIntoWords = productName.split('\s');
            for(var i = 0; i < websiteList.length; i++){
              var flag = true;
              for(var j = 0; j < breakedIntoWords.length; j++){
                if(! websiteList[i].includes(breakedIntoWords[j])){
                  flag = false;
                }
              }
              if(flag){
                valid = true;
              }
            }
            // console.log(productName);
            // console.log(valid);
            if(! valid){
              extraProducts.push(productName);
            }
          });
        }
      }
    });
    for(var i = 0; i < checkoutButtons.length; i++){
      // console.log(checkoutButtons[i].textContent);
      // console.log(extraProducts.length);
      checkoutButtons[i].addEventListener('click', (event) => {
        var result = true;
        if(extraProducts.length > 0){
          var alertmessage = "The website has added following products in your cart\n";
          for(var j = 0; j < extraProducts.length; j++){
            alertmessage += extraProducts[j] + '\n';
          }
          alertmessage += "Are you sure you want to continue?";
          result = confirm(alertmessage);
        }
        if(result){
          chrome.runtime.sendMessage({ action: 'clearData'});
        }
        else{
          event.preventDefault();
        }
      })
    }
  }
};

function contains(inputText, searchStrings){
  var sentences = inputText.split('\n');
  for (var i = 0; i < sentences.length; i++) {
    var currentSentence = sentences[i].trim();
    var found = true;
    for(var j = 0; j < searchStrings.length; j++){
      if(! currentSentence.includes(searchStrings[j])){
        found = false;
      }
    }
    if(found) return true;
  }
  return false;
}

function findFirstNonBlankSentence(inputString) {
  var sentences = inputString.split('\n');

  for (var i = 0; i < sentences.length; i++) {
    var currentSentence = sentences[i].trim();
    if (currentSentence !== "") {
      return currentSentence;
    }
  }
  return null;
}

function getTagList(wordList){
  var tagList = [];
  var prev = [];
  var nxt = [document.querySelector('body')];
  while(nxt.length != 0){
    prev = nxt;
    nxt = [];
    prev.forEach(function (tag) {
      if(tag.textContent.match(/^[\s\n]*[a-zA-Z0-9\s]+[\s\n]*$/)){
        tagList.push(tag);
        return;
      }
      childrenList = tag.children;
      for(var i = 0; i < childrenList.length; i++){
        var child = childrenList[i];
        var loweraseTextContent = child.textContent.toLowerCase();
        for(var j = 0; j < wordList.length; j++){
          if(contains(loweraseTextContent,wordList[j].split(' '))){
            nxt.push(child);
            break;
          }
        }
      }
    });
  }
  return tagList;
}

// Establish a connection with the background script
const port = chrome.runtime.connect({ name: "content-script" });
port.onMessage.addListener((msg) => {
  if (msg.response === "Start Default Disabler") {
    defaultDisable();
  } else if (msg.response === "Start Review") {
    
    // Inject CSS
    var style = document.createElement('style');
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
    var iframe = document.createElement('iframe');
    iframe.style.position = 'fixed';
    iframe.style.height = '100%';
    iframe.style.width = "250px";
    iframe.style.top = '0';
    iframe.style.right = '0';
    iframe.style.zIndex = '1000';
    iframe.style.border = 'none';
    iframe.style.overflow = 'hidden';
    iframe.style.transition = '0.5s';
    iframe.style.backgroundColor = 'white';
    // Create side window div
    var sideWindow = document.createElement('div');
    sideWindow.id = 'mySideWindow';
    sideWindow.className = 'side-window';

    // Add additional content to side window
    sideWindow.innerHTML += `
      <h2>Side Window</h2>
      <p>This is a sample side window.</p>
      `;

    // Append side window to iframe
    iframe.onload = function () {
      iframe.contentDocument.body.appendChild(sideWindow);
    };
    // Append iframe to body
    iframe.style.width = "250px";
    document.body.appendChild(iframe);
  } else if (msg.response === "Close Review") {
    // Close side window
    var iframe = document.querySelector('iframe');
    iframe.style.width = "0";
    iframe.parentElement.removeChild(iframe);
  }
});

function defaultDisable() {
  var inputs = document.querySelectorAll('input, select, textarea');
  inputs.forEach(function (input) {
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

function openSideWindow() {
  document.getElementById("mySideWindow").style.width = "250px";
}

function closeSideWindow() {
  document.getElementById("mySideWindow").style.width = "0";
}

function longestCommonSubstring(str1, str2) {
  const m = str1.length;
  const n = str2.length;

  // Create a 2D array to store the lengths of common suffixes
  const dp = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));

  // Variable to store the length of the longest common substring
  let maxLength = 0;

  // Variable to store the ending index of the longest common substring in str1
  let endIndex = 0;

  for (let i = 1; i <= m; i++) {
      for (let j = 1; j <= n; j++) {
          if (str1[i - 1] === str2[j - 1]) {
              dp[i][j] = dp[i - 1][j - 1] + 1;

              if (dp[i][j] > maxLength) {
                  maxLength = dp[i][j];
                  endIndex = i - 1;
              }
          } else {
              dp[i][j] = 0;
          }
      }
  }

  // Extract the longest common substring
  const longestCommonSubstr = str1.substring(endIndex - maxLength + 1, endIndex + 1);

  return longestCommonSubstr;
}

function extractDomain(url) {
  var domain;
  try {
    domain = new URL(url).hostname;
  } catch (error) {
    console.error('Error extracting domain:', error);
  }
  return domain;
}

function calculateZFunction(s) {
  const n = s.length;
  let z = Array(n);
  z[0] = 0;
  let cur = 0;

  for (let i = 1; i < n; i++) {
    while(cur > 0 && s[i] != s[cur]){
      cur = z[cur - 1];
    }
    if(s[i] == s[cur]) cur++;
    z[i] = cur;
  }

  return z[n-1];
}