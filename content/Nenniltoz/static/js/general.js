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
