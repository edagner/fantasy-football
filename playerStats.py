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
        self.player_data = None

    def listJSONFiles(self):
        gamesDir = os.path.join("GameStats{}".format(self.year))
        print gamesDir
        for gameFiles in os.listdir(gamesDir):
            self.gameList.append(gameFiles)
        print self.gameList

    def get_rb_rec_stats(self, playerType):
        player_data = OrderedDict()
        
        player_data["Name"] = []
        player_data["Touchdowns"] = []
        player_data["Yards"] = []
        player_data["TwoPointConv"] = []
        if playerType.lower() in ("receiver", "rec"):
            player_data["Receptions"] = []
            playerKey = u'receiving'
        elif playerType.lower() in ("runningback", "rb"):
            playerKey = u'rushing'

        for game in self.gameList:
            gameID = game.strip(".json")
            gameDir = os.path.join("GameStats{0}/{1}".format(self.year, game))
            with open(gameDir) as nfl_file:
                data = json.load(nfl_file)
                home_player = data[gameID][u'home'][u'stats'][playerKey]
                away_player = data[gameID][u'away'][u'stats'][playerKey]
                for rec_id in home_player:
                    player_data["Name"].append(home_player[rec_id][u'name'])
                    player_data["Touchdowns"].append(home_player[rec_id][u'tds'])
                    player_data["Yards"].append(home_player[rec_id][u'yds'])
                    player_data["TwoPointConv"].append(home_player[rec_id][u'twoptm'])
                    if playerKey == u'receiving':
                        player_data["Receptions"].append(home_player[rec_id][u'rec'])

                for rec_id in away_player:
                    player_data["Name"].append(away_player[rec_id][u'name'])
                    player_data["Touchdowns"].append(away_player[rec_id][u'tds'])
                    player_data["Yards"].append(away_player[rec_id][u'yds'])
                    player_data["TwoPointConv"].append(away_player[rec_id][u'twoptm'])
                    if playerKey == u'receiving':
                        player_data["Receptions"].append(away_player[rec_id][u'rec'])
        
        self.player_data = player_data
        #print self.player_data
    
    def statsDataFrame(self):
        df = pd.DataFrame(self.player_data)
        #print df.sort_values("Names")
        #print df.groupby(['Names'])[["Touchdowns","Receptions","Yards","TwoPointConv"]].sum().head(5).plot(kind="bar")
        #print df.groupby('Names')["Touchdowns","Yards","TwoPointConv"].sum()
        #print df.groupby('Names').sum().sort_values(['Touchdowns','Yards'], ascending=False)
        #print df.groupby('Name').sum().sort_values(['Touchdowns','Yards'],ascending=False).head(10)
        print df[df['Name'] == 'D.Amendola']
        #df["Name"]['D.Amendola']
        #pylab.show()

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
    pa.get_rb_rec_stats('rec')
    pa.statsDataFrame()