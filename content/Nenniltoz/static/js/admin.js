function runSearche(type){
    showLoad();
    RetrieveSearch(type);
}

function RetrieveSearch(type){
    if(type == "oracles"){
        OraclesSearch();
    }
}

function OraclesSearch(){
    var request_data = "Oracle";
    $.ajax({
        url: "../Management/oracle_search",
        data : {request: request_data},
        success : function(json) {
            printToList("Added Oracle Search To Queue");
            showLoad();
        }
    })
}

function runImport(type){
    showLoad();
    RetrieveAPI(type);
}

function showLoad(){
    document.getElementById("APILoader").classList.toggle("show");
    document.getElementById("APIButtons").classList.toggle("show");
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
        url: "../Management/retrieveAPI",
        data : {request: request_data},
        success : function(json) {
            if(type == "card"){
                CardImport();
            } else if(type == "images"){
                CardImages();
            } else if(type == "oracle"){
                OracleImport();
            } else if(type == "set"){
                SetImport();
            } else if(type == "rule"){
                RuleImport();
            } else if(type == "symbol"){
                SymbolImport();
            }
        }
    })
}

function OracleImport(){
    var request_data = "Oracle";
    $.ajax({
        url: "../Management/oracleUpdate",
        data : {request: request_data},
        success : function(json) {
            printToList("Added Oracle To Queue");
            showLoad();
        }
    })
}


function SetImport(){
    var request_data = "Sets";
    $.ajax({
        url: "../Management/setUpdate",
        data : {request: request_data},
        success : function(json) {
            printToList("Added Set To Queue");
            showLoad();
        }
    })
}

function CardImport(){
    var request_data = "Cards";
    $.ajax({
        url: "../Management/cardUpdate",
        data : {request: request_data},
        success : function(json) {
            printToList("Added Card To Queue");
            CardImages();
        }
    })
}

function CardImages(){
    var request_data = "Cards";
    $.ajax({
        url: "../Management/cardUpdate",
        data : {request: request_data},
        success : function(json) {
            printToList("Added Card Image To Queue");
            showLoad();
        }
    })
}

function RuleImport(){
    var request_data = "Rules";
    $.ajax({
        url: "../Management/ruleUpdate",
        data : {request: request_data},
        success : function(json) {
            printToList("Added Rule To Queue");
            showLoad();
        }
    })
}

function SymbolImport(){
    var request_data = "Symbols";
    $.ajax({
        url: "../Management/symbolUpdate",
        data : {request: request_data},
        success : function(json) {
            printToList("Added Symbol To Queue");
            showLoad();
        }
    })
}