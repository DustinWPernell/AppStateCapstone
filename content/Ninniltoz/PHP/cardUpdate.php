<?php
    session_start();
    $_SESSION["BulkSite"] =  "https://api.scryfall.com/bulk-data";
    $_SESSION["SymbolSite"] = "https://api.scryfall.com/symbology";

    if(isset($_GET['action'])){
        if(function_exists($_GET['action'])) {
            if(isset($_GET['p1'])){
                $_GET['action']($_GET['p1']);
            }else{
                $_GET['action']();
            }
        }
    }

    function printToList($print){
        echo "<p>$print</p>";
    }

    function clearTables(){
        clearTable("Card");
        clearTable("Legalities");
        clearTable("Rules");
        clearTable("Symbols");
    }

    function clearTable($table){
        require 'database.php';
        $records = $cardConn->prepare("DELETE FROM `$table`");
		$records->execute();    
    }

    function retreiveAPI(){
        session_start();
		    
        $BulkSite = $_SESSION["BulkSite"];
        if(!file_exists("BulkSite.txt")){
            file_put_contents( "BulkSite.txt",file_get_contents($BulkSite));
        }
        
        $bulkFile = fopen("BulkSite.txt","r"); 
        $line = fgets($bulkFile);
        $bulk = json_decode($line);
        foreach ($bulk->data as $obj)
        {
            $type = $obj->type;
            $uri = $obj->download_uri;

            $_SESSION[$type] = $uri;
        }
        fclose($bulkFile);

        unlink("BulkSite.txt");
    }

    function cardImport(){
        retreiveAPI();
        session_start();
        $cardSite = $_SESSION["default_cards"];
        usleep(100000);
        if(!file_exists("CardFile.txt")){
            file_put_contents( "CardFile.txt", file_get_contents($cardSite));
        }

        $file = fopen("CardFile.txt","r"); 
        $line = fgets($file);
        while(! feof($file))
        {
            $line = $line.trim("\n");
            $line = $line.trim(",");
            $line = json_decode(fgets($file));
            insertCard($line);
        }
        fclose($file);

        unlink("CardFile.txt");
    }

    function insertCard($card){
        require 'database.php';
        $ID = $card->oracle_id;
		$Name = $card->name;
		$ImageURL = $card->image_uris->png;
        $ManaCost = $card->mana_cost;
        $Loyalty = $card->loyalty;
        $Pow = $card->power;
        $Tough = $card->toughness;
        $TypeLine = $card->type_line;
        $ColorID = $card->color_identity;
        $KeyWords = "";
        $KeywordArry = $card->keywords;
        while(!empty($KeywordArry)){
            $KeyWords = $KeyWords.", ".$KeywordArry[0];
            unset($KeywordArry[0]);
        }
        
        //print("&tab; Card Added: Card ID = $ID");

		$records = $cardConn->prepare("INSERT INTO `Card`(`ID`, `Name`, `ImageURL`,
                `ManaCost`, `Loyalty`, `Pow`, `Tough`, `TypeLine`, `ColorID`, `Keywords`) 
                VALUES ('$ID', '$Name', '$ImageURL', `$ManaCost`, `$Loyalty`, `$Pow`, `$Tough`,
                         `$TypeLine`, `$ColorID`, `$KeyWords`)");
		$records->execute();

        addLegals($ID, $card->legalities);
    }

    function addLegals($CardID, $legals){
        require 'database.php';
        $Standard = $legals->standard;
        $Future = $legals->future;
        $Historic = $legals->historic;
        $Gladiator = $legals->gladiator;
        $Pioneer = $legals->pioneer;
        $Modern = $legals->modern;
        $Legacy = $legals->legacy;
        $Pauper = $legals->pauper;
        $Vintage = $legals->vintage;
        $Penny = $legals->penny;
        $commander = $legals->commander;
        $Brawl = $legals->brawl;
        $Duel = $legals->duel;
        $oldschool = $legals->oldschool;
        $Premodern = $legals->premodern;

        //print("&tab;&tab; Legality Added: Card ID = $ID");

        $records = $cardConn->prepare("INSERT INTO `Legalities`(`CardID`, `Standard`, `Future`, `Historic`, 
                `Gladiator`, `Pioneer`, `Modern`, `Legacy`, `Pauper`, `Vintage`, 
                `Penny`, `Commander`, `Brawl`, `Duel`, `Oldschool`, `Premodern`) 
            VALUES (`$CardID`, `$Standard`, `$Future`, `$Historic`, 
                `$Gladiator`, `$Pioneer`, `$Modern`, `4Legacy`, `$Pauper`, `$Vintage`, 
                `$Penny`, `$Commander`, `$Brawl`, `$Duel`, `$Oldschool`, `$Premodern`)");
        $records->execute();
    }

    function rulesImport(){
      session_start();
        $rullingSite = $_SESSION["rulings"];
        usleep(100000);
        if(!file_exists("RuleFile.txt")){
            file_put_contents( "RuleFile.txt",file_get_contents($rullingSite));
        }

        $file = fopen("RuleFile.txt","r");       
        $line = fgets($file);
        while(! feof($file))
        {
            $line = json_decode(fgets($file));
            insertRule($line);
        }
        fclose($file);

        unlink("RuleFile.txt");
    }

    function insertRule($rule){
        require 'database.php';
        $ID = $rule->oracle_id;
		$Published = $rule->published_at;
		$Comment = $rule->comment;
        
        //print("&tab; Rule Added: Card ID = $ID");

		$records = $cardConn->prepare("INSERT INTO `Rules`(`CardID`, `PublishDate`, `Comment`) 
                                        VALUES ('$ID', '$Published', '$Comment')");
		$records->execute();
    }

    function symbolImport(){
      session_start();
		$SymbolSite = $_SESSION["SymbolSite"];
        usleep(100000);
        if(!file_exists("SymbolFile.txt")){
            file_put_contents( "SymbolFile.txt", file_get_contents($SymbolSite));
		}

        $file = fopen("SymbolFile.txt", "r");    
        $line = fgets($file);
        while(! feof($file))
        {
            $line = json_decode(fgets($file));
            insertSymbol($line);
        }
        fclose($file);

        unlink("SymbolFile.txt");
    }

    function insertSymbol($Symbol){
        require 'database.php';
        $Symbol = $Symbol->symbol;
		$Text = $Symbol->english;
		$ImageURL = $Symbol->svg_uri;
        $IsMana = $Symbol->represents_mana;
        $ManaCost = $Symbol->cmc;
        $Color = $Symbol->colors;
        $ColorID = SelectColorID($Color);

        print("&tab; Symbol Added: Symbol = $Symbol");

		$records = $cardConn->prepare("INSERT INTO `Symbols`
                (`Symbol`, `Text`, `ImageURL`, `IsMana`, `ManaCost`, `ColorID`) 
            VALUES 
                ('$Symbol', '$Text', '$ImageURL','$IsMana','$ManaCost', '$ColorID')");
		$records->execute();
    }

    function SelectColorID($Colors){
        $ColorString = GetColorString($Colors);

        require 'database.php';
        
        $records = $cardConn->prepare("SELECT ID FROM Color WHERE Abv = $ColorString");
		    $records->execute();
        $result = $records->fetch(PDO::FETCH_ASSOC);

        return $result["ID"];
    }

    function GetColorString($Colors){
        $ColorString = "";
        
        $colInc = 0;
        foreach ($Colors as &$value) {
            if($value == "B"){
                $ColorString = $ColorString.$value;
                unset($Colors[$colInc]);
                break;
            }
            $colInc = $colInc + 1;
        }
        $colInc = 0;
        foreach ($Colors as &$value) {
            if($value == "U"){
                $ColorString = $ColorString.$value;
                unset($Colors[$colInc]);
                break;
            }
            $colInc = $colInc + 1;
        }
        $colInc = 0;
        foreach ($Colors as &$value) {
            if($value == "G"){
                $ColorString = $ColorString.$value;
                unset($Colors[$colInc]);
                break;
            }
            $colInc = $colInc + 1;
        }
        $colInc = 0;
        foreach ($Colors as &$value) {
            if($value == "R"){
                $ColorString = $ColorString.$value;
                unset($Colors[$colInc]);
                break;
            }
            $colInc = $colInc + 1;
        }
        $colInc = 0;
        foreach ($Colors as &$value) {
            if($value == "W"){
                $ColorString = $ColorString.$value;
                unset($Colors[$colInc]);
                break;
            }
            $colInc = $colInc + 1;
        }
        return $ColorString;
    }
?>