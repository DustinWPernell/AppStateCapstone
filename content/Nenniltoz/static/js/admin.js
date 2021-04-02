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
            printToList("Added API To Queue");
            if(type == "card"){
                CardImport();
            } else if(type == "oracle"){
                OracleImport();
            }else if(type == "set"){
                SetImport();
            }else if(type == "rule"){
                RuleImport();
            } else if(type == "symbol"){
                SymbolImport();
            }
        }
    })
}

function OracleImport(){
    printToList("Running Oracle Import");
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
    printToList("Running set Import");
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
    printToList("Running Card Import");
    var request_data = "Cards";
    $.ajax({
        url: "../Management/cardUpdate",
        data : {request: request_data},
        success : function(json) {
            printToList("Added Card To Queue");
            showLoad();
        }
    })
}

function CardImport(){
    printToList("Running Card Image Import");
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
    printToList("Running Rule Import");
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
    printToList("Running Symbol Import");
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