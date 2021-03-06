function getPeople() {
    // Create a new variable to hold request
    var getPeopleRequest;

    // Check if XMLHttpRequest exists (modern browsers - IE7+, Firefox, Chrome, Opera, Safari)
    if (window.XMLHttpRequest) {
        // if it does create a XMLHttpRequest
        getPeopleRequest = new XMLHttpRequest();
    }
    else {
        // otherwise deal with IE6, IE5
        getPeopleRequest=new ActiveXObject("Microsoft.XMLHTTP");
    }

    // Call back function for request
    getPeopleRequest.onreadystatechange=function() {

        console.log(getPeopleRequest.status);

        // Check if request was sent successfully.
        if (getPeopleRequest.readyState==4 && getPeopleRequest.status==200) {

            // Get response body
            var json = getPeopleRequest.responseText;
            // Parse into JSON
            json = JSON.parse(json);


            var htmlString = "";
            for (i = 0; i < json.length; i++) {
                var string = "<li id='" + json[i] + "' class='friend-item'>" + json[i] +"<button class='bg-red theme-btn-small'>Message</button></li>";
                htmlString += string;
            }
            var peopleList = document.getElementById("people");
            peopleList.innerHTML = htmlString;

            $("#people li").on('click', function() {
                currentPerson = $(this).attr("id");
                $("#name").text(currentPerson);
                $("#recipient").val(currentPerson);
                getConversation(currentPerson);
            });




        }
    }

    var url = $("#people-url").data()["url"];

    // Send a post request
    getPeopleRequest.open("POST",url,true);
    getPeopleRequest.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    getPeopleRequest.send();
}


function getConversation(name) {
    // Create a new variable to hold request
    var getConversasionRequest;

    // Check if XMLHttpRequest exists (modern browsers - IE7+, Firefox, Chrome, Opera, Safari)
    if (window.XMLHttpRequest) {
        // if it does create a XMLHttpRequest
        getConversasionRequest = new XMLHttpRequest();
    }
    else {
        // otherwise deal with IE6, IE5
        getConversasionRequest=new ActiveXObject("Microsoft.XMLHTTP");
    }

    // Call back function for request
    getConversasionRequest.onreadystatechange=function() {

        console.log(getConversasionRequest.status);

        // Check if request was sent successfully.
            if (getConversasionRequest.readyState==4 && getConversasionRequest.status==200) {

                // Get response body
                var json = getConversasionRequest.responseText;
                // Parse into JSON
                json = JSON.parse(json);

                var htmlString = "";
                for (i = 0; i < json.length; i++) {
                    var Class = "msg-received";
                    if (json[i][2]) {
                        Class = "msg-sent";
                    }
                    var string = "<li class='"+ Class + "'>" + json[i][0] + " " + json[i][1] +"</li>";
                    console.log(string);
                    htmlString = htmlString + string;
                }
                var peopleList = document.getElementById("messages");
                peopleList.innerHTML = htmlString;
            }
        }

        var url = $("#get-messages-url").data()["url"];

        // Send a post request
        getConversasionRequest.open("POST",url,true);
        getConversasionRequest.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        getConversasionRequest.send("other=" + name);
    }
