function setSwitch(set_name, card_image_one, card_image_two){
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

document.addEventListener('input', function (event) {
	if (event.target.tagName.toLowerCase() !== 'textarea') return;
	autoExpand(event.target);
}, false);

var autoExpand = function (field) {

	// Reset field height
	field.style.height = 'inherit';

	// Get the computed styles for the element
	var computed = window.getComputedStyle(field);

	// Calculate the height
	var height = parseInt(computed.getPropertyValue('border-top-width'), 10)
	             + parseInt(computed.getPropertyValue('padding-top'), 10)
	             + field.scrollHeight
	             + parseInt(computed.getPropertyValue('padding-bottom'), 10)
	             + parseInt(computed.getPropertyValue('border-bottom-width'), 10);

	field.style.height = height + 'px';

};

