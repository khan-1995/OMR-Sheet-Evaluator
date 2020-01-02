from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2




#ANSWER_KEY = {0: 4, 1: 3, 2: 3, 3: 3, 4: 1, 5: 1, 6: 4,7: 0, 8: 3, 9: 1, 10: 1, 11: 1, 12: 2, 13: 3, 14: 4}


def getAnswers(x, y, h, w, coords):

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
                    help="path to the input image")
    args = vars(ap.parse_args())
    image = cv2.imread(args["image"])

    scale_percent = 100

    width = int(w * scale_percent / 100)
    height = int(h * scale_percent / 100)
    dim = (width, height)
    # 233,629,1053,1885
    y = y  # 2153
    x = x  # 195
    h = h  # 1029
    w = w  # 450
    crooped = image[y:y+h, x:x+w]
    resized = cv2.resize(crooped, dim, interpolation=cv2.INTER_AREA)

    cv2.imshow("paper", resized)
    cv2.waitKey(0)

    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)


    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    docCnt = None


    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
      

        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            

            if len(approx) == 4: 
               print("corners found")
               docCnt = approx
               break
           
          
    # coords = [(37, 16), (564, 9), (550, 1371), (37, 1365)]
    coords = coords  # [(1, 1), (352, 1), (354, 293), (1, 293)]
    pts = np.array(eval("coords"), dtype="float32")
    paper = four_point_transform(resized, pts)  # docCnt.reshape(4, 2)
    warped = four_point_transform(gray, pts)
    thresh = cv2.threshold(warped, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    questionCnts = []
    attempted = []
    
    
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        # print("x :"+str(x))
        # print("w :"+str(w))
        # print("h :"+str(h))
        # print("ar :"+str(ar))
        if w >= 20 and h >= 20 and ar >= 0.9 and ar <= 1.1:
            # cv2.drawContours(paper, [c], -1, (0, 255, 0), 3)
            cv2.drawContours(paper, [c], -1, (0, 255, 0), 3)
            questionCnts.append(c)
            
            
    
    questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]
    print("qusetions "+str(len(questionCnts)))

    print("spread :"+str(len(np.arange(0, len(questionCnts), 4))))
    
    for (q, i) in enumerate(np.arange(0, len(questionCnts), 4)):
        cnts = contours.sort_contours(questionCnts[i:i + 4])[0]
        bubbled = None
        
        for (j, c) in enumerate(cnts):
            mask = np.zeros(thresh.shape, dtype="uint8")
            cv2.drawContours(mask, [c], -1, 255, -1)
            mask = cv2.bitwise_and(thresh, thresh, mask=mask)
            total = cv2.countNonZero(mask)
            
            if bubbled is None or total > bubbled[0]:
                print("total : "+str(total))
                bubbled = (total, j)           
        print("question no: "+str(q+1)+" your answer :"+str(bubbled[1]+1))
        attempted.append(bubbled[1]+1)            
    
    return attempted       


#sections = 5
#for x in range(sections):
i=0
j=0

print(getAnswers(109+(i*205), 1222+(j*127), 128, 205, [(68, 0), (203, 0), (201, 125), (68, 125)]))
#increment by 270 to move x-axis
