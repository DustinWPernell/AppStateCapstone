<!DOCTYPE html>
<?php 
    include_once "PHP/run.php";
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
                <p>
                    Here There Be Magic <a href="/Admin/adminLand.php">Admin</a>
                </p>
            </div>
        </div>
        <script>loadHTML("none", "tnHome");</script>
    </body>
</html>