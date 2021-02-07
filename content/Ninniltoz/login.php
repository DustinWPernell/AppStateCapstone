<!DOCTYPE html>
<?php 
    include_once "PHP/run.php";
    include_once "PHP/runLogin.php";
?>
<html>
    <head>
        <?php 
            loadFile("/General/css.html");
            loadFile("/General/js.html");
        ?>    
    </head>
    <body class="font">
        <div class="innerBody">
            <?php 
                loadFile("/General/topNav.php");
            ?>
            <div class="main index colorText">
                <form class="modal-content modalAnimate" action="/PHP/runLogin.php" method="post">
                    <div class="modalContainer">
                        <label for="email" class="modalLabel"><b>Email</b></label>
                        <input class="modalInput" type="text" placeholder="Enter Email" name="email" required>
                        <br>
                        <label for="pass" class="modalLabel"><b>Password</b></label>
                        <input class="modalInput" type="password" placeholder="Enter Password" name="pass" required>

                        <button class="modalButton" type="submit">Login</button>
                    </div>
                </form>
            </div>
        </div>
        <script>loadHTML("none", "tnLogin");</script>
    </body>
</html>