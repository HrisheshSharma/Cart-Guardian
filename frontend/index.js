// Retrieve the switch state from storage
chrome.storage.local.get("switchState", function (result) {
    var switchState = result.switchState || {};

    // Set the initial state of switches
    var switches = document.querySelectorAll('input[type="checkbox"]');
    switches.forEach(function (sw) {
        var switchId = sw.id;
        var switchStatus = switchState[switchId] ? "ON" : "OFF";
        sw.checked = switchState[switchId] || false;
        // console.log("Switch " + switchId + " is " + switchStatus);
    });

    // Update the switch state in storage when it changes
    switches.forEach(function (sw) {
        sw.addEventListener("change", function () {
            var switchId = sw.id;
            var switchStatus = sw.checked ? "ON" : "OFF";
            // console.log("Switch " + switchId + " is " + switchStatus);

            // Update the switch state in storage
            switchState[switchId] = sw.checked;
            chrome.storage.local.set({ switchState: switchState });

            // sending switch status to background.js
            chrome.runtime.sendMessage({
                message: 'from_index',
                payload: {
                    "switch_response": sw.checked,
                    "switch_id": switchId
                }
            });
        });
    });

    var reportButton = document.getElementById('report');
    console.log(reportButton);
    reportButton.addEventListener("click", function () {
        chrome.runtime.sendMessage({
            message: 'from_index',
            payload: {
                "button_id": 'report'
            }
        });
    });
});
// chrome.webNavigation.onCompleted.addListener(function (details) {
//     if (details.frameId === 0) {
//         var switches = document.querySelectorAll('input[type="checkbox"]');
//         switches.forEach(function (sw) {
//             var switchId = sw.id;
//             var switchStatus = sw.checked ? "ON" : "OFF";
//             if (switchStatus === "ON") {
//                 chrome.runtime.sendMessage({
//                     message: 'from_index',
//                     payload: {
//                         "switch_response": sw.checked,
//                         "switch_id": switchId
//                     }
//                 });
//             }
//         });
//     }
// });