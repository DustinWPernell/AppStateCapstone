<?php
	session_start();
    require 'database.php';
	if( isset($_SESSION['user_id']) ){
		header("Location: /Users/userLand.php");
	}
	if(!empty($_POST['email']) && !empty($_POST['pass'])){
		$records = $userConn->prepare('SELECT ID, Email, Password, AcctType FROM Users WHERE Email = :email');
		$records->bindParam(':email', $_POST['email']);
		$records->execute();
		$results = $records->fetch(PDO::FETCH_ASSOC);
		$message = '';
    
		if(count($results) > 0 && $_POST['pass'] == $results['Password'] ){
			$_SESSION['user_id'] = $results['ID'];
			$_SESSION['Access'] = $results['AcctType'];
			header("Location: /Users/userLand.php");
		} else {
			$message = 'Sorry, those credentials do not match';
            echo "Sorry, those credentials do not match";
		}
	}

?>