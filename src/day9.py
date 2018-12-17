import time
from collections import defaultdict
from blist import blist
import pandas as pd

class MarbleGame:
    def __init__(self, n_players, last_marble):
        self.n_players = n_players
        self.last_marble = last_marble
        self.marbles = blist([0])
        self.cur_marble = 0
        self.cur_pos = 0
        self.cur_player = 1
        self.highscores = defaultdict(int)
        self.df = pd.DataFrame(columns=['marble','player','highscore'])
        self.data = []


    def add_marble(self):
        next_marble = self.cur_marble + 1
        if next_marble % 23 != 0:
            new_size = len(self.marbles) + 1
            next_pos = (self.cur_pos + 2)
            if next_pos >= new_size:
                next_pos = 1
            self.marbles.insert(next_pos, next_marble)
        else:
            self.highscores[self.cur_player] += next_marble
            next_pos = self.cur_pos - 7
            next_pos %= len(self.marbles)
            marble_r = self.marbles[next_pos]
            self.marbles.remove(marble_r)
            self.highscores[self.cur_player] += marble_r
            self.data.append([next_marble,self.cur_player,self.highscores[self.cur_player]])
            #print(next_marble,self.cur_player,self.highscores[self.cur_player] )
        self.cur_pos = next_pos
        self.cur_marble = next_marble
        # print(self.cur_player, self.marbles)
        self.cur_player %= self.n_players
        self.cur_player += 1

    def play_game(self):
        for _ in range(0, self.last_marble):
            mg.add_marble()

    def get_highest_score(self):
        return max(self.highscores.values())

    def get_df_as_csv(self,path='../data/marble_game.csv'):
        self.df = pd.DataFrame(self.data,columns=['marble','player','highscore'])
        self.df.to_csv(path)


print("tests:")
#
# mg = MarbleGame(9, 25)
# mg.play_game()
# print(mg.get_highest_score())
#
# mg = MarbleGame(10, 1618)
# mg.play_game()
# print(mg.get_highest_score())
#
# mg = MarbleGame(13, 7999)
# mg.play_game()
# print(mg.get_highest_score())
#
# mg = MarbleGame(17, 1104)
# mg.play_game()
# print(mg.get_highest_score())
#
# mg = MarbleGame(21, 6111)
# mg.play_game()
# print(mg.get_highest_score())
#
# mg = MarbleGame(30, 5807)
# mg.play_game()
# print(mg.get_highest_score())
#
# mg = MarbleGame(424, 71144)
# mg.play_game()
# print(mg.get_highest_score())

mg = MarbleGame(424, 71144*10)
start = time.time()
mg.play_game()
mg.get_df_as_csv()
print(time.time() - start)
print(mg.get_highest_score())
