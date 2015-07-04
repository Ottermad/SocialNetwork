function sendFriendRequest () {

    var username = $(".friend-request-button").attr("data-ref");
    console.log(username);
    var friendRequest;

    if (XMLHttpRequest) {
        friendRequest = new XMLHttpRequest();
    } else {
        friendRequest = new ActiveXObject("Microsoft.XMLHTTP");
    }

    friendRequest.onreadystatechange = function () {
        if (friendRequest.readyState == 4 && friendRequest.status == 200) {
            // Response
            var response = friendRequest.responseText;
            alert(response);
            $("#name").html(username + "<tag class='pending'>Request Pending...</tag>");
        }
    }

    var url = $("#send-friend-request").data()["url"];

    friendRequest.open("POST", url, true);
    friendRequest.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    friendRequest.send("username=" + username);
}