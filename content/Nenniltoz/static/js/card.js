function setSwitch(set_name, set_image, card_image_one, card_image_two, set_list){
//'set_name': card_set.name,'set_image': card_set.imageURL, 'card_image_one': face_obj[0].imageURL, 'card_image_two': ''
//    for (set_val in set_list){
//        document.getElementById("setImage-"+set_val.set_name).classList = ["singSetObj","clickable"];
//    }

    //document.getElementById("setImage-"+set_name).classList.toggle("singSetObjActive");
    //document.getElementById("setImage-"+set_name).classList.toggle("clickable");

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