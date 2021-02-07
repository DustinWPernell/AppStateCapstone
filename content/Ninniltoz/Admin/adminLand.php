<!DOCTYPE html>
<?php 
    include_once "../PHP/run.php";
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
            <div class="main admin colorText">
                <p>
                    There Be Magic <a href="/index.php">Home</a>
                </p>
            </div>
        </div>
        <script>loadHTML("none", "none");</script>
    </body>
</html>