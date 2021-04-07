class Block:
    def __init__(self, digit, color):
        self.color = color
        self.digit = digit

class Game:
    def __init__(self):
        self.turn = 0
        self.game_over = False
        self.players = list()
        self.bundle = list()
        self.board = list()
        self.current_player = None
        self.current_idx = 0

        self.add_to_bundle('red')
        self.add_to_bundle('yellow')
        self.add_to_bundle('black')
        self.add_to_bundle('blue')
        self.bundle.append(Block(0, 'red'))
        self.bundle.append(Block(0, 'black'))



    def add_to_bundle(self,color):
        for i in range(26):
            digit = i + 1
            if i>12:
                digit = (i - 13) + 1

            block =  Block(digit, color)
            self.bundle.append(block)
        

    


    def reset_board(self):
        self.board.clear()

    def add_player(self, player):
        self.players.append(player)
        player.set_game(self)


    def grab_block(self, player):
        block = self.bundle.pop()
        player.add_to_hand(block)
    
    def add_section(self, section):
        self.board.append(section)
    
    def add_to_section(self, section, block):
        self.board[section].append(block)

    def remove_from_section(self,section, block):
        b = self.board[section][block].copy()
        del self.board[section][block]
        return b


    def set_turn(self,player):
        self.current_player.is_turn = False
        self.current_player = player
        self.current_player.is_turn = True

    def next_turn(self):
        self.current_idx +=1
        if self.current_idx % (len(self.players)-1) == 0:
            self.current_idx=0
        
        self.set_turn(self.players[self.current_idx])
        

class Player:
    def __init__(self, is_player=False):
        self.hand = list()
        self.is_turn = False
        self.score = 0
        self.game = Game()
        self.is_player = is_player
    
    def add_to_hand(self, block):
        self.hand.append(block)

    def set_game(self,game):
        self.game = game
    
    def reset_hand(self):
        self.hand.clear()

    



game = Game()
player1 = Player()
player2 = Player(True)
game.add_player(player1)
game.add_player(player2)