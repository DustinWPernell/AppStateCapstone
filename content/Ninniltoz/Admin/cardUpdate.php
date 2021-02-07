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
            <div id="loader"></div>
            <div class="cardUpdate index colorText">
                <dl>
                  <dt>Running API data import</dt>
                    <dd>
                      <ul id="updateTasks">
                        
                      </ul>
                    </dd>
                </dl
            </div>
        </div>
        <script>loadHTML("none", "none");</script>
        <script>RunCardUpdate();</script>
    </body>
</html>