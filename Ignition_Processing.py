from ast import Num
from io import TextIOWrapper
import re
import Decision_Types
import Regex_Searches as Searches


positions = {'UTG': 0,
             'UTG+1': 1,
             'UTG+2': 2,
             'Dealer': 3,
             'Small': 4,
             'Big': 5}


class Database:
    def __init__(self):
        self.data = []
        self.num_players = 6

    def process(self, directory):
        for filename in directory:
            file = open(filename, 'r')
            self.process_file(file)
            file.close()

    def process_file(self, file: TextIOWrapper):
        while file.readline():
            hand = Hand(self.num_players, file)
            hand.process()
            break


class Hand:
    def __init__(self, num_players, file: TextIOWrapper):
        self.hero_position = None # in range {0, ..., 5}
        self.num_players = num_players
        self.stacks = [None] * num_players
        self.hole_cards = [[]] * num_players
        self.streets = []
        self.file = file
        self.players = ['UTG', 'UTG+1', 'UTG+2', 'Dealer', 'Small', 'Big']


    def process(self):
        # move file cursor past hand padding
        self.init_stacks()
        self.init_hole_cards()
        preflop = Preflop(self, 0)
        preflop.process()


    def init_stacks(self):
        line = self.file.readline().strip()
        while not line.startswith('***'):
            result = re.search(Searches.StackSize, line)
            if result:
                positionList = result.group(1).strip().split() # i.e ['Small', 'Blind', '[ME]']
                position = positionList[0]
                stackSize = float(result.group(2))
                if 'ME' in positionList[-1]:
                    self.hero_position = position
                try:
                    self.stacks[positions[position]] = stackSize
                except:
                    print(positions[position])

            line = self.file.readline().strip()
            

    def init_hole_cards(self):
        line = self.file.readline().strip()
        toBeDealt = set(positions.keys())
        while len(toBeDealt):
            result = re.search(Searches.HoleCards, line)
            if result:
                position = result.group(1)
                cards = result.group(2).split()
                self.hole_cards[positions[position]] = Card.from_list(cards)
                toBeDealt.remove(position)
            line = self.file.readline().strip()
        

class Street:
    # name: preflop, flop, turn, river
    def __init__(self, name: str, hand: Hand, pot_size):
        self.name = name
        self.hand = hand
        self.comm_cards = None
        self.prior_pot_size = pot_size
        self.actions = [[] for _ in range(self.hand.num_players)]


    def process(self):
        pass


    def init_cards(self):
        pass


class Preflop(Street):
    def __init__(self, hand, pot_size):
        super().__init__('Preflop', hand, pot_size)


    def init_cards(self):
        self.comm_cards = []

    
    def process(self):
        self.init_cards()
        bet_number = 1
        line = self.hand.file.readline().strip()
        while not line.startswith('***'):
            valid_action = re.search(Searches.ValidAction, line)
            if valid_action:
                position = valid_action.group(1).split()[0]
                decision = valid_action.group(2)
                action = Action(bet_number, decision)
                action.process(line)
                if action.decision == 'Raises':
                    bet_number += 1
                self.actions[positions[position]].append(action)
            line = self.hand.file.readline().strip()


class Action:
    def __init__(self, bet_number, decision):
        self.bet_number = bet_number
        self.decision = decision
        self.size = None
        self.all_in = False # only applicable for 'Raises' and 'Bets'


    def process(self, line: str):
        if self.decision == Decision_Types.Bets:
            self.size = Action._process_helper(line, Searches.BetSize)
        elif self.decision == Decision_Types.Raises:
            self.size = Action._process_helper(line, Searches.RaiseSize)
        elif self.decision == Decision_Types.AllIn:
            self.size = Action._process_helper(line, Searches.BetSize)
            self.all_in = True
        elif self.decision == Decision_Types.AllInRaise:
            self.size = Action._process_helper(line, Searches.RaiseSize)
            self.all_in = True
        # No need to do anything more for bet, check, or fold


    def _process_helper(line: str, regexText):
        return float(re.search(regexText, line).group(2))

            
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit


    def __init__(self, cardText: str):
        cardText = cardText.strip()
        if len(cardText) != 2:
            raise cardText
        self.rank = cardText[0]
        self.suit = cardText[1]


    def from_list(cards: list):
        return [Card(card) for card in cards]

    
    def __str__(self):
        return f'{self.rank}{self.suit}'


db = Database()
f = open('log_files/oneHand1.txt', 'r')
db.process_file(f)