function setSwitch(set_name, card_image_one, card_image_two){
    document.getElementById("singCardSetName").innerHTML = set_name

    document.getElementById("singCardFirstImg").src = card_image_one
    if (card_image_two != 'NONE'){
        document.getElementById("singCardSecondImg").src = card_image_two
    }
}

function advFilterFunc() {
    document.getElementById("advFilter").classList.toggle("show");
}

function setSearchDisplay() {
    document.getElementById("setSearchCheckBoxes").classList.toggle("show");
}