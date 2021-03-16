function publicViewCB(checkboxObj) {
    var checkBox = document.getElementById(checkboxObj+"CB");
    $.ajax({
        url: "./update_settings",
        data : { 'setting': checkboxObj, 'value': checkBox.checked },
        success : function(json) {
        }
    })
}

function font_type(font) {
    $.ajax({
        url: "./update_settings",
        data : { 'setting': 'font_family', 'value': font },
        success : function(json) {
        }
    })
}