import cv2
from extract_blocks import extract_blocks, predict_blocks, extract_section
import numpy as np
from PIL import ImageGrab
from game_rules import check_if_move_possible, divide_colors,check_section,check_move

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
            
            #Save frame to directory
            # cv2.imwrite(f'{write_directory}/{counter}_image.png', frame)
            # print(f'saved image {counter}')
            counter+=1

    if predict:
        sections = extract_section(frame)
        sections = [ [section, []] for section in sections ]
        if len(sections)>0:
            for section in sections:
                x,y,w,h = section[0]
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)


        rectangles = extract_blocks(frame)

            # for s in sections:
            #     msg = "section "
            #     for r in s:
            #         msg += f'{r[1]} {r[2]}'
            #     print((msg))

        predict = False
        c_hand = divide_colors(hand)
        print('-------------------------------------------------------------------------------------------')
        # print(c_hand['blue'])
        print('black',check_if_move_possible(c_hand['black']), ' red',check_if_move_possible(c_hand['red']))
        print('yellow',check_if_move_possible(c_hand['yellow']), ' blue',check_if_move_possible(c_hand['blue']))
        for rectangle in rectangles:
                x,y,w,h = rectangle[0]
                _,digit,color = rectangle
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

                if y >350:
                    hand.append([digit, color])
                else:

                    for section in sections:
                        sx,sy,sw,sh = section[0]
                        margin = 5

                        if x>sx-margin and x+w < sx+sw+margin and y>sy-margin and y+h<sy+sh:
                            section[1].append(rectangle)
                font  = cv2.FONT_HERSHEY_SIMPLEX
                fontScale  = 0.5

        for section in sections:
            msg = 'section with '
            for block in section[1]:
                msg+= f' {block[1]} {block[2]} '
            move_type = check_section(section)
            msg+= move_type
            print(msg)


    

    if draw_rects:
        if len(rectangles)>0:
            for rectangle in rectangles:
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








    # print('--------------------')





    # for section in game_board:
    #     msg = 'section with '
    #     for block in section:
    #         msg+= f' {block[1]} {block[2]} '
    
        # print(msg)
    # print(game_board)
    

    cv2.imshow('Game', frame)

            
cv2.destroyAllWindows()

