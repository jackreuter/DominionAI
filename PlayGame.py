from TomBot import TomBot
from ExampleBot import RandBot

from Environment import Environment
import random


class PlayGame:
    
    def __init__(self, bot1, bot2, verbose=False):
        flip = random.randint(1, 2)
        self.flip = flip
        if flip == 1:
            self.p1 = bot1
            self.p2 = bot2
        else:
            self.p2 = bot1
            self.p1 = bot2
            
        self.env = Environment()
        self.verbose = verbose
        
        self.p1_deck = [7, 0, 0, 3, 0, 0, 0]
        self.p2_deck = [7, 0, 0, 3, 0, 0, 0]
        self.p1_hand= [0, 0, 0, 0, 0, 0, 0]
        self.p2_hand= [0, 0, 0, 0, 0, 0, 0]
        self.p1_discard = [0, 0, 0, 0, 0, 0, 0]
        self.p2_discard = [0, 0, 0, 0, 0, 0, 0]
        
        if verbose:
            print("Player 1: {}".format(self.p1.name))
            print("Player 2: {}".format(self.p2.name))
        
    def play_game(self):
        
        # Player 1 is referred to as 1, and Player 2 is -1
        self.clean_up(1)
        self.clean_up(-1)
        
        for turn_number in range(1000):
            
            move = self.p1.get_moves(self.env, self.p1_deck, self.p1_hand, self.p1_discard)
            if self.verbose:
                print(self.p1.name + " buy a: " + get_card_name(move))
            if move >= 0:
                self.p1_discard[move] += 1
                self.env.card_counts[move] -= 1
            if self.env.check_win():
                return [self.declare_winner(), turn_number]
            self.clean_up(1)
                
            move = self.p2.get_moves(self.env, self.p2_deck, self.p2_hand, self.p2_discard)
            if self.verbose:
                print(self.p2.name + " buy a: " + get_card_name(move))
            if move >= 0:
                self.p2_discard[move] += 1
                self.env.card_counts[move] -= 1
            if self.env.check_win():
                return [self.declare_winner(), turn_number]
            self.clean_up(-1)

                       
    def clean_up(self, player):

        if player == 1:
            deck = self.p1_deck
            discard = self.p1_discard
            hand = self.p1_hand
        else:
            deck = self.p2_deck
            discard = self.p2_discard
            hand = self.p2_hand
            
        for i in range(len(hand)):
            discard[i] += hand[i]
            hand[i] = 0
            
        for i in range(5):
            if sum(deck) < 1:
                for i in range(len(discard)):
                    deck[i] += discard[i]
                    discard[i] = 0
            if sum(deck) > 0:
                draw = random.randint(1, sum(deck))
                for j in range(7):
                    if draw <= deck[j]:
                        deck[j] -= 1
                        hand[j] += 1
                        break
                    draw -= deck[j]
    
    
    def declare_winner(self):
        p1_score = self.get_vp(1)
        p2_score = self.get_vp(-1)
        if (p1_score > p2_score):
            if self.flip == 1:
                return 1
            else:
                return -1
        else:
            if self.flip == 1:
                return -1
            else:
                return 1
    
    def get_vp(self, player):
        
        if player == 1:
            return self.p1_deck[3]+self.p1_deck[4]*3+self.p1_deck[5]*6+self.p1_hand[3]+self.p1_hand[4]*3+self.p1_hand[5]*6+self.p1_discard[3]+self.p1_discard[4]*3+self.p1_discard[5]*6
        else:
            return self.p2_deck[3]+self.p2_deck[4]*3+self.p2_deck[5]*6+self.p2_hand[3]+self.p2_hand[4]*3+self.p2_hand[5]*6+self.p2_discard[3]+self.p2_discard[4]*3+self.p2_discard[5]*6
        
def get_card_name(index):
    if index == -1:
        return 'No Buy'
    return ['Copper', 'Silver', 'Gold', 'Estate', 'Duchy', 'Province', 'Curse'][index]


tom_wins = 0
joe_wins = 0
for _ in range(100):
    result = PlayGame(TomBot(), RandBot(), True).play_game()
    if result[0] == 1:
        tom_wins += 1
    else:
        joe_wins += 1
print("Tom: " + str(tom_wins))
print("Joe: " + str(joe_wins))

