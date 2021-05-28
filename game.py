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

    def reset_bundle(self):
        self.bundle.clear()
        self.add_to_bundle('red')
        self.add_to_bundle('yellow')
        self.add_to_bundle('black')
        self.add_to_bundle('blue')
        self.bundle.append(Block(0, 'red'))
        self.bundle.append(Block(0, 'black'))

    def add_player(self, player):
        self.players.append(player)
        player.set_game(self)

    

    def check_if_valid(self, section, block):
        valid = False
        digits, colors, section_type  = self.check_section_type(section)

        if section_type == 's':
            # check if same digit check if different color check if joker
            if (digits[0]== block.digit and block.color not in colors) or block.digit == 0:
                valid=True
        else:
            # check if same color check if counting 
            if block.digit == 0:
                valid=True
            elif block.color == colors[0]:
                digits.sort()
                # check if its in the middle or if its upper or lower
                # if block.digit > digits[0] and block.digit<digits[-1]:
                #     if digits[-1] - block.digit >=3:
                #         valid=True
                if block.digit == digits[0]-1:
                    valid=True
                elif block.digit == digits[-1]+1:
                    valid=True
        
        return valid
        

    def check_all_sections(self,block):
        for section in self.board:
            if self.check_if_valid(section, block):
                prt = [f'{b.digit} {b.color}' for b in section]
                print(f'You can place -[ {block.digit} {block.color} ]- in section -[ {" ".join(prt)} ]-')


    def check_if_moves_in_hand(self,player):
        for block in player.hand:
            self.check_all_sections(block)

    def check_section_type(self,section):
        digits = [block.digit for block in section]
        colors = [block.color for block in section]

        set_digits = [s for s in set(digits)]

        if len(set_digits) == 1 or (len(set_digits)==2 and (set_digits[0]==0 or set_digits[1]==0)):
            return [digits,colors, 's']
        else:
            return [digits,colors, 'c']

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

    def check_move_in_hand(self):
        cur_hand = self.hand
        cur_hand.sort()
        cur_move = list()
        possible_moves = list()
        for i in range(len(cur_hand)-1):
            cur_move.append(cur_hand[i])

            if i == len(cur_hand)-2:
                if cur_hand[i].block +1 == cur_hand[i+1].block:
                    cur_move.append(cur_hand[i+1])

                if (len(cur_move)>=3):
                    possible_moves.append([x for x in cur_move])
                cur_move.clear()

            elif (not cur_hand[i].digit +1 == cur_hand[i+1].digit ):
                if (len(cur_move)>=3):
                    possible_moves.append([x for x in cur_move])
                cur_move.clear()

        return possible_moves

    def check_if_valid(self, section, block):
        valid = False
        digits, colors, section_type  = self.check_section_type(section)

        if section_type == 's':
            # check if same digit check if different color check if joker
            if (digits[0]== block.digit and block.color not in colors) or block.digit == 0:
                valid=True
        else:
            # check if same color check if counting 
            if block.digit == 0:
                valid=True
            elif block.color == colors[0]:
                digits.sort()
                # check if its in the middle or if its upper or lower
                # if block.digit > digits[0] and block.digit<digits[-1]:
                #     if digits[-1] - block.digit >=3:
                #         valid=True
                if block.digit == digits[0]-1:
                    valid=True
                elif block.digit == digits[-1]+1:
                    valid=True
        
        return valid

    def check_all_sections(self,block):
        for section in self.board:
            if self.check_if_valid(section, block):
                prt = [f'{b.digit} {b.color}' for b in section]
                print(f'You can place -[ {block.digit} {block.color} ]- in section -[ {" ".join(prt)} ]-')


    def check_if_moves_in_hand(self,player):
        for block in player.hand:
            self.check_all_sections(block)

    def check_section_type(self,section):
        digits = [block.digit for block in section]
        colors = [block.color for block in section]

        set_digits = [s for s in set(digits)]

        if len(set_digits) == 1 or (len(set_digits)==2 and (set_digits[0]==0 or set_digits[1]==0)):
            return [digits,colors, 's']
        else:
            return [digits,colors, 'c']

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

    



from collections import namedtuple
from random import choice
from mcts import MCTS, Node
_RKB = namedtuple("RummikubBoard", "tup instructions hand bag turn_moves inhand turn winner terminal moves_zero")

class RummikubBoard(_RKB, Node):
   
    def move_section_excess(board, all_sections):
        excess = list()
        for i, section in enumerate(all_sections):
            cur_section = sorted(section, key=lambda a: a.digit)
            if len(cur_section)>3:
                digits, colors, section_type  = board.check_section_type(cur_section)
                lst = [(x.digit, x.color) for x in board.hand]
                if section_type == 's':
                    s_lst = [x for x in cur_section if x.digit == 0]
                    if len(s_lst)>0:
                        excess.append(s_lst[0])
                    else:
                        block = choice(cur_section)
                        if (block.digit, block.color) not in lst:
                                excess.append( block) 
                            # board.instructions += f"Using {block.digit} {block.color} from {[f'{x.digit} {x.color}' for x in section]}"
                else:
                    if (cur_section[-1].digit, cur_section[-1].color) not in lst:
                        excess.append(cur_section[-1])
                        # board.instructions += f"Using {block.digit} {block.color} from {[f'{x.digit} {x.color}' for x in cur_section]}"
                    elif (cur_section[0].digit, cur_section[0].color) not in lst:
                        excess.append(cur_section[0])
                        # board.instructions += f"Using {block.digit} {block.color} from {[f'{x.digit} {x.color}' for x in section]}"
        return excess

    def all_possible_moves(board,all_sections,hand):
        moves = list()

        excess = board.move_section_excess(board.tup)
        cur_hand = list(board.hand)
        cur_hand.extend(excess)
        # print('excess -------------')
        # for x in excess:
        #     print(f'{x.digit} {x.color}')
        # print('-----------------')
        cur_hand = sorted(cur_hand, key=lambda a: a.digit)
        # print('Hand -------------')
        # for h in cur_hand:
        #     print(f'{h.digit} {h.color}')
        # print('-------------------')
        cur_move_counting = list()
        cur_move_same = list()
  
        for i in range(len(cur_hand)-1):
            cur_move_counting.clear()
            cur_move_same.clear()
            cur_move_counting.append(cur_hand[i])
            cur_move_same.append(cur_hand[i])
            for block in cur_hand[i+1:]:

                if ( block.digit  == cur_move_counting[-1].digit +1 and block.color == cur_move_counting[-1].color) or (block.digit == 0 or cur_move_counting[-1].digit == 0) :
                    cur_move_counting.append(block)

                colors = [x.color for x in cur_move_same if not x.digit ==0]
    
                if (block.digit  == cur_move_same[-1].digit  and (not block.color in colors)) or (block.digit == 0 or cur_move_same[-1] == 0):
                    cur_move_same.append(block)
            
            if len(cur_move_counting)>=3:
                moves.append([[x for x in cur_move_counting],[],-1,-1])

                
            if len(cur_move_same)>=3:
                moves.append([[x for x in cur_move_same],[],-1,-1])
            
            

        for sectionidx,section in enumerate(all_sections):
            for blockidx,block in enumerate(hand):
                if board.check_if_valid(section, block):
                    
                    moves.append((block,section,blockidx,sectionidx))
        return tuple(moves)


    def check_hand_for_moves(board,hand):
        cur_hand = board.hand
        cur_hand.sort()
        cur_move = list()
        possible_moves = list()


        for i in range(len(cur_hand)-1):
            cur_move.append([cur_hand[i], i])

            if i == len(cur_hand)-2:
                if cur_hand[i].block +1 == cur_hand[i+1].block:
                    cur_move.append([cur_hand[i+1], i+1])

                if (len(cur_move)>=3):
                    possible_moves.append([x for x in cur_move])
                cur_move.clear()

            elif (not cur_hand[i].digit +1 == cur_hand[i+1].digit ):
                if (len(cur_move)>=3):
                    possible_moves.append([x for x in cur_move])
                cur_move.clear()
        return tuple(possible_moves)


    def check_section_type(self,section):
        digits = [block.digit for block in section]
        colors = [block.color for block in section]

        set_digits = [s for s in set(digits)]

        if len(set_digits) == 1 or (len(set_digits)==2 and (set_digits[0]==0 or set_digits[1]==0)):
            return [digits,colors, 's']
        else:
            return [digits,colors, 'c']
            
    def find_children(board):
        if board.terminal:
            return set()


        if board.turn:
            apm = board.all_possible_moves(board.tup, board.hand)
            return {
                board.make_move(value) for i,value in enumerate(apm)
            }
        else:
            apm = board.all_possible_moves(board.tup, [choice(board.bag) for _ in range(board.inhand)] )
            return {
                board.make_move(value) for i,value in enumerate(apm)
            }
    
    def find_random_child(board):
        if board.terminal:
            return None

        if board.turn:
            apm = board.all_possible_moves(board.tup, board.hand)
            if len(apm)<=0: 
                return board.make_move([-1,-1,-1,-1])
            else:
                return board.make_move(choice(apm))
        else:
            if len(board.bag)<=0:
                return board.make_move([-1,-1,-1,-1])
            apm = board.all_possible_moves(board.tup, [choice(board.bag) for _ in range(board.inhand)] )
            if len(apm)<=0: 
                return board.make_move([-1,-1,-1,-1])
            else:
                return board.make_move(choice(apm))
                    
        
    def reward(board):
        if not board.terminal:
            raise RuntimeError(f"reward called on nonterminal board {board}")
        # if board.winner is board.turn:
        #     #It's your turn and you've already won
        #     raise RuntimeError(f"reward called on unreachable board {board}")
        
        if board.turn is (not board.winner):
            return 0
        if board.winner is None:
            return board.turn_moves + 0.5 
        if board.winner is True:
            return 100
        raise RuntimeError(f"Board has unknown winner type {board.winner}")

    def is_terminal(board):
        return board.terminal
        
    def get_instructions(board):
        return board.instructions

    

    def check_if_valid(board, section, block):
        valid = False
        digits, colors, section_type  = board.check_section_type(section)

        if section_type == 's':
            # check if same digit check if different color check if joker
            joker_color = ''
            for b in section:
                if b.digit == 0:
                    joker_color = b.color
                

            if (digits[1]== block.digit and (block.color not in colors or block.color == joker_color)) or block.digit == 0:
                valid=True
        else:
            # check if same color check if counting 
            if block.digit == 0:
                valid=True
            
            elif block.color == colors[0]:
                digits.sort()

                if digits[0] == 0 and digits[1]-2 == block.digit:
                    valid = True

                
                # check if its in the middle or if its upper or lower
                # if block.digit > digits[0] and block.digit<digits[-1]:
                #     if digits[-1] - block.digit >=3:
                #         valid=True
                elif block.digit == digits[0]-1:
                    valid=True
                elif block.digit == digits[-1]+1:
                    valid=True
        
                elif len(digits)>=5: 
                    if digits[2] == block.digit:
                        valid = True
                    elif digits[-3] == block.digit:
                        valid = True
                    elif len(digits)>6:
                        for i in range(len(digits)-6):
                            if digits[2+i] == block.digit:
                                valid = True
        return valid

    def make_move(board, move):
        block, section, blockidx, sectionidx = move
        hand = list(board.hand)
        bag = list(board.bag)
        turn = board.turn
        turn_moves = board.turn_moves
        instructions =board.instructions
        inhand= board.inhand
        moves_zero = board.moves_zero
        tup = board.tup
        
        if block == -1:
            if turn_moves == 0:
                if board.turn: 
                    instructions +="\nTake block from bag"
                    turn = not board.turn
                    winner = None 
                if len(bag)>0:
                    hand.append(bag.pop())
            moves_zero +=1
            turn = not board.turn
            turn_moves=0
        
        else:

            tup = list(board.tup)
            tup = [sorted(x, key=lambda y: y.digit) for x in tup ]
            tup = tuple(tup)

            if board.turn:
                turn_moves+=1
                if type(block) is list and len(block)>0:
                    instructions+= f"\nMove blocks [ {[f'{b.digit} {b.color}'for b in block]} ]  to the board (new section)"
                    turn_moves+=len(block)
                    for blck in block:
                        add=[x for x in hand if x.digit == blck.digit and x.color == blck.color]
                        if len(add)>0:
                            hand.remove(blck)    
                else:
                    instructions+=f"\nMove block {block.digit} {block.color} to section {[f'{x.digit} {x.color}' for x in tup[sectionidx] if sectionidx > -1]}"
                    add=[x for x in hand if x.digit == block.digit and x.color == block.color]
                    hand.remove(add[0])
            else:
                if type(block) is list and len(block)>0:
                    for blck in block:
                        add=[x for x in hand if x.digit == blck.digit and x.color == blck.color]
                        if len(add)>0:
                            hand.remove(add[0])  
                else:

                    add=[x for x in bag if x.digit == block.digit and x.color == block.color]
                    bag.remove(add[0])
                    inhand-=1
            

        if board.turn and len(hand)<=0:
            winner = True
        elif not board.turn and inhand<=0:
            winner = True
        elif moves_zero > 5:
            winner = None
            moves_zero = 0
        elif turn_moves > 100:
            winner = None
        else:
            winner = False        

        is_terminal = winner if winner is not None else True
        # print(f'turn moves {block.digit if block != -1 else -1} {block.color if block != -1 else " "}')
        # print(f'turn moves {turn_moves}')
        return RummikubBoard(
            to_tuple(tup),
            instructions, 
            to_tuple(hand), 
            to_tuple(bag), 
            turn_moves, 
            inhand, 
            turn, 
            winner, 
            is_terminal, 
            moves_zero)        
    

def to_tuple(lst):
    return tuple(to_tuple(i) if isinstance(i, list) else i for i in lst)








            


