function loadHTML(sideActive, topActive){
    
    checkSession();

    //updateLinks(sideActive, "sideNavItem colorText", "SNactive"); 
    updateLinks(topActive, "topNavItem colorText", "TNactive");
}

function checkSession(){
    obj = { "limit":1 };
    dbParam = JSON.stringify(obj);
    xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var isAdmin = this.responseText;

            switch(isAdmin){
                case "3":
                    userNav();
                    generalNav();
                    document.getElementById("tnLogin").remove();
                case "2":
                    userNav();
                    generalNav();
                    document.getElementById("tnLogin").remove();
                case "1":
                    userNav();
                    adminNav();
                    generalNav();
                    document.getElementById("tnLogin").remove();
                    break;
                default: 
                    generalNav();
                    document.getElementById("tnLogout").remove();
                break;
            }
        }
    };
    xmlhttp.open("GET", "/PHP/run.php?x=ChkSes", true);
    xmlhttp.send();
}

function updateLinks(active, oldClass ,newClass){
    let curActive = document.getElementsByClassName(newClass);
    var i;
    for (i = 0; i < curActive.length; i++) {
        curActive[i].className = oldClass;
    }
    if(active != "none")
    {
        let newActive = document.getElementById(active);
        newActive.className += " " + newClass;
    }
}
