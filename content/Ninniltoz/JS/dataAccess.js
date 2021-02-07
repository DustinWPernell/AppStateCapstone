function login() {
    obj = { "limit":1 };
    dbParam = JSON.stringify(obj);
    xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
        }
    };
    xmlhttp.open("GET", "/php/dataAccess.php?x=" + "login", true);
    xmlhttp.send();
}


function isAdmin(){
    obj = { "limit":10 };
    dbParam = JSON.stringify(obj);
    xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var result = this.responseText;
            if (result && redirect){
                window.location.href = "/index.html";
            } else if(!result) {
                window.location.href = "/login.html";
                return false;
            }
            return true;
        }
    };
    xmlhttp.open("GET", "/php/dataAccess.php?x=" + "isAdmin", true);
    xmlhttp.send();
}