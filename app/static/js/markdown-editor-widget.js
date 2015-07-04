var converter = new Markdown.Converter();
var editor = new Markdown.Editor(converter);

//Causes error:  unknownHook postNormalisation
//Markdown.Extra.init(converter); // Implement markdown extra

editor.getConverter();
editor.run();
console.log(converter.makeHtml("**I am bold**"));

userShow = true; //Whether the user wants the box to be shown

jQuery(document).ready(function($) {
    console.log("Jquery ready");

    updatePreviewVisibility(userShow);

    $("#wmd-input").keyup(function(event) {
        $("#wmd-input").css('min-height',$("#wmd-preview").css('height'));
        updatePreviewVisibility(userShow);
    });

    $("#preview-toggle").click(function(event) {
        userShow = !($("#wmd-preview").is(':visible'));
        
        $("#wmd-preview").slideToggle(400);
        if ($(this).hasClass('fa-eye')) {
        	$(this).removeClass('fa-eye');
        	$(this).addClass('fa-eye-slash');
        }
        else if ($(this).hasClass('fa-eye-slash')) {
        	$(this).removeClass('fa-eye-slash');
        	$(this).addClass('fa-eye');
        }
    });
});

function updatePreviewVisibility (userDesire) {
    console.log($("#wmd-preview").text());
    if ($("#wmd-preview").text() == "" || userDesire == false) {
        $("#wmd-preview").hide('fast', function() {
            $('#preview-toggle').removeClass('fa-eye');
            $('#preview-toggle').addClass('fa-eye-slash');
        });
    }
    else if (userDesire){
       $("#wmd-preview").show('fast', function() {
            $('#preview-toggle').removeClass('fa-eye-slash');
            $('#preview-toggle').addClass('fa-eye');
        }); 
    }
}