import urllib, json

playerNames = ["Boban Marjanovic", "Boris Diaw", "Danny Green", "David West", "Jonathon Simmons", "Kawhi Leonard", "Kyle Anderson",
	"LaMarcus Aldridge", "Manu Ginobili", "Matt Bonner", "Patty Mills", "Rasual Butler", "Ray McCallum", "Tim Duncan", "Tony Parker"]

playerIDs = ["1626246", "2564", "201980", "2561", "203613", "202695", "203937", 
	"200746", "1938", "2588", "201988", "2446", "203492", "1495", "2225"]

roosterSize = len(playerNames)

# Table Headers
print '------'
print '**Team Stats**\n'
print '------\n'
print '| | | | | | |'
print ':--:|:--:|:--:|:--:|:--:|:--:|:--:'
print 'Player | PTS | REB | AST | STL | BLK'

for i in range(0,roosterSize):
	# Get data from stats.nba.com in json format
	url = "http://stats.nba.com/stats/playerprofilev2?playerID=" + playerIDs[i] + "&PerMode=PerGame"
	response = urllib.urlopen(url)
	data = json.loads(response.read())

	# Get headers and career stats by regular seasons
	headersList = data["resultSets"][0]["headers"]
	seasonStatsList = data["resultSets"][0]["rowSet"]

	# Number of different stats (PTS, REB, AST, etc...)
	headersCount = len(headersList)
	# Number of seasons for this player
	seasonsCount = len(seasonStatsList)

	for j in range(0,headersCount):
		if j == 20:
			REB = seasonStatsList[seasonsCount - 1][j]
		elif j == 21:
			AST = seasonStatsList[seasonsCount - 1][j]
		elif j == 22:
			STL = seasonStatsList[seasonsCount - 1][j]
		elif j == 23:
			BLK = seasonStatsList[seasonsCount - 1][j]
		elif j == 26:
			PTS = seasonStatsList[seasonsCount - 1][j]
		# End if
	# End for
	print playerNames[i] + ' | ' + str(PTS) + ' | ' + str(REB) + ' | ' + str(AST) + ' | ' + str(STL) + ' | ' + str(BLK)
#End for

# Table footer
print '\n| | | | |'
print ':--:|:--:|:--:|:--:|'















