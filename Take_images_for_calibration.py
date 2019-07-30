###################################
##### Authors:                #####
##### Stephane Vujasinovic    #####
##### Frederic Uhrweiller     #####
#####                         #####
##### Creation: 2017          #####
###################################

import numpy as np
import cv2

print('Starting the Calibration. Press and maintain the space bar to exit the script\n')
print('Push (s) to save the image you want and push (c) to see next frame without saving the image')

id_image=0

# termination criteria
criteria =(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Call the two cameras
CamR= cv2.VideoCapture(0)   # 0 -> Right Camera
CamL= cv2.VideoCapture(2)   # 2 -> Left Camera

cornerImageR = 0
cornerImageL = 0

while True:
    retR, frameR= CamR.read()
    retL, frameL= CamL.read()

    cv2.imshow('imgR',frameR)
    cv2.imshow('imgL',frameL)

    if cv2.waitKey(1) & 0xFF == ord(' '):
        print('Processing Image...')
        grayR= cv2.cvtColor(frameR,cv2.COLOR_BGR2GRAY)
        grayL= cv2.cvtColor(frameL,cv2.COLOR_BGR2GRAY)

        blurGaussianR = cv2.GaussianBlur(grayR, (5,5),0)
        blurGaussianL = cv2.GaussianBlur(grayL, (5,5),0)

        # Find the chess board corners
        retR, cornersR = cv2.findChessboardCorners(blurGaussianR,(9,6),None)  # Define the number of chess corners (here 9 by 6) we are looking for with the right Camera
        retL, cornersL = cv2.findChessboardCorners(blurGaussianL,(9,6),None)  # Same with the left camera

        '''
        if (retR == True):
            cornerImageR = cornerImageR+1
            corners2R= cv2.cornerSubPix(blurGaussianR,cornersR,(11,11),(-1,-1),criteria)
            cv2.drawChessboardCorners(blurGaussianR,(9,6),corners2R,retR)
            cv2.imshow(str(cornerImageR),blurGaussianR)

        if (retL == True):
            cornerImageL = cornerImageL+1
            corners2L= cv2.cornerSubPix(blurGaussianL,cornersL,(11,11),(-1,-1),criteria)
            cv2.drawChessboardCorners(blurGaussianL,(9,6),corners2L,retL)
            cv2.imshow(str(cornerImageL),blurGaussianL)

        '''
        # If found, add object points, image points (after refining them)
        if (retR == True) & (retL == True):
            corners2R= cv2.cornerSubPix(blurGaussianR,cornersR,(11,11),(-1,-1),criteria)    # Refining the Position
            corners2L= cv2.cornerSubPix(blurGaussianL,cornersL,(11,11),(-1,-1),criteria)

            # Draw and display the corners
            cv2.drawChessboardCorners(blurGaussianR,(9,6),corners2R,retR)
            cv2.drawChessboardCorners(blurGaussianL,(9,6),corners2L,retL)
            cv2.imshow('VideoR',blurGaussianR)
            cv2.imshow('VideoL',blurGaussianL)


            if cv2.waitKey(0) & 0xFF == ord('s'):   # Push "s" to save the images and "c" if you don't want to
                str_id_image= str(id_image)
                print('Images saved for right and left cameras')
                cv2.imwrite('chessboard-R'+str_id_image+'.png',frameR) # Save the image in the file where this Programm is located
                cv2.imwrite('chessboard-L'+str_id_image+'.png',frameL)
                id_image=id_image+1
            else:
                print('Images not saved')

    # End the Programme
    if cv2.waitKey(1) & 0xFF == ord('q'):   # Push the space bar and maintan to exit this Programm
        break

# Release the Cameras
CamR.release()
CamL.release()
cv2.destroyAllWindows()
