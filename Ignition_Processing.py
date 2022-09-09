from io import TextIOWrapper
import re


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
        #preflop.process()
        print("STACKS:\n")
        print(self.stacks)
        print("HOLE CARDS:")
        print(self.hole_cards)


    def init_stacks(self):
        line = self.file.readline().strip()
        while not line.startswith('***'):
            result = re.search(r"Seat \d:([^(]*)\(\$([0-9.]*).*", line)
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
            result = re.search(r"([^\s]*).*dealt.*\[(.*)\].*", line)
            if result:
                position = result.group(1)
                cards = result.group(2).split()
                self.hole_cards[positions[position]] = Card.from_list(cards)
                toBeDealt.remove(position)
            line = self.file.readline().strip()
        

class Street:
    # name: preflop, flop, turn, river
    def __init__(self, name: str, hand: Hand):
        self.name = name
        self.hand = hand
        self.comm_cards = None
        self.actions = [[] for _ in range(self.hand.num_players)]


    def process(self):
        pass


    def init_cards(self):
        pass


class Preflop(Street):
    def __init__(self, hand):
        super().__init__('Preflop', hand)


    def init_cards(self):
        self.comm_cards = []

    
    def process(self):
        self.init_cards()
        bet_number = 1
        line = self.hand.file.readline().strip()
        while not line.startswith('***'):
            action = Action(bet_number)
            action.process(line)
            if action.decision == 'Raise':
                bet_number += 1


class Action:
    def __init__(self, bet_number):
        self.bet_number = bet_number
        self.decision = None
        self.size = None # only applicable for 'raise'

    def process(self, line: str):
        if line.find('Folds') != -1:
            self.decision = 'Fold'
        elif line.find('Calls') != -1:
            self.decision = 'Call'
            self.size = float(line[line.index('$'):].split()[0][1:])
        elif line.find('Checks') != -1:
            self.decision = 'Check'
        else:
            self.decision = 'Raise'
            self.size = float(line[line.index('$'):].split()[0][1:])


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
f = open('log_files/oneHand.txt', 'r')
db.process_file(f)