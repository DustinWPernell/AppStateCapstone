<?php

session_start();

session_unset();

session_destroy();

header("Location: ../");
?>
<html>
<head>
  <meta http-equiv="refresh" content="5; URL='../'" />
</head>
<body>
  <p>If you are not redirected in five seconds, <a href="../">click here</a>.</p>
</body>
</html>