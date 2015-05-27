var converter = new Markdown.Converter();
var editor = new Markdown.Editor(converter);

//Causes error:  unknownHook postNormalisation
//Markdown.Extra.init(converter); // Implement markdown extra

editor.getConverter();
editor.run();
console.log(converter.makeHtml("**I am bold**"));

jQuery(document).ready(function($) {
    console.log("Jquery ready");

    $("#wmd-input").keypress(function(event) {
        $("#wmd-input").css('min-height',$("#wmd-preview").css('height'));
    });

    $("#preview-toggle").click(function(event) {
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