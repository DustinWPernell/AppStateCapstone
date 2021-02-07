<?php
    session_start();

    $obj = $_GET["x"];
    switch($obj){
        case "ChkSes": checkSession(); break;
        default: break;
    }
    
    function checkSession(){
        echo $_SESSION['Access'];
    }

    function loadFile($filePath){
        echo file_get_contents("http://dustinp4.sg-host.com/" . $filePath);
    }
?>