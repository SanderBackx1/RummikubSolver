#First only digit+color from hand in order


the_hand = [3,1,2,6,4,5,9,10,12]

hand2 = [
    [3, 'red'],[1,'red'],[2,'red'],[6,'red'],[4,'red'],[5,'red'],[9,'red'],[10,'red'],[12,'red'],
    [3, 'black'],[1,'black'],[2,'black'],[6,'black'],[4,'black'],[5,'black'],[9,'black'],[10,'black'],[12,'black'],
    [2, 'yellow'],[1,'yellow'],[8,'yellow'],[6,'yellow'],[4,'yellow'],[5,'yellow'],[9,'yellow'],[10,'yellow'],[12,'yellow'],
    [5, 'blue'],[8,'blue'],[2,'blue'],[9,'blue'],[2,'blue'],[1,'blue'],[10,'blue'],
]




def check_if_move_possible(hand):
    cur_hand = hand
    cur_hand.sort()
    cur_move = list()
    possible_moves = list()
    for i in range(len(cur_hand)-1):
        cur_move.append(cur_hand[i])

        if i == len(cur_hand)-2:
            if cur_hand[i] +1 == cur_hand[i+1]:
                cur_move.append(cur_hand[i+1])

            if (len(cur_move)>=3):
                possible_moves.append([x for x in cur_move])
            cur_move.clear()

        elif (not cur_hand[i] +1 == cur_hand[i+1] ):
            if (len(cur_move)>=3):
                possible_moves.append([x for x in cur_move])
            cur_move.clear()

    return possible_moves




def divide_colors(hand):
    cur_color = dict()
    cur_color = {
        'red':[],
        'blue':[],
        'black':[],
        'yellow':[]
    }
    for block in hand:
        color = block[1]
        if not color =='':
            cur_color[color].append(block[0])

    return cur_color
        


red = divide_colors(hand2)['red']
blue = divide_colors(hand2)['blue']
black = divide_colors(hand2)['black']
yellow = divide_colors(hand2)['yellow']

print('red',check_if_move_possible(red))
print('blue',check_if_move_possible(blue))
print('black',check_if_move_possible(black))
print('yellow',check_if_move_possible(yellow))





def check_section(section):
    digits = [block.digit for block in section]
    colors = [block.color for block in section]
    #check if same
    set_digits = [s for s in set(digits)]

    if len(set_digits) == 1 or (len(set_digits) == 2 and (set_digits[0] == 0 or set_digits[1] == 0)):
        return 's'
    else:
        return 'c'


def check_move(section, hand, type):
    digits = [block[1] for block in section[1]]
    colors = [block[2] for block in section[1]]

    for block in hand:
        if type == 's' and block[1] == digits[1] and block[2] not in colors:
            print(f'can place {block} in section {section}') 







# print(divide_colors(hand2))

        
        
