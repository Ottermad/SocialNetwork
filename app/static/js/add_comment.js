$("#posts").on("click", ".comment-button", function() {

    var id = $(this).attr("id");
    var comment = $(".input" + id ).val();
    var csrfToken = document.getElementById("csrf_token").value;

    // Create a new variable to hold request
    var commentRequest;

    // Check if XMLHttpRequest exists (modern browsers - IE7+, Firefox, Chrome, Opera, Safari)
    if (window.XMLHttpRequest) {
        // if it does create a XMLHttpRequest
        commentRequest = new XMLHttpRequest();
    }
    else {
        // otherwise deal with IE6, IE5
        commentRequest=new ActiveXObject("Microsoft.XMLHTTP");
    }

    // Call back function for request
    commentRequest.onreadystatechange=function() {

        console.log(commentRequest.status);

        // Check if request was sent successfully.
        if (commentRequest.readyState==4 && commentRequest.status==200) {

            // Get response body
            var response = commentRequest.responseText;
            alert(response);
            getSinglePost(id);
        }
    }

    var url = $("#add-comment-url").data()["url"];

    // Send a post request
    commentRequest.open("POST", url,true);
    commentRequest.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    commentRequest.send("comment=" + comment + "&post_id=" + id + "&csrf_token=" + csrfToken);
});

function getSinglePost(id) {
    // Create a new variable to hold request
    var commentRequest;

    // Check if XMLHttpRequest exists (modern browsers - IE7+, Firefox, Chrome, Opera, Safari)
    if (window.XMLHttpRequest) {
        // if it does create a XMLHttpRequest
        commentRequest = new XMLHttpRequest();
    }
    else {
        // otherwise deal with IE6, IE5
        commentRequest=new ActiveXObject("Microsoft.XMLHTTP");
    }

    // Call back function for request
    commentRequest.onreadystatechange=function() {

        console.log(commentRequest.status);

        // Check if request was sent successfully.
        if (commentRequest.readyState==4 && commentRequest.status==200) {

            // Get response body
            var json = commentRequest.responseText;
            var json = JSON.parse(json);
            var postHTML = "";
            postHTML += '<p class="name dark-gray"> By ' + json[0] + ' at ';
            postHTML += '<span class="timestamp">' + json[1] + '</span> </p>';
            postHTML += '<p class="content">' + json[2] + '</p>';
            postHTML += '<h2 class="comment-header">Comments:</h2>';
            postHTML += '<hr class="comment-section-seperator">';
            postHTML += '<ul class="comment-list">';
            for(var c = 0; c < json[3].length; c++) {
                postHTML += '<li class="comment"><span class="comment-name">' + json[3][c][0] + '</span>: ' + json[3][c][2] + ' <span class="data right">' +  json[3][c][1] + '</span></li>';
                postHTML += '<hr class="comment-seperator">';
            }
            postHTML += ' </ul>';
            postHTML += '</div>';

            postHTML += '<form>';
            postHTML += '<input class="input' + json[4] + ' comment-input" name="comment" type="text">';
            postHTML += '<button type="button" id="' + json[4] + '" class="comment-button"><i class="fa fa-comment"></i> Post comment</button>';
            postHTML += '</form>';
            $("#div" + id).html(postHTML);
        }
    }

    var url = $("#get-post-url").data()["url"];

    // Send a post request
    commentRequest.open("POST", url,true);
    commentRequest.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    commentRequest.send("id=" + id);
}