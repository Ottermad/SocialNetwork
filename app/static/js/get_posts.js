function getPosts() {
        var count = $("#posts .post").length;

        var getPostsRequest;

        if (window.XMLHttpRequest) {
            getPostsRequest = new XMLHttpRequest();
        } else {
            getPostsRequest = new ActiveXObject("Microsoft.XMLHTTP");
        }

        getPostsRequest.onreadystatechange = function () {
            if (getPostsRequest.readyState == 4 & getPostsRequest.status == 200) {
                var extra = getPostsRequest.responseText;
                var extra = JSON.parse(extra);
                var postHTML = formatPost(extra);

                $("#posts").append(postHTML);
                console.log("Updated");

            }
        }

        var url = $("#get-posts-url").data()["url"];

        getPostsRequest.open("POST", url, true);
        getPostsRequest.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        getPostsRequest.send("offset=" + count);

    }

    function getLatestPosts() {
        var getPostsRequest;

        if (window.XMLHttpRequest) {
            getPostsRequest = new XMLHttpRequest();
        } else {
            getPostsRequest = new ActiveXObject("Microsoft.XMLHTTP");
        }

        getPostsRequest.onreadystatechange = function () {
            if (getPostsRequest.readyState == 4 & getPostsRequest.status == 200) {
                var extra = getPostsRequest.responseText;
                var extra = JSON.parse(extra);
                var postHTML = formatPost(extra);

                $("#posts").html(postHTML);
                console.log("Updated!!!!!!!!!!");

            }
        }

        var url = $("#get-posts-url").data()["url"];

        getPostsRequest.open("POST", url, true);
        getPostsRequest.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        getPostsRequest.send("offset=" + 0);

    }

    function formatPost (extra) {
        formattedPost = "";
        for (var i = 0; i < extra.length; i++) {
            formattedPost += '<div class="post theme-box clearfix" id="div' + extra[i][4] +'">';
            formattedPost += '<span class="name dark-gray">' + 'By ' + extra[i][0] + ' at ';
            formattedPost += '<span class="timestamp">' + extra[i][1] + '</span> </span>'; 
            if (extra[i][5]) {
               formattedPost += '<span class="delete-button right"><i class="fa fa-times fa-lg" title="delete"></i></span>';
               formattedPost += '<i class="fa fa-5x"></i><span class="edit-toggle right" data-ref="#edit-container'
               formattedPost += extra[i][4];
               formattedPost += '"><i class="fa fa-edit fa-lg"></i></span>';
            }
            formattedPost += '<p class="content">' + extra[i][2] + '</p>';
            if (extra[i][5]) {
                //Stuff
                formattedPost += '<div id="edit-container';
                formattedPost += extra[i][4];
                formattedPost += '" class="edit-container"><button class="edit-button" data-id="';
                formattedPost += extra[i][4];
                formattedPost += '">Update</button> <br> <textarea id="edit';
                formattedPost += extra[i][4] + '">';
                formattedPost += extra[i][6];
                formattedPost += '</textarea></div>';
            }
            formattedPost += '<div>';
            formattedPost += '<h2 class="comment-header">Comments:</h2>';
            formattedPost += '<hr class="comment-section-seperator">';
            formattedPost += '<ul class="comment-list">';
            for(var c = 0; c < extra[i][3].length; c++) {
                formattedPost += '<li class="comment"><span class="comment-name">' + extra[i][3][c][0] + '</span>: ' + extra[i][3][c][2] + ' <span class="data right">' +  extra[i][3][c][1] + '</span></li>';
                formattedPost += '<hr class="comment-seperator">';
            }
            formattedPost += '</ul>';
            formattedPost += '</div>';

            formattedPost += '<form>';
            formattedPost += '<input class="input' + extra[i][4] + ' comment-input" name="comment" type="text">';
            formattedPost += '<button type="button" id="' + extra[i][4] + '" class="comment-button"><i class="fa fa-comment"></i> Post comment</button>';
            formattedPost += '</form>';
            formattedPost += '</div>';
        }
        return formattedPost;
    }