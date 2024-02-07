document.addEventListener("DOMContentLoaded", function () {
    var switches = document.querySelectorAll('input[type="checkbox"]');
    switches.forEach(function (sw) {
        sw.addEventListener("change", function () {
            var switchId = sw.id;
            var switchStatus = sw.checked ? "ON" : "OFF";
            console.log("Switch " + switchId + " is " + switchStatus);
            // sending switch status to background.js
            chrome.runtime.sendMessage({
                message: 'from_index',
                payload: {
                    "switch_response":sw.checked,
                    "switch_id":switchId
                }
            });
        });
    });
});