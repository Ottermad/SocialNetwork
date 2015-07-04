function createBio() {
    var biography = $("#biography").val();
    var csrfToken = document.getElementById("csrf_token").value;


    var createBioRequest;

    if (window.XMLHttpRequest) {
        createBioRequest = new XMLHttpRequest();
    } else {
        createBioRequest = new ActiveXObject("Microsoft.XMLHTTP");
    }

    createBioRequest.onreadystatechange = function () {
        if (createBioRequest.readyState == 4 & createBioRequest.status == 200) {
            var extra = createBioRequest.responseText;
            alert(extra);

            getBiography();

        }
    }

    var url = $("#create-bio").data()["url"];

    createBioRequest.open("POST", url, true);
    createBioRequest.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    createBioRequest.send("biography=" + biography+ "&csrf_token=" + csrfToken);

}

function getBiography() {
    var getBiographyRequest;

    if (window.XMLHttpRequest) {
        getBiographyRequest = new XMLHttpRequest();
    } else {
        getBiographyRequest = new ActiveXObject("Microsoft.XMLHTTP");
    }

    getBiographyRequest.onreadystatechange = function () {
        if (getBiographyRequest.readyState == 4 & getBiographyRequest.status == 200) {
            var extra = getBiographyRequest.responseText;
            var extra = JSON.parse(extra);
            var bio_md = extra[0];
            var bio_html = extra[1];
            $("#bio-view").html(bio_html);
            $("#biography").val(bio_md);

        }
    }

    var url = $("#get-bio").data()["url"];

    getBiographyRequest.open("POST", url, true);
    getBiographyRequest.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    getBiographyRequest.send();

}