function confirmRequest(id, result) {
    // Create a new variable to hold request
    var confirmRequest;

    // Check if XMLHttpRequest exists (modern browsers - IE7+, Firefox, Chrome, Opera, Safari)
    if (window.XMLHttpRequest) {
        // if it does create a XMLHttpRequest
        confirmRequest = new XMLHttpRequest();
    }
    else {
        // otherwise deal with IE6, IE5
        confirmRequest = new ActiveXObject("Microsoft.XMLHTTP");
    }

    // Call back function for request
    confirmRequest.onreadystatechange = function () {

        console.log(confirmRequest.status);

        // Check if request was sent successfully.
        if (confirmRequest.readyState == 4 && confirmRequest.status == 200) {

            // Get response body
            var response = confirmRequest.responseText;
            alert(response);
            getFriendRequests();
        }
    };

    // Setup url
    var url = $("#confirm-friend-request").data()["url"];
    console.log(url);

    // Send a post request
    confirmRequest.open("POST", url, true);
    confirmRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    confirmRequest.send("id=" + id +"&result=" + result);
}

function getFriendRequests() {
    // Create a new variable to hold request
    var getFriendRequests;

    // Check if XMLHttpRequest exists (modern browsers - IE7+, Firefox, Chrome, Opera, Safari)
    if (window.XMLHttpRequest) {
        // if it does create a XMLHttpRequest
        getFriendRequests = new XMLHttpRequest();
    }
    else {
        // otherwise deal with IE6, IE5
        getFriendRequests = new ActiveXObject("Microsoft.XMLHTTP");
    }

    // Call back function for request
    getFriendRequests.onreadystatechange = function () {

        console.log(getFriendRequests.status);

        // Check if request was sent successfully.
        if (getFriendRequests.readyState == 4 && getFriendRequests.status == 200) {

            // Get response body
            var response = getFriendRequests.responseText;
            var json = JSON.parse(response);
            var html = "";

            if (json.length == 0) {
                html = "<li>You have no open friend requests.</li>";
            }

            for (var i=0; i < json.length; i++) {
                html += '<li>' + json[i][0] + ' - <button id="' + json[i][1] + '" class="confirm-request-button">CONFIRM</button><button id="' + json[i][1] + '" class="decline-request-button">DECLINE</button></li>';
            }

            $("#friend-requests").html(html);
        }
    };

    var url = $("#get-friend-requests").data()["url"];
    console.log(url);
    // Send a post request
    getFriendRequests.open("POST", url, true);
    getFriendRequests.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    getFriendRequests.send("");

}

$("#friend-requests").on("click", ".confirm-request-button", function() {
    var id = $(this).attr("id");
    console.log(id);
    confirmRequest(id, "True");
});

$("#friend-requests").on("click", ".decline-request-button", function() {
    var id = $(this).attr("id");

    confirmRequest(id, "False");
});


