/*$(document).keypress(
    function(event){
        if (event.which == '13') {
            event.preventDefault();
        }
    }
);*/

window.onclick = function(event) {
    if (!event.target.matches('.navDropBtn')) {
        var dropdowns = document.getElementsByClassName("navDropDownContent");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('navDropShow')) {
                openDropdown.classList.remove('navDropShow');
            }
        }
    }
}

function navDropFunc() {
    document.getElementById("userNavDrop").classList.toggle("navDropShow");
}

function openTab(evt, tabName) {
  var i, tabcontent, tablinks;

  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
}

function numValidate(evt) {
  var theEvent = evt || window.event;

  // Handle paste
  if (theEvent.type === 'paste') {
      key = event.clipboardData.getData('text/plain');
  } else {
  // Handle key press
      var key = theEvent.keyCode || theEvent.which;
      key = String.fromCharCode(key);
  }
  var regex = /[0-9]|\./;
  if( !regex.test(key) ) {
    theEvent.returnValue = false;
    if(theEvent.preventDefault) theEvent.preventDefault();
  }
}

function googleTranslateElementInit() {
  new google.translate.TranslateElement({pageLanguage: 'en'}, 'google_translate_element');
}

function show_page_load(){
    document.getElementById("page_loading").classList.toggle("show");
}