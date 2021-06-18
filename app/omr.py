import cv2
import numpy as np 


def getCornerPoints( cont):
        per = cv2.arcLength(cont,True)
        approx = cv2.approxPolyDP(cont,0.02*per,True)
        return approx

def reorder( myPoints):
        myPoints = myPoints.reshape((4,2))
        myPointsnew = np.zeros((4,1,2),np.int32)
        add = myPoints.sum(1)
        myPointsnew[0] = myPoints[np.argmin(add)]
        myPointsnew[3] = myPoints[np.argmax(add)]
        diff = np.diff(myPoints,axis=1)
        myPointsnew[1] = myPoints[np.argmin(diff)]
        myPointsnew[2] = myPoints[np.argmax(diff)]
        return myPointsnew

def splitBoxes( img,noRow,noCol):
        imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        rows = np.vsplit(imgGray,noRow)
        #cv2.imshow("split",rows[0])
        boxes = []
        for r in rows:
            cols = np.hsplit(r,noCol)
            for box in cols:
                boxes.append(box)
                #cv2.imshow("box",box)
        return boxes

def matrix( box,n_row,n_cols):
        matrix = np.zeros((n_row,n_cols))
        countR = 0
        countC = 0
        for images in box:
            totalpixels = cv2.countNonZero(images)
            matrix[countR][countC] = int(totalpixels)
            countC +=1
            if countC == n_cols:
                countR +=1
                countC = 0
        matrix = matrix.astype(int)        
        return matrix   


def answer( img,a1,b1,a2,b2):
        pts1 = np.float32([[a1,b1],[a2,b1],[a1,b2],[a2,b2]])
        pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])
        matrix1= cv2.getPerspectiveTransform(pts1,pts2)
        imgwarp = cv2.warpPerspective(img,matrix1,(300,300))
        #cv2.imshow("imgwarp",imgwarp)

        #imggray = cv2.cvtColor(imgwarp,cv2.COLOR_BGR2GRAY)
        #cv2.imshow("imggray",imggray)
        imgthresh = cv2.threshold(imgwarp,240,100,cv2.THRESH_BINARY)[1]
        #cv2.imshow("imgthresh",imgthresh) 
        return imgthresh

def answer_matrix( qus_matrix,n_row,n_cols,val):
        ans_matrix = np.zeros((n_row,n_cols))
        for i in range(n_row):
            for j in range(n_cols):
                if(qus_matrix[i][j]<val):
                    ans_matrix[i][j] = 1
                else:
                    ans_matrix[i][j] = 0   
        
        ans_matrix = ans_matrix.astype(int)   
        return ans_matrix           
class Omr:
    def main(self, path):
            img = cv2.imread(path)

            heightImg = 700
            widthImg  = 700

            #PREPROCESSING
            img = cv2.resize(img,(widthImg,heightImg))
            imgContours = img.copy()
            imgBiggestContours = img.copy()
            imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            imgBlur = cv2.GaussianBlur(imgGray,(5,5),1) 
            imgCanny = cv2.Canny(imgBlur,20,50)

            #finding biggest contours
            contours, hierarchy = cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
            rectcon = []
            for cnt in contours:
                area = cv2.contourArea(cnt)
                
                if area > 20000:
                    per = cv2.arcLength(cnt,True)
                    approx = cv2.approxPolyDP(cnt,0.02*per,True)
                    if len(approx)==4:
                        rectcon.append(cnt)
                    cv2.drawContours(imgContours,cnt,-1,(255,0,0),10)
            rectcon = sorted(rectcon,key=cv2.contourArea,reverse=True)
            biggestContour1 = getCornerPoints(rectcon[0]) 
            biggestContour2 = getCornerPoints(rectcon[1]) 
            biggestContour3 = getCornerPoints(rectcon[2]) 
            if (biggestContour1.size !=0 and biggestContour2.size != 0 and biggestContour3.size != 0):
                cv2.drawContours(imgBiggestContours,biggestContour1,-1,(255,0,0),10)
                cv2.drawContours(imgBiggestContours,biggestContour2,-1,(0,255,0),10)
                cv2.drawContours(imgBiggestContours,biggestContour3,-1,(0,0,255),10)

                biggestContour1=reorder(biggestContour1)
                biggestContour2=reorder(biggestContour2)
                biggestContour3=reorder(biggestContour3)
                
                pts11 = np.float32(biggestContour1)
                pts21 = np.float32([[0,0],[300,0],[0,200],[300,200]])
                matrix1 = cv2.getPerspectiveTransform(pts11,pts21)
                details = cv2.warpPerspective(img,matrix1,(300,200))
                #cv2.imshow("details",details)
                
                pts21 = np.float32(biggestContour2)
                pts22 = np.float32([[0,0],[400,0],[0,300],[400,300]])
                matrix2 = cv2.getPerspectiveTransform(pts21,pts22)
                answer2 = cv2.warpPerspective(img,matrix2,(400,300))
                #cv2.imshow("answer2",answer2)

                pts31 = np.float32(biggestContour3)
                pts32 = np.float32([[0,0],[300,0],[0,300],[300,300]])
                matrix3 = cv2.getPerspectiveTransform(pts31,pts32)
                answer1 = cv2.warpPerspective(img,matrix3,(300,300))
                #cv2.imshow("answer1",answer1)
                
                pts1 = np.float32([[16,48],[179,48],[16,192],[179,192]])
                pts2 = np.float32([[0,0],[250,0],[0,350],[250,350]])
                matrix1_roll = cv2.getPerspectiveTransform(pts1,pts2)
                imgrollnumber = cv2.warpPerspective(details,matrix1_roll,(250,350))
                #cv2.imshow("rollnumber",imgrollnumber)

                imgrollnumbergray = cv2.cvtColor(imgrollnumber,cv2.COLOR_BGR2GRAY)
                #cv2.imshow("rollhgray",imgrollnumbergray)
                imgrollnumberthresh = cv2.threshold(imgrollnumber,240,100,cv2.THRESH_BINARY)[1]
                #cv2.imshow("rollthresh",imgrollnumberthresh)

                boxes = splitBoxes(imgrollnumberthresh,10,10) 
                rollnumber_matrix = matrix(boxes,10,10)


                pts1 = np.float32([[206,48],[288,48],[206,192],[288,192]])
                pts2 = np.float32([[0,0],[250,0],[0,350],[250,350]])
                matrix1_roll = cv2.getPerspectiveTransform(pts1,pts2)
                imgtestid = cv2.warpPerspective(details,matrix1_roll,(250,350))
                #cv2.imshow("testid",imgtestid)

                imgtestidgray = cv2.cvtColor(imgtestid,cv2.COLOR_BGR2GRAY)
                #cv2.imshow("rollhgray",imgtestidgray)
                imgtestidthresh = cv2.threshold(imgtestid,240,100,cv2.THRESH_BINARY)[1]
                #cv2.imshow("testidthresh",imgtestidthresh)
                

                boxes = splitBoxes(imgtestidthresh,10,5)
                testid_matrix = matrix(boxes,10,5)


                imgans1_5 = answer(answer1,28,73,117,284)
                ans1_5_box = splitBoxes(imgans1_5,5,4)
                ans1_5_matrix = matrix(ans1_5_box,5,4)

                imgans6_10 = answer(answer1,179,73,267,284)
                ans6_10_box = splitBoxes(imgans6_10,5,4)
                ans6_10_matrix = matrix(ans6_10_box,5,4)

                imgans_11_12 = answer(answer2,11,98,63,252)
                ans11_12_box = splitBoxes(imgans_11_12,2,4)
                ans11_12_matrix = matrix(ans11_12_box,2,4)

                imgans_13_14 = answer(answer2,94,98,144,252)
                ans13_14_box = splitBoxes(imgans_13_14,2,4)
                ans13_14_matrix = matrix(ans13_14_box,2,4)

                imgans_15_16 = answer(answer2,177,98,224,252)
                ans15_16_box = splitBoxes(imgans_15_16,2,4)
                ans15_16_matrix = matrix(ans15_16_box,2,4)

                imgans_17_18 = answer(answer2,258,98,306,252)
                ans17_18_box = splitBoxes(imgans_17_18,2,4)
                ans17_18_matrix = matrix(ans17_18_box,2,4)

                imgans_19_20 = answer(answer2,337,98,383,252)
                ans19_20_box = splitBoxes(imgans_19_20,2,4)
                ans19_20_matrix = matrix(ans19_20_box,2,4)

            

                rollnumber = answer_matrix(rollnumber_matrix,10,10,500)
                testid = answer_matrix(testid_matrix,10,5,1000)
                ans1_5 = answer_matrix(ans1_5_matrix,5,4,3250)
                ans6_10 = answer_matrix(ans6_10_matrix,5,4,3250)
                ans11_12 = answer_matrix(ans11_12_matrix,2,4,8000)
                ans13_14 = answer_matrix(ans13_14_matrix,2,4,8000)
                ans15_16 = answer_matrix(ans15_16_matrix,2,4,8000)
                ans17_18 = answer_matrix(ans17_18_matrix,2,4,8000)
                ans19_20 = answer_matrix(ans19_20_matrix,2,4,8000)

                ans1 = ans1_5[0,:]
                ans2 = ans1_5[1,:]
                ans3 = ans1_5[2,:]
                ans4 = ans1_5[3,:]
                ans5 = ans1_5[4,:]
                ans6 = ans6_10[0,:]
                ans7 = ans6_10[1,:]
                ans8 = ans6_10[2,:]
                ans9 = ans6_10[3,:]
                ans10 = ans6_10[4,:]
                ans11 = ans11_12[0,:]
                ans12 = ans11_12[1,:]
                ans13 = ans13_14[0,:]
                ans14 = ans13_14[1,:]
                ans15 = ans15_16[0,:]
                ans16 = ans15_16[1,:]
                ans17 = ans17_18[0,:]
                ans18 = ans17_18[1,:]
                ans19 = ans19_20[0,:]
                ans20 = ans19_20[1,:]

                dicts = {"roll_number":rollnumber,"test_id":testid,1:ans1,2:ans2,3:ans3,4:ans4,5:ans5,6:ans6,7:ans7,8:ans8,9:ans9,10:ans10,11:ans11,12:ans12,13:ans13,14:ans14,15:ans15,16:ans16,17:ans17,18:ans18,19:ans19,20:ans20,}
                return dicts

OMR = Omr()