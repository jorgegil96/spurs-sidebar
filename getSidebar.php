<?php
/*
$BobanID = "1626246";
$DiawID = "2564";
$GreenID = "201980";
$WestID = "2561";
$SimmonsID = "203613";
$KawhiID = "202695";
$KyleID = "203937";
$AldridgeID = "200746";
$GinobiliID = "1938"; 
$BonnerID = "2588";
$MillsID = "201988";
$ButlerID = "2446";
$McCallumID = "203492";
$DuncanID = "1495";
$ParkerID = "2225";
*/

$playerNames = array("Boban Marjanovic", "Boris Diaw", "Danny Green", "David West", "Jonathon Simmons", "Kawhi Leonard", "Kyle Anderson",
	"LaMarcus Aldridge", "Manu Ginobili", "Matt Bonner", "Patty Mills", "Rasual Butler", "Ray McCallum", "Tim Duncan", "Tony Parker");

$playerIDs = array("1626246", "2564", "201980", "2561", "203613", "202695", "203937", 
	"200746", "1938", "2588", "201988", "2446", "203492", "1495", "2225");

$rosterSize = count($playerNames);


// Table headers
echo "------<br>

**Team Stats**<br>  
<br>
------<br>
<br>
| | | | | | |<br>
:--:|:--:|:--:|:--:|:--:|:--:|:--:<br>
Player | PTS | REB | AST | STL | BLK<br>";


for ($i = 0; $i < $rosterSize; $i++) {
	// Get data from stats.nba.com in json format
	$playerData = json_decode(file_get_contents("http://stats.nba.com/stats/playerprofilev2?playerID=" . $playerIDs[$i] . "&PerMode=PerGame"));

	// Get headers and career stats by regular seasons
	$headersArray = $playerData->resultSets[0]->headers;
	$seasonStatsArray = $playerData->resultSets[0]->rowSet;

	// Number of different stats
	$headersCount = count($headersArray);
	// Number of seasons for this player
	$seasonsCount = count($seasonStatsArray);

	echo $playerNames[$i] . " ";
	for ($j = 0; $j < $headersCount; $j++) {
		switch ($j) {
			case 26:
				$PTS = $seasonStatsArray[$seasonsCount - 1][$j];
				break;
			case 20:
				$REB = $seasonStatsArray[$seasonsCount - 1][$j];
				break;
			case 21:
				$AST = $seasonStatsArray[$seasonsCount - 1][$j];
				break;
			case 22:
				$STL = $seasonStatsArray[$seasonsCount - 1][$j];
				break;
			case 23:
				$BLK = $seasonStatsArray[$seasonsCount - 1][$j];
				break;
		}
	}
	echo "| " . $PTS . " | " . $REB . " | " . $AST . " | " . $STL . " | " . $BLK . "<br>";
}

// Table footer
echo "<br>| | | | |<br>
:--:|:--:|:--:|:--:|  <br>";

?>