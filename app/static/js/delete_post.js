$("#posts").on("click", ".delete-button", function () {
    console.log("in function");
    var deletePostRequest;

    var id = $(this).parent().attr("id").replace("div", "");

    // Setup request
    if (window.XMLHttpRequest) {
        deletePostRequest = new XMLHttpRequest();
    } else {
        deletePostRequest = new ActiveXObject("Microsoft.XMLHTTP");
    }

    deletePostRequest.onreadystatechange = function () {

        if (deletePostRequest.readyState == 4 && deletePostRequest.status == 200) {
            var response = deletePostRequest.responseText;
            alert(response);
            console.log(response);
            getLatestPosts();
        }
    }

    var url = $("#delete-post-url").data()["url"];

    deletePostRequest.open("POST", url, true);
    deletePostRequest.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    deletePostRequest.send("id=" + id);
});

