# import json
import urllib2
import os
# from pprint import pprint
import xml.etree.ElementTree as et

# default url for nfl json
# 2016091112 - date of game and index of the game played that day
"http://www.nfl.com/liveupdate/game-center/2016091112/2016091112_gtd.json"

# url to xml doc of game eid that will help construct urls to each game's json
# http://www.nfl.com/ajax/scorestrip?season=2016&seasonType=REG&week=1

# eidurl = "http://www.nfl.com/ajax/scorestrip?season=2016&seasonType=REG&week=1"
# gameeids = urllib2.urlopen(eidurl).read()

# nflsoup = BeautifulSoup(gameeids,"html.parser")

# nflsoup = ET.fromstring(gameeids)


# print nflsoup.__dict__

class NFLGameRetriever:

    def __init__(self, year):
        self.year = year
        self.gameEIDS = None

    def retrieve_eids(self, weeks):
        """
        Retrieve game eids for range of weeks or a given week.
        Parameters
        ===========
        weeks = list of weeks
        ===========
        """

        gameidslist = []

        for week in weeks:
            eidurl = ("http://www.nfl.com/ajax/scorestrip?season={0}"
                      "&seasonType=REG&week={1}".format(self.year, week))
            print(eidurl)
            gameeids = urllib2.urlopen(eidurl).read()
            nflxml = et.fromstring(gameeids)
            for game in nflxml.iter('g'):
                gameidslist.append(game.get('eid') + "-" + str(week))
        self.gameEIDS = gameidslist
        print("List of NewEIDS", self.gameEIDS)

    def retrieve_nflgame_json(self):
        """
        Constructs NFL URL to json document of statistics for each game.
        Once constructed, json document is downloaded to GameStats{year}
        directory.
        """
        # list of games already downloaded
        game_dir = os.listdir(os.path.join("GameStats{}".format(self.year)))
        game_dir = [os.path.splitext(gameExt)[0] for gameExt in game_dir]
        # list comprehension for list of games not downloaded
        new_game = [game for game in self.gameEIDS if game not in game_dir]
        for game in new_game:
            game_url = game.split("-")[0]
            json_url = ("http://www.nfl.com/liveupdate/game-center"
                        "/{0}/{0}_gtd.json".format(game_url))
            self.game_download(json_url, game)

    def game_download(self, url, game_eid):
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
            "GameStats{}".format(self.year), "{}.json".format(game_eid))
        if not os.path.exists(filename):
            print("{} does not exist".format(filename))
            with open(filename, 'w') as f:
                f.write(gameurl.read())
        else:
            print("{} already exists".format(filename))

    def create_game_directory(self):
        """
        Create directory if it does not exist for that NFL year
        """
        print(os.getcwd())
        game_dir_check = os.path.exists(os.getcwd() + '\\' + "GameStats{}".format(self.year))
        if game_dir_check is False:
            os.mkdir("GameStats{}".format(self.year))
            print("GameStats{} created".format(self.year))


if __name__ == '__main__':
    # retrieveEIDS(year)
    nfl = NFLGameRetriever(2016)
    nfl.create_game_directory()
    nfl.retrieve_eids([5, 7, 10])
    nfl.retrieve_nflgame_json()
