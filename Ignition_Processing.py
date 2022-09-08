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

    def process_file(self, file):
        while file.readline():
            hand = Hand(self.num_players, file)
            hand.process()


class Hand:
    def __init__(self, num_players, file):
        self.hero_position = None # in range {0, ..., 5}
        self.stacks = [] * num_players
        self.hole_cards = [] * num_players
        self.streets = []
        self.file = file
        self.players = ['UTG', 'UTG+1', 'UTG+2', 'Dealer', 'Small', 'Big']


    class Street:
        # name: preflop, flop, turn, river
        def __init__(self, name: str, hand):
            self.name = name
            self.hand = hand
            self.comm_cards = None
            self.actions = [[] for _ in range(len(self.stacks))]


        def process(self):
           pass


        def init_cards(self):
            pass

    class Preflop(Street):
        def __init__(self):
            super().__init__('Preflop')

        def process(self):
            self.init_cards()
            bet_number = 1
            line = self.hand.file.readline()
            # UTG
            while line[:3] != 'UTG':
                line = self.hand.file.readline()
            action = Action(bet_number)
            action.process(line)
            if action.decision == 'Raise':
                bet_number += 1
            self.actions[positions['UTG']].append(action)



        def init_cards(self):
            self.comm_cards = []

    def process(self):
        # move file cursor past hand padding
        while self.file.readline(3) != 'Ign':
            continue
        self.init_stacks()
        while self.file.readline(3) != '***':
            continue
        self.init_hole_cards()
        preflop = self.Preflop()
        preflop.process()


    def init_stacks(self):
        line = self.file.readline()
        for i in range(len(self.stacks)):
            idx = line.index('$')
            stack = float(line[idx:].split()[0][1:])
            self.stacks[i] = stack
            # check if current player is the hero
            if line.find('ME') != -1:
                self.hero_position = i

    def init_hole_cards(self):
        line = self.file.readline()
        num_players = len(self.hole_cards)
        for i in range(num_players):
            idx = line.index('[')
            cards = [Card(line[idx + 1], line[idx + 2]), Card(line[idx + 4], line[idx + 5])]
            self.hole_cards[i] = cards



class Action:
    def __init__(self, bet_number):
        self.bet_number = bet_number
        self.decision = None
        self.size = None # only applicable for 'raise'

    def process(self, line):
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
