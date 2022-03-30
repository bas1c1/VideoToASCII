import sys, random, argparse
import numpy as np
import math
from PIL import Image
import numpy as np
import cv2
import time
import os
from numba import njit, prange

gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
gscale2 = '@%#*+=-:. '

def getAverageL(image):
    im = np.array(image)
    w,h = im.shape

    return np.average(im.reshape(w*h))

def covertImageToAscii(fileName, cols, scale, moreLevels):
    global gscale1, gscale2

    image = Image.open(fileName).convert('L')
    W, H = image.size[0], image.size[1]
    w = W/cols
    h = w/scale

    rows = int(H/h)

    if cols > W or rows > H:
        # print("Image too small for specified cols!")
        exit()

    aimg = []

    for j in prange(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)

        if j == rows-1:
            y2 = H

        aimg.append("")
        for i in prange(cols):
            x1 = int(i*w)
            x2 = int((i+1)*w)

            if i == cols-1:
                x2 = W

            img = image.crop((x1, y1, x2, y2))
            avg = int(getAverageL(img))

            if moreLevels:
                gsval = gscale1[int((avg*69)/255)]

            else:
                gsval = gscale2[int((avg*9)/255)]

            aimg[j] += gsval

    return aimg

def start_convert(fname, vcols, mor):
    imgFile = fname
    scale = 1 # or 0.43
    cols = vcols

    aimg = covertImageToAscii(imgFile, cols, scale, mor)

    for row in aimg:
        print(row)

fileorcamera = input("Веб-камера или видео-файл (введите 0 или 1): ")
mor = bool(int(input("Уровень вывода ASCII (0 или 1, рекомендуется 0): ")))

cols = int(input("Введите размер картинки (рекомендуется 60): "))

if fileorcamera == "0":
    fileorcamera = 0
elif fileorcamera == "1":
    fileorcamera = input("Введите имя файла: ")

cap = cv2.VideoCapture(fileorcamera)
 
i = 0

while (True):
    i += 1
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("1" + ".jpg", gray)
    os.system("cls")
    start_convert("1" + ".jpg", cols, mor)