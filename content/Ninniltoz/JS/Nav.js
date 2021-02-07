function navDropFunc() {
    document.getElementById("userNavDrop").classList.toggle("navDropShow");
}

function adminNav(){
    let navMenu = document.getElementById("userNavDrop");
    
    //Admin Land
    navMenu.appendChild(createEle("a", "tnAdmin", "topDropNavHeadItem colorText", "/Admin/adminLand.php", "width:auto;", "Administrator",""));
    //Card Update
    navMenu.appendChild(createEle("a", "tnCUpdate", "topDropNavItem colorText", "/Admin/cardUpdate.php", "width:auto;", "Card Update",""));
}

function userNav(){
    let navMenu = document.getElementById("userNavDrop");
    //User Land
    navMenu.appendChild(createEle("a", "tnUser", "topDropNavHeadItem colorText", "/Users/userLand.php", "width:auto;", "User",""));
    //User Full Card
    navMenu.appendChild(createEle("a", "tnCard", "topDropNavItem colorText", "/Users/cardDisplay.php", "width:auto;", "Card List",""));

}

function generalNav(){
    let navMenu = document.getElementById("userNavDrop");
    //Login
    navMenu.appendChild(createEle("a", "tnLogin", "topDropNavHeadItem colorText", "/login.php", "width:auto;", "Login", ""));

    //Logout
    navMenu.appendChild(createEle("a", "tnLogout", "topDropNavHeadItem colorText", "/PHP/logout.php", "width:auto;", "Logout",""));
}

function createEle(eleType, eleId, eleClass, eleHref, eleStyle, eleInner, eleOnClick){
    let ele = document.createElement(eleType);
    ele.setAttribute("id", eleId);
    ele.setAttribute("class", eleClass);
    ele.setAttribute("href", eleHref);
    ele.setAttribute("style", eleStyle);
    ele.setAttribute("onclick", eleOnClick);
    ele.innerHTML = eleInner;
    return ele;
}