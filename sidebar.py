import json
import urllib.request as ur
import urllib.parse as par

recordUrl = "http://stats.nba.com/stats/playoffpicture?LeagueID=00&SeasonID=22015"
response = ur.urlopen(recordUrl).read()
recordData = json.loads(response.decode('utf-8'))

#------HEADINGS AND RECORD-------
spursID = 1610612759
westStandings = recordData["resultSets"][3]["rowSet"]
for i in range(0,15):
	if westStandings[i][3] == spursID:
		spursRecord = str(westStandings[i][4]) + '-' + str(westStandings[i][5])

print ('[48 Minutes of Hell](http://www.48minutesofhell.com/) | [Pounding the Rock](http://www.poundingtherock.com/) | [Spurstalk](http://www.spurstalk.com/forums/)')
print ('\n------')
print ('**2015-2016 Spurs Schedule | Record: ' + spursRecord + '**\n')
print ('------\n')


# TODO: AUTOMATE SCHEDULE
#url = http://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&gameDate=1%2F12%2F2016
#------SCHEDULE-------
print ('| | | | | | |')
print (':--:|:--:|:--:|:--:|:--:|:--:|:--:')
print ('1/11 | [](/r/nbaspurs) | @ | [](/r/gonets) | W | 106-79')
print ('1/12 | [](/r/nbaspurs) | @ | [](/r/detroitpistons) | W | 109-99')
print ('1/14 | [](/r/clevelandcavs) | @ | [](/r/nbaspurs) | 7:00 | TNT')
print ('1/17 | [](/r/mavericks) | @ | [](/r/nbaspurs) | 6:00 | FSSW')
print ('1/21 | [](/r/nbaspurs) | @ | [](/r/suns) | 9:30 | TNT')
print ('1/22 | [](/r/nbaspurs) | @ | [](/r/lakers) | 9:30 | FSSW')
print ('\n| | | | |')
print (':--:|:--:|:--:|:--:|')


#------PLAYER STATS------
playerNames = ["Boban Marjanovic", "Boris Diaw", "Danny Green", "David West", "Jonathon Simmons", "Kawhi Leonard", "Kyle Anderson",
	"LaMarcus Aldridge", "Manu Ginobili", "Matt Bonner", "Patty Mills", "Rasual Butler", "Ray McCallum", "Tim Duncan", "Tony Parker"]

playerIDs = ["1626246", "2564", "201980", "2561", "203613", "202695", "203937", 
	"200746", "1938", "2588", "201988", "2446", "203492", "1495", "2225"]

roosterSize = len(playerNames)

# Table Headers
print ('------')
print ('**Team Stats**\n')
print ('------\n')
print ('| | | | | | |')
print (':--:|:--:|:--:|:--:|:--:|:--:|:--:')
print ('Player | PTS | REB | AST | STL | BLK')

for i in range(0,roosterSize):
	# Get data from stats.nba.com in json format
	url = "http://stats.nba.com/stats/playerprofilev2?playerID=" + playerIDs[i] + "&PerMode=PerGame"
	response = ur.urlopen(url).read()
	data = json.loads(response.decode('utf-8'))

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
	print (playerNames[i] + ' | ' + str(PTS) + ' | ' + str(REB) + ' | ' + str(AST) + ' | ' + str(STL) + ' | ' + str(BLK))
#End for

# Table footer
print ('\n| | | | |')
print (':--:|:--:|:--:|:--:|\n')


#------RULES-------
print ('\n**BE NICE.**\n')
print ('Troll posts will be removed and violators may be banned. Lighthearted shittalking is allowed. We will make judgement calls about what qualifies.\n')
print ('**POST SPURS RELATED CONTENT ONLY.**\n')
print ('Reaction GIFs, image macros, or memes will be removed if they do not contain content that is substantially related to the Spurs.\n')
print ('**NO SPAMMING.**\n' )
print ('Original content from your blog about the Spurs (or similar such content) is welcome, but if that\'s the only thing you post, and you do not otherwise participate in the community, your posts may be removed.  Duplicate posts may be removed. Short text "comment" posts may also be removed.\n')

print ('#### [](/skyline)\n')
print ('##### [](/headerlinks)')
print ('* [](http://reddit.com)\n')
print ('###### [](/headerlinks)')
print ('* [](/r/nba)\n')
print ('1. [](http://en.wikipedia.org/wiki/1998%E2%80%9399_San_Antonio_Spurs_season)')
print ('2. [](http://en.wikipedia.org/wiki/2002%E2%80%9303_San_Antonio_Spurs_season)')
print ('3. [](http://en.wikipedia.org/wiki/2004%E2%80%9305_San_Antonio_Spurs_season)')
print ('4. [](http://en.wikipedia.org/wiki/2006%E2%80%9307_San_Antonio_Spurs_season)')
print ('5. [](http://en.wikipedia.org/wiki/2013%E2%80%9314_San_Antonio_Spurs_season)')












