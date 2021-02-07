function clearCards(newPage){
    addNewCards(newPage);

    changePage(newPage);
}

function addNewCards(newPage){
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("cardGrid").innerHTML = this.responseText;
        }
    };
    xmlhttp.open("GET", "/PHP/displayCard.php?action=getNextCardSet&p1=" + newPage, true);
    xmlhttp.send();
}

function changePage(newPage){
    let ele = document.getElementsByClassName("cardPageActive");
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        document.getElementById("cardPageSelector").innerHTML = this.responseText;
    }
    };
    xmlhttp.open("GET", "/PHP/displayCard.php?action=getPages&p1=" + newPage, true);
    xmlhttp.send();
}