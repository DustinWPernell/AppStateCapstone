function printToList(print){
    let topOL = document.getElementById("updateTasks");
        var ele = document.createElement("li");
            ele.innerHTML = print;
        topOL.appendChild(ele);
}

function RunCardUpdate(){
    ClearTables();
}

function ClearTables(){
    printToList("Clearing tables");
    var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                printToList("Finished clearing tables");
                RetreiveAPI();
            }
        };
    xmlhttp.open("GET", "/PHP/cardUpdate.php?action=clearTables", true);
    xmlhttp.send();
}

function RetreiveAPI(){
    printToList("Calling API");
    var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    printToList("Finished calling API");
                    CardImport();
                }
        };
        xmlhttp.open("GET", "/PHP/cardUpdate.php?action=retreiveAPI", true);
        xmlhttp.send();
}

function CardImport(){
    printToList("Running card import");
    var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                printToList("Finished card import");
                RuleImport();
            }
        };
        xmlhttp.open("GET", "/PHP/cardUpdate.php?action=cardImport", true);
        xmlhttp.send();
}

function RuleImport(){
    printToList("Running rule import");
    var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    printToList("Finished rule import");
                    SymbolImport();
                }
        };
        xmlhttp.open("GET", "/PHP/cardUpdate.php?action=rulesImport", true);
        xmlhttp.send();
}

function SymbolImport(){
    printToList("Running symbol import");
    var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    printToList("Finished symbol import");
                }
        };
        xmlhttp.open("GET", "/PHP/cardUpdate.php?action=symbolImport", true);
        xmlhttp.send();
}