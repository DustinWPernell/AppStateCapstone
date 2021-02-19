function runImport(type){
    showLoad();
    RetrieveAPI(type);
}

function showLoad(){
    document.getElementById("APILoader").classList.toggle("loaderShow");
    document.getElementById("APIButtons").classList.toggle("loaderShow");
}

function printToList(print){
    let topOL = document.getElementById("APIProgress");
        var ele = document.createElement("li");
            ele.innerHTML = print;
        topOL.appendChild(ele);
}

function RetrieveAPI(type){
    printToList("Calling API");
    var request_data = "API";
    $.ajax({
        url: "../Collection/retrieveAPI",
        data : {request: request_data},
        success : function(json) {
            printToList("Finished calling API");
            if(type == "card"){
                CardImport();
            } else if(type == "rule"){
                RuleImport();
            } else if(type == "symbol"){
                SymbolImport();
            }
        }
    })
}

function CardImport(){
    printToList("Running card import");
    var request_data = "Cards";
    $.ajax({
        url: "../Collection/cardUpdate",
        data : {request: request_data},
        success : function(json) {
            printToList("Finished card import");
            showLoad();
        }
    })
}

function RuleImport(){
    printToList("Running rule import");
    var request_data = "Rules";
    $.ajax({
        url: "../Collection/ruleUpdate",
        data : {request: request_data},
        success : function(json) {
            printToList("Finished rule import");
            showLoad();
        }
    })
}

function SymbolImport(){
    printToList("Running symbol import");
    var request_data = "Symbols";
    $.ajax({
        url: "../Collection/symbolUpdate",
        data : {request: request_data},
        success : function(json) {
            printToList("Finished symbol import");
            showLoad();
        }
    })
}