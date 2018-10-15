import json
from datetime import date, timedelta, datetime
from dateutil import tz
import praw
import requests
import config


def getUrlContent2(url):
    headers = {'user-agent': (
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'),
        'Dnt': '1',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en',
        'origin': 'http://stats.nba.com'}
    response = requests.get(url, headers=headers)
    return json.loads(response.text)


def timeStringToCentral(s):
    from_zone = tz.gettz('America/New_York')
    to_zone = tz.gettz('America/Chicago')
    time = datetime.strptime(s[:-3], '%I:%M %p')
    newyork = time.replace(tzinfo=from_zone)
    central = newyork.astimezone(to_zone)
    formatted = datetime.strftime(central, '%I:%M')
    if formatted[0] == '0':
        formatted = formatted[1:]
    return formatted + " CT"


print('Please wait, the script may take a while to run')
recordUrl = "http://stats.nba.com/stats/playoffpicture?LeagueID=00&SeasonID=22018"
recordData = getUrlContent2(recordUrl)
print('Got record')

# ------HEADINGS AND RECORD-------
spursID = 1610612759
westStandings = recordData["resultSets"][3]["rowSet"]
for i in range(0, 15):
    if westStandings[i][3] == spursID:
        spursRecord = str(westStandings[i][4]) + '-' + str(westStandings[i][5])

sidebarText = (
    '[Pounding the Rock](http://www.poundingtherock.com/) | [Spurstalk](http://www.spurstalk.com/forums/) | [Spurs '
    'Discord](https://discord.gg/rcvBDQ6)')
sidebarText += '\n\n------'
sidebarText += ('\n**[2018-2019 Spurs Schedule](http://www.nba.com/spurs/schedule/) | Record: ' + spursRecord + '**\n')
sidebarText += '\n------\n'

teamSubs = {'1610612742': 'mavericks',
            '1610612743': 'denvernuggets',
            '1610612744': 'warriors',
            '1610612745': 'rockets',
            '1610612746': 'laclippers',
            '1610612747': 'lakers',
            '1610612763': 'memphisgrizzlies',
            '1610612750': 'timberwolves',
            '1610612740': 'nolapelicans',
            '1610612760': 'thunder',
            '1610612756': 'suns',
            '1610612757': 'ripcity',
            '1610612758': 'kings',
            '1610612759': 'nbaspurs',
            '1610612762': 'utahjazz',
            '1610612737': 'atlantahawks',
            '1610612738': 'bostonceltics',
            '1610612751': 'gonets',
            '1610612766': 'charlottehornets',
            '1610612741': 'chicagobulls',
            '1610612739': 'clevelandcavs',
            '1610612765': 'detroitpistons',
            '1610612754': 'pacers',
            '1610612748': 'heat',
            '1610612749': 'mkebucks',
            '1610612752': 'nyknicks',
            '1610612753': 'orlandomagic',
            '1610612755': 'sixers',
            '1610612761': 'torontoraptors',
            '1610612764': 'washingtonwizards'}


# ------SCHEDULE-------
def formatDate(date):
    return str(date.month) + '%2F' + str(date.day) + '%2F' + str(date.year)


sidebarText += '\n| | | | | | |'
sidebarText += '\n:--:|:--:|:--:|:--:|:--:|:--:|:--:'
today = date.today()

scheduleList = [None] * 6
dateList = [None] * 6
homeList = [None] * 6
awayList = [None] * 6
WLTimeList = [None] * 6
scoreTV = [None] * 6

limit = 10  # Stop looking for games after 10 days.
pastGames = 0
cont = 1
while pastGames < 2 and cont < limit:
    newDate = today - timedelta(days=cont)
    date = formatDate(newDate)
    url = "http://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&gameDate=" + date
    data = getUrlContent2(url)

    rowSet = data["resultSets"][0]["rowSet"]
    for i in range(0, len(rowSet)):
        if rowSet[i][6] == spursID or rowSet[i][7] == spursID:
            if pastGames == 0:
                dateList[1] = str(newDate.month) + '/' + str(newDate.day)
                homeList[1] = teamSubs[str(rowSet[i][6])]
                awayList[1] = teamSubs[str(rowSet[i][7])]
                scheduleList[1] = rowSet[i][5]
                scoreSet = data["resultSets"][1]["rowSet"]
                if scoreSet[i * 2][22] > scoreSet[i * 2 + 1][22]:
                    if rowSet[i][7] == spursID:
                        WLTimeList[1] = 'W'
                    else:
                        WLTimeList[1] = 'L'
                else:
                    if rowSet[i][6] == spursID:
                        WLTimeList[1] = 'W'
                    else:
                        WLTimeList[1] = 'L'
                scoreTV[1] = str(scoreSet[i * 2][22]) + '-' + str(scoreSet[i * 2 + 1][22])
            elif pastGames == 1:
                dateList[0] = str(newDate.month) + '/' + str(newDate.day)
                homeList[0] = teamSubs[str(rowSet[i][6])]
                awayList[0] = teamSubs[str(rowSet[i][7])]
                scheduleList[0] = rowSet[i][5]
                scoreSet = data["resultSets"][1]["rowSet"]
                if scoreSet[i * 2][22] > scoreSet[i * 2 + 1][22]:
                    if rowSet[i][7] == spursID:
                        WLTimeList[0] = 'W'
                    else:
                        WLTimeList[0] = 'L'
                else:
                    if rowSet[i][6] == spursID:
                        WLTimeList[0] = 'W'
                    else:
                        WLTimeList[0] = 'L'
                scoreTV[0] = str(scoreSet[i * 2][22]) + '-' + str(scoreSet[i * 2 + 1][22])
            # End if
            pastGames += 1
            # End if
    # End for
    cont += 1
# End while

print('Got past games')

futureGames = 0
cont = 0
while futureGames < 4 and cont < limit:
    newDate = today + timedelta(days=cont)
    date = formatDate(newDate)
    url = "http://stats.nba.com/stats/scoreboardV2?DayOffset=0&LeagueID=00&gameDate=" + date
    data = getUrlContent2(url)
    rowSet = data["resultSets"][0]["rowSet"]
    for i in range(0, len(rowSet)):
        if rowSet[i][6] == spursID or rowSet[i][7] == spursID:
            if cont == 0:
                scoreSet = data["resultSets"][1]["rowSet"]
                if scoreSet[i * 2][22] is None:
                    WLTimeList[2 + futureGames] = timeStringToCentral(rowSet[i][4])
                    if rowSet[i][11] is None:
                        scoreTV[2 + futureGames] = 'FSSW'
                    else:
                        scoreTV[2 + futureGames] = str(rowSet[i][11])
                else:
                    if scoreSet[i * 2][22] > scoreSet[i * 2 + 1][22]:
                        if rowSet[i][7] == spursID:
                            WLTimeList[2 + futureGames] = 'W'
                        else:
                            WLTimeList[2 + futureGames] = 'L'
                    else:
                        if rowSet[i][6] == spursID:
                            WLTimeList[2 + futureGames] = 'W'
                        else:
                            WLTimeList[2 + futureGames] = 'L'
                    scoreTV[2 + futureGames] = str(scoreSet[i * 2][22]) + '-' + str(scoreSet[i * 2 + 1][22])
            else:
                WLTimeList[2 + futureGames] = timeStringToCentral(rowSet[i][4])
                if rowSet[i][11] is None:
                    scoreTV[2 + futureGames] = 'FSSW'
                else:
                    scoreTV[2 + futureGames] = str(rowSet[i][11])
            # End if
            dateList[2 + futureGames] = str(newDate.month) + '/' + str(newDate.day)
            homeList[2 + futureGames] = teamSubs[str(rowSet[i][6])]
            awayList[2 + futureGames] = teamSubs[str(rowSet[i][7])]
            scheduleList[2 + futureGames] = rowSet[i][5]
            futureGames += 1
            # End if
    # End for
    cont += 1
# End while

print('Got future games')

# Previous Games
for i in range(0, pastGames):
    sidebarText += ('\n' + dateList[i] + ' | [](/r/' + awayList[i] + ') | @ | [](/r/' + homeList[i] + ') | ' + WLTimeList[i] + ' | ' + scoreTV[i])

# Future Games
for i in range(2, 2 + futureGames):
    sidebarText += ('\n' + dateList[i] + ' | [](/r/' + awayList[i] + ') | @ | [](/r/' + homeList[i] + ') | ' + WLTimeList[i] + ' | ' +scoreTV[i])

# ------PLAYER STATS------
playerNames = ["Dejounte Murray", "Marco Belinelli", "DeMar DeRozan", "LaMarcus Aldridge", "Pau Gasol",
               "Patty Mills", "Derrick White", "Jakob Poeltl", "Rudy Gay", "Davis Bertans",
               "Bryn Forbes", "Quincy Pondexter",
               "Dante Cunningham"]

playerIDs = ["1627749", "201158", "201942", "200746", "2200",
             "201988", "1628401", "1627751", "200752", "202722",
             "1627854", "202347",
             "201967"]

rosterSize = len(playerNames)

# Stats table Headers
sidebarText += '\n\n| | | | | | |'
sidebarText += '\n|--:|:--:|:--:|:--:|:--:|:--:|:--:'
sidebarText += '\n**Player** | **PTS** | **REB** | **AST** | **STL** | **BLK**'

for i in range(0, rosterSize):
    # Get data from stats.nba.com in json format
    url = "http://stats.nba.com/stats/playerprofilev2?playerID=" + playerIDs[i] + "&PerMode=PerGame"
    data = getUrlContent2(url)

    # Get headers and career stats by regular seasons
    headersList = data["resultSets"][0]["headers"]
    seasonStatsList = data["resultSets"][0]["rowSet"]

    # Number of different stats (PTS, REB, AST, etc...)
    headersCount = len(headersList)
    # Number of seasons for this player
    seasonsCount = len(seasonStatsList)

    for j in range(0, headersCount):
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
    print("Got " + playerNames[i] + " stats")
    sidebarText += (
        '\n' + playerNames[i] + ' | ' + str(PTS) + ' | ' + str(REB) + ' | ' + str(AST) + ' | ' + str(STL) + ' | ' + str(
            BLK))
# End for

print('Got roster stats')

# Table footer
'''
sidebarText += ('\
n\n| | | | |')
sidebarText += '\n:--:|:--:|:--:|:--:|\n'
'''

# ------RULES-------
sidebarText += '\n\n**BE NICE.**\n'
sidebarText += (
    '\nTroll posts will be removed and violators may be banned. Lighthearted shittalking is allowed. We will make '
    'judgement calls about what qualifies.\n')
sidebarText += '\n**POST SPURS RELATED CONTENT ONLY.**\n'
sidebarText += (
    '\nReaction GIFs, image macros, or memes will be removed if they do not contain content that is substantially '
    'related to the Spurs.\n')
sidebarText += '\n**NO SPAMMING.**\n'
sidebarText += (
    '\nOriginal content from your blog about the Spurs (or similar such content) is welcome, but if that\'s the only '
    'thing you post, and you do not otherwise participate in the community, your posts may be removed.  Duplicate '
    'posts may be removed. Short text "comment" posts may also be removed.\n')

sidebarText += '\n* [](http://en.wikipedia.org/wiki/1998%E2%80%9399_San_Antonio_Spurs_season)'
sidebarText += '\n* [](http://en.wikipedia.org/wiki/2002%E2%80%9303_San_Antonio_Spurs_season)'
sidebarText += '\n* [](http://en.wikipedia.org/wiki/2004%E2%80%9305_San_Antonio_Spurs_season)'
sidebarText += '\n* [](http://en.wikipedia.org/wiki/2006%E2%80%9307_San_Antonio_Spurs_season)'
sidebarText += '\n* [](http://en.wikipedia.org/wiki/2013%E2%80%9314_San_Antonio_Spurs_season)'
sidebarText += '\n* [](http://en.wikipedia.org/wiki/2017%E2%80%9318_San_Antonio_Spurs_season)\n'

sidebarText += '\n1. [](http://en.wikipedia.org/wiki/James_Silas)'
sidebarText += '\n2. [](http://en.wikipedia.org/wiki/George_Gervin)'
sidebarText += '\n3. [](http://en.wikipedia.org/wiki/Johnny_Moore_%28basketball%29)'
sidebarText += '\n4. [](http://en.wikipedia.org/wiki/David_Robinson_%28basketball%29)'
sidebarText += '\n5. [](http://en.wikipedia.org/wiki/Sean_Elliott)'
sidebarText += '\n6. [](http://en.wikipedia.org/wiki/Avery_Johnson)'
sidebarText += '\n7. [](http://en.wikipedia.org/wiki/Bruce_Bowen)'
sidebarText += '\n8. [](http://en.wikipedia.org/wiki/Tim_Duncan)\n'

sidebarText += '\n* [](https://en.wikipedia.org/wiki/1999_NBA_Playoffs)'
sidebarText += '\n* [](https://en.wikipedia.org/wiki/2003_NBA_Playoffs)'
sidebarText += '\n* [](https://en.wikipedia.org/wiki/2005_NBA_Playoffs)'
sidebarText += '\n* [](https://en.wikipedia.org/wiki/2007_NBA_Playoffs)'
sidebarText += '\n* [](https://en.wikipedia.org/wiki/2013_NBA_Playoffs)'
sidebarText += '\n* [](https://en.wikipedia.org/wiki/2014_NBA_Playoffs)\n'

sidebarText += '\n######nba######'
sidebarText += '\n* [](http://reddit.com/r/nba)\n'
sidebarText += '\n#####reddit#####'
sidebarText += '\n* [](http://reddit.com)'

# Post sidebar text to subreddit
print('Reddit Crendentials (Must be moderator of subreddit)')
subreddit = 'nbaspurs'
username = config.username
password = config.password
print('Wait until you see "Done!", ignore warnings')
r = praw.Reddit(user_agent=config.user_agent, client_id=config.client_id,
                client_secret=config.client_secret, password=password, username=username)
print("Updating sidebar...")
r.subreddit(subreddit).mod.update(description=sidebarText)
print('\nDone!')
