<?php
    $cardPerPage = 50;

    if(isset($_GET['action'])){
        if(function_exists($_GET['action'])) {
            if(isset($_GET['p1'])){
                $_GET['action']($_GET['p1']);
            }else{
                $_GET['action']();
            }
        }
    }

    function getNextCardSet($pageNum){
        global $cardPerPage;
        require 'database.php';
        $orderLow = $pageNum * $cardPerPage;

        $sql = "SELECT * FROM Card ORDER By Name limit $orderLow, $cardPerPage";
        $records = $cardConn->prepare($sql, array(PDO::ATTR_CURSOR => PDO::CURSOR_SCROLL));
        $records->execute();
        $returnVal = "";
        while($row = $records->fetch(PDO::FETCH_ASSOC, PDO::FETCH_ORI_NEXT)){
            $image = $row['ImageURL'];
            if($image == "")
            {
                $image = "/Images/blankCard.png";
            }
            $returnVal = $returnVal."<div id=\"".$row['ID']."\" class=\"cardObj\"><img class=\"cardImg\" src=\"".$image."\" alt=\"Avatar\"><div class=\"cardObjText\">".$row['Name']."</div></div>";
        }
        echo $returnVal;
    }
    
    function getPages($pageNum){
        global $cardPerPage;

        $cardCount = getNumCards();
        $pageCount = floor($cardCount / $cardPerPage);

        $lowPage = $pageNum-3;
        $highPage = $pageNum+6;
        if($lowPage <= 0){
            $lowPage = 1;
            $highPage = 10;
        }else if($highPage >= $pageCount){
            $lowPage = $pageCount - 10;
            $highPage = $pageCount;
        }

        $returnVal = "<div class=\"cardPagination\"><a class=\"cardPageItem\" onclick=\"clearCards(1)\">&laquo;</a>";
        for ($curPage = $lowPage; $curPage <= $highPage; $curPage++) {
            if($pageNum == $curPage){
                $returnVal = $returnVal."<a class=\"cardPageItem cardPageActive\" id=\"cardDisplayPage-".$curPage."\" onclick=\"clearCards(".$curPage.")\">".$curPage."</a>";
            } else{
                $returnVal = $returnVal."<a class=\"cardPageItem\" id=\"cardDisplayPage-".$curPage."\" onclick=\"clearCards(".$curPage.")\">".$curPage."</a>";
            }
            
        } 
        $returnVal = $returnVal."<a class=\"cardPageItem\" onclick=\"clearCards(".$pageCount.")\">&raquo;</a></div>";

        echo $returnVal;
    }

    function getNumCards(){
        require 'database.php';
        
        $records = $cardConn->prepare('SELECT COUNT(ID) AS NumCards FROM Card');
		    $records->execute();
        $result = $records->fetch(PDO::FETCH_ASSOC);

        return $result['NumCards'];
    }
?>