import os
import json
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import pylab
import itertools
import numpy
from collections import OrderedDict

class PlayerAnalysis():

    def __init__(self, year, playerName):
        self.year = year
        self.playerName = playerName
        self.gameList = []

    def listJSONFiles(self):
        gamesDir = os.path.join("GameStats{}".format(self.year))
        print gamesDir
        for gameFiles in os.listdir(gamesDir):
            self.gameList.append(gameFiles)
        print self.gameList

    def getReceivingStats(self):
        receiver_data = OrderedDict()
        
        receiver_data["Names"] = []
        receiver_data["Touchdowns"] = []
        receiver_data["Receptions"] = []
        receiver_data["Yards"] = []
        
        for game in self.gameList:
            gameID = game.strip(".json")
            gameDir = os.path.join("GameStats{0}/{1}".format(self.year, game))
            with open(gameDir) as nfl_file:
                data = json.load(nfl_file)
                home_receiver = data[gameID][u'home'][u'stats'][u'receiving']
                away_receiver = data[gameID][u'away'][u'stats'][u'receiving']
                for rec_id in home_receiver:
                    print rec_id, home_receiver[rec_id][u'name']
                    receiver_data["Names"].append(home_receiver[rec_id][u'name'])
                    receiver_data["Touchdowns"].append(home_receiver[rec_id][u'tds'])
                    receiver_data["Receptions"].append(home_receiver[rec_id][u'rec'])
                    receiver_data["Yards"].append(home_receiver[rec_id][u'yds'])

                for rec_id in away_receiver:
                    print rec_id, away_receiver[rec_id][u'name']
                    receiver_data["Names"].append(away_receiver[rec_id][u'name'])
                    receiver_data["Touchdowns"].append(away_receiver[rec_id][u'tds'])
                    receiver_data["Receptions"].append(away_receiver[rec_id][u'rec'])
                    receiver_data["Yards"].append(away_receiver[rec_id][u'yds'])
        print receiver_data
        df = pd.DataFrame(receiver_data)
        print df.sort_values("Names")
        print df.groupby(['Names'])[["Touchdowns","Receptions","Yards"]].sum().plot(kind="bar")
        pylab.show()

    def getTouchdowns():
        pass

    def playerFantasyPoints(self):
        pass
        """
        25 passing yards = 1 point
        1 pass td = 4 points
        interception = -2 points
        10 rushing yards = 1 point
        rush td = 6 points
        10 rec yards = 1 point
        rec td = 6 points
        """

if __name__ == '__main__':
    pa = PlayerAnalysis(2016,"T. Brady")
    pa.listJSONFiles()
    pa.getReceivingStats()