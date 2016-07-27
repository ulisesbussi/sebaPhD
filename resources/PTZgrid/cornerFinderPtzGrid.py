# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 13:34:13 2016

@author: sebalander
"""




# %%
import cv2
import numpy as np
import matplotlib.pyplot as plt

# %%
# input
# 6x9 chessboard
#imageFile = "./resources/fishChessboard/Screenshot from fishSeba.mp4 - 12.png"

# 8x11 A4 shetts chessboard
imageFile = "ptz_(0.850278, -0.014444, 0.0).jpg"
cornersIniFile = "./PTZgridImageInitialConditions.txt"

# output
cornersFile = "ptzCorners.npy"
patternFile = "ptzChessPattern.npy"
imgShapeFile = "ptzImgShape.npy"

# load
# corners set by hand, read as (n,1,2) size
# must format as float32
cornersIni = np.array([[crnr] for crnr in np.loadtxt(cornersIniFile)],
                       dtype='float32')
img = cv2.imread(imageFile, cv2.IMREAD_GRAYSCALE)
imgCol = cv2.imread(imageFile)

# %% BINARIZE IMAGE 
# see http://docs.opencv.org/3.0.0/d7/d4d/tutorial_py_thresholding.html
th = cv2.adaptiveThreshold(img,
                            255,
                            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                            cv2.THRESH_BINARY,
                            501,
                            0)

# haceomos un close para sacar manchas
kernel = np.ones((5,5),np.uint8)
closed = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel)

plt.imshow(th)
plt.imshow(closed)
plt.imshow(imgCol)
plt.plot(cornersIni[:,0,0],cornersIni[:,0,1],'ow')

# %% FIND CORNERS (NOT WORKING)
# cantidad esquinas internas del tablero:
# los cuadraditos del chessboard-1
pattW = 8  # width 
pattH = 11  # height
patternSize = (pattW, pattH)

found, corners = cv2.findChessboardCorners(th, patternSize);

# %% refine corners

# criterio de finalizacion de cornerSubPix
subpixCriteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, # termination criteria type
            300, # max number of iterations
            0.01) # min accuracy

corners = np.copy(cornersIni)

cv2.cornerSubPix(closed,
                 corners,
                 (15, 15),
                 (5, 5),
                 subpixCriteria);


plt.imshow(imgCol[:,:,[2,1,0]])
plt.plot(cornersIni[:,0,0],cornersIni[:,0,1],'ow')
plt.plot(corners[:,0,0],corners[:,0,1],'xg')

# %%
#Arrays para pts del objeto y pts de imagen para from all the images.
objpoints = [] #3d points in real world
imgpoints = [] #2d points in image plane





# Se arma un vector con la identificacion de cada cuadrito
# La dimensión de este vector es diferente al que se usa en la calibracion
# de la PTZ, es necesaria una dimension mas para que corra el calibrate
chessboardModel = np.zeros((1,pattH*pattW,3), np.float32)
chessboardModel[0, :, :2] = np.mgrid[0:pattW, 0:pattH].T.reshape(-1, 2) #rellena las columnas 1 y 2


# %% SAVE DATA POINTS
np.save(cornersFile, imgpoints)
np.save(patternFile, chessboardModel)
np.save(imgShapeFile, img.shape)
