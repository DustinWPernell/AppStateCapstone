<?php 
    include_once "../PHP/run.php";
?>
                <div class="topNav colorNavBackground">
                <a id="tnHome" class="topNavItem colorText TNactive" href="/index.php">Home</a>
                <a id="tnAbout" class="topNavItem colorText" href="#about">About</a>
                <div class="navDropdown colorNavBackground colorText">
                        <button onclick="navDropFunc()" class="navDropBtn colorNavBackground colorText">=</button>
                        <div id="userNavDrop" class="navDropDownContent colorNavBackground colorText">
                        </div>
                </div>
                <?php 
                        loadFile("/General/login.html");
                ?>
                </div>