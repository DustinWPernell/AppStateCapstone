<?php
    $server = 'localhost';
    $username = 'uc4k0xbxfmjbw';
    $password = 'MTGdbCap';
    $userDB = 'dbkg7yfif8s2hs';
    $mainDB = 'db0vvmuuddebof';
    $cardDB = 'db1ql6us93pyjw';

    try{
	    $userConn = new PDO("mysql:host=$server;dbname=".$userDB.";", $username, $password);
    } catch(PDOException $e){
	    die( "User Connection failed: " . $e->getMessage());
    }
    try{
	    $cardConn = new PDO("mysql:host=$server;dbname=".$cardDB.";", $username, $password);
    } catch(PDOException $e){
	    die( "Card Connection failed: " . $e->getMessage());
    }
    try{
	    $mainConn = new PDO("mysql:host=$server;dbname=".$mainDB.";", $username, $password);
    } catch(PDOException $e){
	    die( "Main Connection failed: " . $e->getMessage());
    }
?>