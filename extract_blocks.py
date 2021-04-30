import pickle 
import cv2
import numpy as np


loaded_model = pickle.load(open('models/finalized_model7.sav', 'rb'))
c_count=0;
c_size = 'large'

def extract_section(img):
    rectangles = list()

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    COLOR_MIN = np.array([136, 133, 124],np.uint8)
    COLOR_MAX = np.array([236, 234, 237],np.uint8)
    frame_threshed = cv2.inRange(img, COLOR_MIN, COLOR_MAX)
    ret,thresh = cv2.threshold(frame_threshed,127,255,0)
    blur = cv2.blur(thresh,(5,5))
    contours, hierarchy = cv2.findContours(blur,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        if x>100 and y > 25 and x < 180+620 and y < 400:
            if w > 50 and h > 40 and h < 80:
                # print(h)
                # uncomment to show green rectangles
                rectangles.append((x,y,w,h))

    return rectangles



def extract_blocks(img):
    rectangles = list()
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    COLOR_MIN = np.array([190, 190, 190],np.uint8)
    COLOR_MAX = np.array([240, 240, 240],np.uint8)
    frame_threshed = cv2.inRange(img, COLOR_MIN, COLOR_MAX)
    ret,thresh = cv2.threshold(frame_threshed,127,255,0)
    blur = cv2.blur(thresh,(5,5))
    contours, hierarchy = cv2.findContours(blur,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


    imagem = cv2.bitwise_not(frame_threshed)
    _, binary_image = cv2.threshold(imagem, 0, 255, cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(binary_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:

        x,y,w,h = cv2.boundingRect(cnt)
        if x>125 and x<830:
            if w > 20 and h > 40 and h < 100:

                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                rectangles.append(([x,y,w,h],predict_digit(img[y:y+h, x:x+w]),predict_color(img[y:y+h, x:x+w])))
    
    
    # cv2.imshow('ddd', img);
    # cv2.imshow("thresh", binary_image)
    return rectangles

def predict_blocks(rectangles, im):
    x,y,w,h = rectangles
    blocks = 0
    block_w = 0
    b_predicts=list()
    global c_size

    roi = im[y:y+h, x+(block_w*i):x+(block_w*(i+1)  )]
    digit_predict = predict_digit(roi)
    color_predict = predict_color(roi)
    b_predicts.append([[ x+(block_w*i),y,block_w,h], digit_predict,color_predict])
    roi = im[y:y+h, x+(block_w*i):x+(block_w*(i+1))]

    return b_predicts

def predict_digit(block):
    lower = [136, 133, 124]
    upper = [236, 234, 237]
    if block.shape[1]>50:
        block = block[:, 0:50]

    b_block = cv2.resize(block, (50,70), interpolation=cv2.INTER_CUBIC)
    global c_count
    global c_size
    # Extract digit
    imthresh = get_tresh( b_block )
    imagem = cv2.bitwise_not(imthresh)
    contours, hierarchy = cv2.findContours(imagem,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    gray = cv2.cvtColor(b_block, cv2.COLOR_BGR2GRAY)
    gray = gray[5:45,5:45]
    
    _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)


    
    # Predict
    binary_image = cv2.resize(binary_image, (30,30), interpolation=cv2.INTER_CUBIC)

    b = binary_image.reshape(-1).astype(np.float32())


    result = loaded_model.predict([b]) 
    c_count+=1
    # cv2.imwrite(f'D:/Desktop/stage/blocks/a/roi_{c_count}_{result[0]}.jpg', binary_image) 
    # print('save img')
    return result[0]
    

def predict_color(block):

    b_block = cv2.resize(block, (50,70), interpolation=cv2.INTER_CUBIC)
    digit_only = b_block[5:45,5:45]
    pixels = np.float32(digit_only.reshape(-1, 3))

    n_colors = 2
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS

    _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
    _, counts = np.unique(labels, return_counts=True)


    c_indx = 0
    for j in range(len(counts)):
        if int(palette[j][0])>175 and int(palette[j][0])<220:
            c_indx = j
    ac_indx = 0 if c_indx ==1 else 1

    blue_range = [(240,60,5),(260,85,40)]
    red_range = [(12,12,185),(70,60,210)]
    black_range = [ (0,0,0),(48,48,48)]
    yellow_range = [(55,130,235), (90,145,250)]

    color_label = ''
    b,g,r = palette[ac_indx]
    bb,bg,br = blue_range[0]
    tb,tg,tr = blue_range[1]

    if b>bb and g>bg and r>br and b<tb and g<tg and r<tr:
        color_label='blue'

    bb,bg,br = red_range[0]
    tb,tg,tr = red_range[1]
    if b>bb and g>bg and r>br and b<tb and g<tg and r<tr:
        color_label='red'
    
    bb,bg,br = black_range[0]
    tb,tg,tr = black_range[1]
    if b>bb and g>bg and r>br and b<tb and g<tg and r<tr:
        color_label='black'

    bb,bg,br = yellow_range[0]
    tb,tg,tr = yellow_range[1]
    if b>bb and g>bg and r>br and b<tb and g<tg and r<tr:
        color_label='yellow'
    
    # start = (4, 0)
    # end = (8,30)
    # digit_only = cv2.rectangle(digit_only, start,end,(int(palette[ac_indx][0]),int(palette[ac_indx][1]),int(palette[ac_indx][2])), -1)
    
    # start = (0, 0)
    # end = (2,30)
    # digit_only = cv2.rectangle(digit_only, start,end,(int(palette[0][0]),int(palette[0][1]),int(palette[0][2])), -1)

    # start = (2, 0)
    # end = (4,30)
    # digit_only = cv2.rectangle(digit_only, start,end,(int(palette[1][0]),int(palette[1][1]),int(palette[1][2])), -1)

    # if color_label == "":
    #     cv2.imshow(':)',digit_only)
    #     cv2.waitKey(0)
    return color_label

def get_tresh(im):
	hsv_img = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
	COLOR_MIN = np.array([136, 133, 124],np.uint8)
	COLOR_MAX = np.array([236, 234, 237],np.uint8)
	frame_threshed = cv2.inRange(im, COLOR_MIN, COLOR_MAX)
	ret,thresh = cv2.threshold(frame_threshed,127,255,0)
	blur = cv2.blur(thresh,(5,5))
	contours, hierarchy = cv2.findContours(blur,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	return thresh