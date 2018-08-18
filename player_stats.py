import os
import json
import pandas as pd
import matplotlib
import pylab
import itertools
import numpy
from collections import OrderedDict
matplotlib.use('TkAgg')


class PlayerAnalysis:
    def __init__(self, year, player_name):
        self.year = year
        self.playerName = player_name
        self.gameList = []
        self.player_data = None
        self.gameDir = None

    def list_json_files(self):
        self.gameDir = os.path.join("GameStats{}-1".format(self.year))
        print(self.gameDir)
        for gameFiles in os.listdir(self.gameDir):
            self.gameList.append(gameFiles)
        print(self.gameList)

    def get_rb_rec_stats(self, player_type):
        player_data = OrderedDict()
        
        player_data["Name"] = []
        player_data["Touchdowns"] = []
        player_data["Yards"] = []
        player_data["TwoPointConv"] = []
        player_data["Week"] = []
        if player_type.lower() in ("receiver", "rec"):
            player_data["Receptions"] = []
            player_key = u'receiving'
        elif player_type.lower() in ("runningback", "rb"):
            player_key = u'rushing'

        for game in self.gameList:
            game_id = game.split("-")[0]
            week = game.split("-")[1].strip(".json")
            game_dir = os.path.join("{0}/{1}".format(self.gameDir, game))
            with open(game_dir) as nfl_file:
                data = json.load(nfl_file)
                home_player = data[game_id][u'home'][u'stats'][player_key]
                away_player = data[game_id][u'away'][u'stats'][player_key]
                for rec_id in home_player:
                    player_data["Name"].append(home_player[rec_id][u'name'])
                    player_data["Touchdowns"].append(home_player[rec_id][u'tds'])
                    player_data["Yards"].append(home_player[rec_id][u'yds'])
                    player_data["TwoPointConv"].append(home_player[rec_id][u'twoptm'])
                    player_data["Week"].append(week)
                    if player_key == u'receiving':
                        player_data["Receptions"].append(home_player[rec_id][u'rec'])

                for rec_id in away_player:
                    player_data["Name"].append(away_player[rec_id][u'name'])
                    player_data["Touchdowns"].append(away_player[rec_id][u'tds'])
                    player_data["Yards"].append(away_player[rec_id][u'yds'])
                    player_data["TwoPointConv"].append(away_player[rec_id][u'twoptm'])
                    player_data["Week"].append(week)
                    if player_key == u'receiving':
                        player_data["Receptions"].append(away_player[rec_id][u'rec'])
        
        self.player_data = player_data
        print(self.player_data)
    
    def stats_dataframe(self):
        df = pd.DataFrame(self.player_data)
        print(df.sort_values("Name"))
        # print(df.groupby(['Names'])[["Touchdowns","Receptions","Yards","TwoPointConv"]].sum().head(5).plot(kind="bar")))
        # print(df.groupby('Names')["Touchdowns","Yards","TwoPointConv"].sum())
        # print(df.groupby('Names').sum().sort_values(['Touchdowns','Yards'], ascending=False))
        # print(df.groupby('Name').sum().sort_values(['Touchdowns','Yards'],ascending=False).head(10))
        print(df[df['Name'] == self.playerName][['Name', 'Yards', 'Week']].plot(x="Week", y='Yards', kind="bar"))
        # print(df.loc[df['Name'] == self.playerName][['Name','Yards',]].plot(x="Name",kind="bar"))
        # print(df[df['Name'] == self.playerName].plot(x="Name",kind="bar"))
        # df["Name"]['D.Amendola']
        pylab.show()

    def player_fantasy_points(self):
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
    pa = PlayerAnalysis(2016, "D.Amendola")
    pa.list_json_files()
    pa.get_rb_rec_stats('rec')
    pa.stats_dataframe()
