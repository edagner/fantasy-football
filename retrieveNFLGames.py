import json
import urllib2
import os
from pprint import pprint
import xml.etree.ElementTree as ET

#default url for nfl json
#2016091112 - date of game and index of the game played that day
"http://www.nfl.com/liveupdate/game-center/2016091112/2016091112_gtd.json"

#url to xml doc of game eid that will help construct urls to each game's json
#http://www.nfl.com/ajax/scorestrip?season=2016&seasonType=REG&week=1

eidurl = "http://www.nfl.com/ajax/scorestrip?season=2016&seasonType=REG&week=1"
gameeids = urllib2.urlopen(eidurl).read()

#nflsoup = BeautifulSoup(gameeids,"html.parser")

nflsoup = ET.fromstring(gameeids)


#print nflsoup.__dict__

class NFLGameRetriever():

    def __init__(self, year):
        self.year = year
        self.gameEIDS = None

    def retrieveEIDS(self, startWeek, endWeek):
        """
        Retrieve game eids for range of weeks or a given week.
        Parameters
        ===========
        startWeek - week you begin at
        endWeek - last week you stop at and is inclusive
        ===========
        """

        gameidslist = []

        endRange = endWeek + 1
        for week in range(startWeek, endRange):
            eidurl = ("http://www.nfl.com/ajax/scorestrip?season={0}".format(self.year)
            + "&seasonType=REG&week={0}".format(week))
            print eidurl
            gameeids = urllib2.urlopen(eidurl).read()
            nflxml = ET.fromstring(gameeids)
            for game in nflxml.iter('g'):
                print game.get('eid')
                gameidslist.append(game.get('eid'))
        self.gameEIDS = gameidslist

    def retrieveNFLGameJSON(self):
        """
        Constructs NFL URL to json document of statistics for each game.
        Once constructed, json document is downloaded to GameStats{year}
        directory.
        """
        for game in self.gameEIDS:
            jsonURL = ("http://www.nfl.com/liveupdate/game-center"
            + "/{0}/{0}_gtd.json".format(game))
            self.gameDownload(jsonURL, game)

    def gameDownload(self, url, gameEID):
        """
        Given a NFL URL to a game json, function will download document
        and write to GameStats directory. If json is already present,
        it will not write.
        Parameters
        ===========
        url - NFL game URL
        gameEID - EID for each game
        ===========
        """
        gameurl = urllib2.urlopen(url)
        filename = os.path.join(
            "GameStats{}".format(self.year),"{}.json".format(gameEID))
        if os.path.exists(filename) == False:
            print "{} does not exist".format(filename)
            with open(filename, 'w') as f: 
                f.write(gameurl.read())
        else:
            print "{} already exists".format(filename)

    def createGameDirectory(self):
        """
        Create directory if it does not exist for that NFL year
        """
        print os.getcwd()
        gameDirCheck = os.path.exists(os.getcwd()
            + '\\'
            + "GameStats{}".format(self.year))
        if gameDirCheck == False:
            os.mkdir("GameStats{}".format(self.year))
            print "GameStats{} created".format(self.year) 




if __name__ == '__main__':
    #retrieveEIDS(year)
    nfl = NFLGameRetriever(2016)
    nfl.retrieveEIDS(1,1)
    nfl.retrieveNFLGameJSON()
    #nfl.gameDownload()

    