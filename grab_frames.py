import cv2
from extract_blocks import extract_rectangles, predict_blocks
import numpy as np
from PIL import ImageGrab
from game_rules import check_if_move_possible, divide_colors

record = False
predict = False

#Directory to write recorded frames
counter = 0
write_directory = f'D:/Desktop/stage/images/raw/' 

#Manage screenshot speed
framecounter = 0
frames = 20


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

    if record:
        framecounter+=1
        if framecounter%frames==0:
            framecounter = framecounter-frames
            
            #Save frame to directory
            cv2.imwrite(f'{write_directory}/{counter}_image.png', frame)
            print(f'saved image {counter}')
            counter+=1

    if predict:
        rectangles = extract_rectangles(frame)
        cur_section = list()
        if len(rectangles)>0:
            for rectangle in rectangles:
                x,y,w,h = rectangle[0]
                _,digit,color = rectangle
                
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

                # cv2.rectangle(frame, (0, 350), (960, 540), (0,0,255),2)
                if y >350:
                    hand.append([digit, color])
                # if len(game_board>1):
                    # if game_board[-1][0]
                    # game_board[-1]./append(predictions)


                # predictions = predict_blocks(rectange, frame)
                # print(predictions)
                # for pred in predictions:
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

    # print('--------------------')
    # for section in game_board:
    #     msg = 'section with '
    #     for block in section:
    #         msg+= f' {block[1]} {block[2]} '
    
    #     print(msg)
    # print(game_board)
    

    c_hand = divide_colors(hand)
    print('-------------------------------------------------------------------------------------------')
    # print(c_hand['blue'])
    print('black',check_if_move_possible(c_hand['black']), ' red',check_if_move_possible(c_hand['red']))
    print('yellow',check_if_move_possible(c_hand['yellow']), ' blue',check_if_move_possible(c_hand['blue']))
    cv2.imshow('Game', frame)


    
            
cv2.destroyAllWindows()

