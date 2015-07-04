$(document).on("click", ".edit-button", function () {
        console.log("in function");
        var editPostRequest;

        var id = $(this).attr("data-id");
        var content = $("#edit" + id).val();
        console.log(id);
        console.log(content);

        // Setup request
        if (window.XMLHttpRequest) {
            editPostRequest = new XMLHttpRequest();
        } else {
            editPostRequest = new ActiveXObject("Microsoft.XMLHTTP");
        }

        editPostRequest.onreadystatechange = function () {

            if (editPostRequest.readyState == 4 && editPostRequest.status == 200) {
                var response = editPostRequest.responseText;
                alert(response);
                console.log(response);
                getLatestPosts();
            }
        }

        var url = $("#edit-post-url").data()["url"];

        editPostRequest.open("POST", url, true);
        editPostRequest.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        editPostRequest.send("id=" + id + "&content=    " + content);
});
