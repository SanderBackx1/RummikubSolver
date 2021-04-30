import cv2
from extract_blocks import extract_blocks, predict_blocks, extract_section
import numpy as np
from PIL import ImageGrab
from game_rules import check_if_move_possible, divide_colors,check_section,check_move
from game import Game, Player, Block, RummikubBoard
from mcts import MCTS, Node




def draw_rect(rectangle, frame):
    x,y,w,h = rectangle[0]
    _,digit,color = rectangle
    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

    font  = cv2.FONT_HERSHEY_SIMPLEX
    fontScale  = 0.5


    fontColor = (0,0,255)
    
    lineType= 2
    x,y,w,h = rectangle[0]
    bottomLeftCornerOfText = (x + int(w/2)-5,y + int(h/3)+int(h/3))
    if rectangle[2]=='blue':
        fontColor = (255,0,0)
    elif rectangle[2] =='black':
        fontColor = (0,0,0)
    elif rectangle[2] =='red':
        fontColor=(0,0,255)
    elif rectangle[2] == 'yellow':
        fontColor = (90,145,250)
    cv2.putText(frame,f'{rectangle[1]}', 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)


    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)

def run():
    record = False
    predict = False
    draw_rects = False

    #Directory to write recorded frames
    counter = 0
    write_directory = f'D:/Desktop/stage/images/raw/' 

    #Manage screenshot speed
    framecounter = 0
    frames = 20

    c_hand = list()
    rectangles = list()
    sections = list()



    game = Game()
    player1 = Player()
    ai_player = Player(True)
    game.add_player(player1)
    game.add_player(ai_player)
    while True:
        

        hand = list()
        game_board = list()
        resolutionx, resolutiony = (960,540)
        margin = 35

        frame = np.array(ImageGrab.grab(bbox=(0, margin, resolutionx, resolutiony+margin)))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


        k = cv2.waitKey(10)

        if k == ord('q'):
            break;
        elif k == ord('r'):
            #Toggle recording
            record = not record
            print(f'recording {record}')
        elif k == ord('p'):
            predict = not predict
            print(f'predicting {predict}')
        elif k == ord('d'):
            draw_rects = not draw_rects
            print(f'drawing on screen')


        if record:
            framecounter+=1
            if framecounter%frames==0:
                framecounter = framecounter-frames
                counter+=1

        if predict:
            ai_player.reset_hand()
            game.reset_board()
            game.reset_bundle()
            sections = extract_section(frame)
            sections = [ [section, []] for section in sections ]
            if len(sections)>0:
                for section in sections:
                    x,y,w,h = section[0]
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)


            rectangles = extract_blocks(frame)

            predict = False
            for rectangle in rectangles:
                x,y,w,h = rectangle[0]
                _,digit,color = rectangle
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                if y >350:
                    hand.append([digit, color])
                    blocks = [x for x in game.bundle if x.digit == digit and x.color==color]
                    #get block from bundle
                    if len(blocks)>0:
                        #add to player hand and remove from bundle
                        ai_player.add_to_hand(blocks[0])
                        game.bundle.remove(blocks[0])
                else:
                    #add to board section
                    for section in sections:
                        sx,sy,sw,sh = section[0]
                        margin = 5

                        if x>sx-margin and x+w < sx+sw+margin and y>sy-margin and y+h<sy+sh:
                            section[1].append(rectangle)
                font  = cv2.FONT_HERSHEY_SIMPLEX
                fontScale  = 0.5

            c_hand = divide_colors(hand)


            print('-------------------------------------------------------------------------------------------')
            # print(c_hand['blue'])
            
            h = [f'{x.digit} {x.color}' for x in ai_player.hand]
            print(h)


            print('black',check_if_move_possible(c_hand['black']), ' red',check_if_move_possible(c_hand['red']))
            print('yellow',check_if_move_possible(c_hand['yellow']), ' blue',check_if_move_possible(c_hand['blue']))



            for section in sections:
                new=list()
                for block in section[1]:
                    add=[x for x in game.bundle if x.digit == block[1] and x.color == block[2]]
                    if len(add)>0:
                        new.append(add[0])
                        game.bundle.remove((add[0]))
                game.add_section(new)

            print(len(game.bundle))
            for section in game.board:
                msg = 'section with '
                for block in section:
                    msg+= f'{block.digit} {block.color} '

                move_type = check_section(section)
                msg+= move_type
                print(msg)

            # game.check_if_moves_in_hand(ai_player)
            play_game(game.board, ai_player.hand, game.bundle)
            






        

        if draw_rects:
            if len(rectangles)>0:
                for rectangle in rectangles:
                    draw_rect(rectangle, frame)

        

        cv2.imshow('Game', frame)


def play_game(board, hand, bag):
    tree=MCTS()
    # inhand = int(input("enter how many ai has in hand: "))
    c = [1,2,3,4]
    c = set(c)
    b = RummikubBoard(
        to_tuple(board), 
        "", 
        to_tuple(hand), 
        to_tuple(bag), 
        0, 
        len(hand),
        True, 
        False, 
        False, 0)   

    for i in range(50):
        tree.do_rollout(b)
    print('done')
    print('------------')
    if len(b.find_children()) <1:
        print("No moves possible")
    else:
        board = tree.choose(b)
        print(board.instructions)
    print('------------')

def to_tuple(lst):
    return tuple(to_tuple(i) if isinstance(i, list) else i for i in lst)

if __name__ == "__main__":
    run()
    cv2.destroyAllWindows()


