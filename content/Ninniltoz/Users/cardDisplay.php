<!DOCTYPE html>
<?php 
    include_once "../PHP/run.php";
    include_once "../PHP/displayCard.php";
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
            <div class="userCard index colorText">
                <div id="cardGrid" class="userCardGrid">
                </div>
                <div id="cardPageSelector">
                </div>
            </div>
        </div>
        <script>
            loadHTML("none", "none"); 
            clearCards(1);
        </script>
    </body>
</html>