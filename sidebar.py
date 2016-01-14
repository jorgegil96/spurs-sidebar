import json
import urllib.request as ur
import urllib.parse as par
from datetime import date, timedelta

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

teamSubs = {}
teamSubs['1610612742'] = 'mavericks'
teamSubs['1610612743'] = 'denvernuggets'
teamSubs['1610612744'] = 'warriors'
teamSubs['1610612745'] = 'rockets'
teamSubs['1610612746'] = 'laclippers'
teamSubs['1610612747'] = 'lakers'
teamSubs['1610612763'] = 'memphisgrizzlies'
teamSubs['1610612750'] = 'timberwolves'
teamSubs['1610612740'] = 'nolapelicans'
teamSubs['1610612760'] = 'thunder'
teamSubs['1610612756'] = 'suns'
teamSubs['1610612757'] = 'ripcity'
teamSubs['1610612758'] = 'kings'
teamSubs['1610612759'] = 'nbaspurs'
teamSubs['1610612762'] = 'utahjazz'
teamSubs['1610612737'] = 'atlantahawks'
teamSubs['1610612738'] = 'bostonceltics'
teamSubs['1610612751'] = 'gonets'
teamSubs['1610612766'] = 'charlottehornets'
teamSubs['1610612741'] = 'chicagobulls'
teamSubs['1610612739'] = 'clevelandcavs'
teamSubs['1610612765'] = 'detroitpistons'
teamSubs['1610612754'] = 'pacers'
teamSubs['1610612748'] = 'heat'
teamSubs['1610612749'] = 'mkebucks'
teamSubs['1610612752'] = 'nyknicks'
teamSubs['1610612753'] = 'orlandomagic'
teamSubs['1610612755'] = 'sixers'
teamSubs['1610612761'] = 'torontoraptors'
teamSubs['1610612764'] = 'whashingtonwizards'

# TODO: AUTOMATE SCHEDULE
#url = http://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&gameDate=1%2F12%2F2016
#------SCHEDULE-------
def formatDate(date):
    return str(date.month) + '%2F' + str(date.day) + '%2F' + str(date.year)
    
print ('| | | | | | |')
print (':--:|:--:|:--:|:--:|:--:|:--:|:--:')
today = date.today()

scheduleList = [None] * 6
dateList = [None] * 6
homeList = [None] * 6
awayList = [None] * 6
WLTimeList = [None] * 6
scoreTV = [None] * 6

pastGames = 0
cont = 1
while pastGames < 2:
    newDate = today - timedelta(days=cont)
    date = formatDate(newDate)
    url = "http://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&gameDate=" + date
    response = ur.urlopen(url).read()
    data = json.loads(response.decode('utf-8'))
    rowSet = data["resultSets"][0]["rowSet"]
    for i in range(0, len(rowSet)):
        if (rowSet[i][6] == spursID or rowSet[i][7] == spursID):
            if pastGames == 0:
                dateList[1] = str(newDate.month) + '/' + str(newDate.day)
                homeList[1] = teamSubs[str(rowSet[i][6])]
                awayList[1] = teamSubs[str(rowSet[i][7])]
                scheduleList[1] = rowSet[i][5]
                scoreSet = data["resultSets"][1]["rowSet"]
                if (scoreSet[i * 2][21] > scoreSet[i * 2 + 1][21]):
                    WLTimeList[1] = 'W'
                else:
                    WLTimeList[1] = 'L'
                scoreTV[1] = str(scoreSet[i * 2][21]) + '-' + str(scoreSet[i * 2 + 1][21])
            elif pastGames == 1:
                dateList[0] = str(newDate.month) + '/' + str(newDate.day)
                homeList[0] = teamSubs[str(rowSet[i][6])]
                awayList[0] = teamSubs[str(rowSet[i][7])]
                scheduleList[0] = rowSet[i][5]
                scoreSet = data["resultSets"][1]["rowSet"]
                if (scoreSet[i * 2][21] > scoreSet[i * 2 + 1][21]):
                    WLTimeList[0] = 'W'
                else:
                    WLTimeList[0] = 'L'
                scoreTV[0] = str(scoreSet[i * 2][21]) + '-' + str(scoreSet[i * 2 + 1][21])
            # End if
            pastGames += 1
        # End if
    #End for
    cont += 1
#End while

futureGames = 0
cont = 0
while futureGames < 4:
    newDate = today + timedelta(days=cont)
    date = formatDate(newDate)
    url = "http://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&gameDate=" + date
    response = ur.urlopen(url).read()
    data = json.loads(response.decode('utf-8'))
    rowSet = data["resultSets"][0]["rowSet"]
    for i in range(0, len(rowSet)):
        if (rowSet[i][6] == spursID or rowSet[i][7] == spursID):
            dateList[2 + futureGames] = str(newDate.month) + '/' + str(newDate.day)
            homeList[2 + futureGames] = teamSubs[str(rowSet[i][6])]
            awayList[2 + futureGames] = teamSubs[str(rowSet[i][7])]
            WLTimeList[2 + futureGames] = '?'
            if rowSet[i][11] == None:
                scoreTV[2 + futureGames] = 'FSSW'
            else:
                scoreTV[2 + futureGames] = str(rowSet[i][11])
            scheduleList[2 + futureGames] = rowSet[i][5]
            futureGames += 1
        # End if
    # End for
    cont += 1
# End while

# Previous Games
print (dateList[0] + ' | [](/r/' + awayList[0] + ') | @ | [](/r/' + homeList[0] + ') | ' + WLTimeList[0] + ' | ' + scoreTV[0])
print (dateList[1] + ' | [](/r/' + awayList[1] + ') | @ | [](/r/' + homeList[1] + ') | ' + WLTimeList[1] + ' | ' + scoreTV[1])

# Future Games
for i in range(2, 6):
    print (dateList[i] + ' | [](/r/' + awayList[i] + ') | @ | [](/r/' + homeList[i] + ') | ' + WLTimeList[i] + ' | ' + scoreTV[i])

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










