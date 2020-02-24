import pytesseract
from PIL import Image
import glob
import cv2
import numpy as np
import os
import shutil
import csv


def find_names_and_save():
    with open("all_ral_names.txt") as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    print(content)
    path = 'C:\\Users\\AhmetBerk\\Desktop\\all_process\\all_classes\\'
    for filename in glob.glob('C:\\Users\\AhmetBerk\\Desktop\\all_process\\real_frames/*.png'): #assuming gif
        img = cv2.imread(filename,0)
        img_name = cv2.resize(img,(1200,900),fx=5,fy=5)
        img_rect = img_name
        ret, img_name = cv2.threshold(img_name,160,255,cv2.THRESH_BINARY)
        ret, img_rect = cv2.threshold(img_rect,155,255,cv2.THRESH_BINARY)
        kernel = np.ones((3,3),np.uint8)
        img_rect = cv2.dilate(img_rect, kernel, iterations=1)
        #find_rects(img_rect)
        #img = cv2.dilate(thresh1,kernel,iterations = 1)
        #cv2.imshow("dilation",img)
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        text = pytesseract.image_to_string(img_name, lang='eng', config='--psm 6')
        index = text.find("RAL")
        ralname=text[index:index+8]
        print(ralname)
        #cv2.imshow("dilation",img_name)
        #cv2.waitKey(0)
        # Create target Directory if don't exist
        if not os.path.exists(path+ralname) and ralname in content:
            os.mkdir(path+ralname)
            shutil.move(filename, path + ralname)
            print("Directory ", ralname, " Created ")
        elif os.path.exists(path+ralname) and ralname in content:
            shutil.move(filename,path+ralname)
        elif not ralname in content and not os.path.exists(path+"Undentified"):
            os.mkdir(path+"Undentified")
            print("Directory  Undentified Created ")
            shutil.move(filename, path + "Undentified")
        elif not ralname in content and os.path.exists(path+"Undentified"):
            shutil.move(filename,path+"Undentified")


def find_rgb_values():

    path = 'C:\\Users\\AhmetBerk\\Desktop\\all_process\\all_classes'
    for root, dirs, files in os.walk(path):
        for name in files:
            square_list = []
            rect_list = []
            dirname = root.split(os.path.sep)[-1]
            print(dirname)
            fullname=root+"\\"+name
            img = cv2.imread(root+"\\"+name,cv2.IMREAD_GRAYSCALE)
            #img = cv2.resize(img, (800, 600))
            _, threshold = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
            cv2.imshow("Points", threshold)
            contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for i,cnt in enumerate(contours):
                approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
                #cv2.drawContours(img, [approx], 0, (0, 0, 0), 2)
                x = approx.ravel()[0]
                y = approx.ravel()[1]
                if len(approx) == 4 and cv2.contourArea(cnt) > 100:
                    x, y, w, h = cv2.boundingRect(approx)
                    aspectRatio = float(w) / h
                    if aspectRatio >= 0.90 and aspectRatio <= 1.05:
                        cv2.putText(img, "Square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
                        square_list.append(cnt)
                        #print(aspectRatio)
                    if aspectRatio >= 1.60 and aspectRatio <= 2.00 and cv2.contourArea(cnt)>10000:
                        cv2.putText(img, "Rect", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
                        rect_list.append(cnt)
                        print(aspectRatio)
                #cv2.imshow("threshold1", img)
            square_list=get_small_squares(square_list)
            rect_list=get_small_rectangle(rect_list)
            get_rgb_and_save(square_list,rect_list,fullname,dirname)
            print(len(square_list))
            print(len(rect_list))
            #cv2.waitKey(0)


def get_small_squares(square_list):
    for i in range(len(square_list)):
        for j in range(0, len(square_list) - i - 1):
            if cv2.contourArea(square_list[j]) > cv2.contourArea(square_list[j + 1]):
                square_list[j], square_list[j + 1] = square_list[j + 1], square_list[j]
    small_squares= []
    for i in range(4):
        small_squares.append(square_list[i])
    return small_squares


def get_small_rectangle(rect_list):
    small_rectangle = []
    if cv2.contourArea(rect_list[0])>cv2.contourArea(rect_list[1]):
        small_rectangle.append(rect_list[1])
    else:
        small_rectangle.append(rect_list[0])
    return small_rectangle

def get_rgb_and_save(square_list, rect_list, fullname,dirname):
    img = cv2.imread(fullname, 1)
    values = []
    for rect in rect_list:
        x, y, w, h = cv2.boundingRect(rect)
        print(x,y,w,h)
        start_x =int(x + (w/20))
        stop_x =int( x + ((9*w)/10))
        start_y =int(y + (h/6))
        stop_y =int(y + ((3*h)/4))
        red=0
        green=0
        blue=0
        count = 0
        cv2.putText(img, ".", (start_x, stop_y), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0))
        cv2.putText(img, ".", (start_x, start_y), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0))
        cv2.putText(img, ".", (stop_x, start_y), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0))
        cv2.putText(img, ".", (stop_x, stop_y), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0))
        for i in range(start_x,stop_x):
            for j in range(start_y,stop_y):
                count+=1
                t_blue, t_green, t_red= img[i][j]
                red+=t_red
                green+=t_green
                blue+=t_blue
        print("Rect values=",int(red/count),int(green/count),int(blue/count),count)
        values.append(int(red/count))
        values.append(int(green / count))
        values.append(int(blue / count))
    count = 0
    red = 0
    green = 0
    blue = 0
    for square in square_list:
        x, y, w, h = cv2.boundingRect(square)
        start_x = x
        stop_x =int(x+(4*w/5))
        start_y = int(y + (h / 10))
        stop_y = int(y + ((18 * h) / 20))
        cv2.putText(img, ".", (start_x, stop_y), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0))
        cv2.putText(img, ".", (start_x, start_y), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0))
        cv2.putText(img, ".", (stop_x, start_y), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0))
        cv2.putText(img, ".", (stop_x, stop_y), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0))
        for i in range(start_x,stop_x):
            for j in range(start_y,stop_y):
                count+=1
                t_blue, t_green, t_red= img[j][i]
                red+=t_red
                green+=t_green
                blue+=t_blue
    print("Average square values=" , int(red / count), int(green / count), int(blue / count), count)
    values.append(int(red / count))
    values.append(int(green / count))
    values.append(int(blue / count))
    values.append(dirname)
    cv2.imshow("Points", img)
    with open(r'name.csv', 'a',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(values)

    #cv2.waitKey(0)
find_names_and_save()
find_rgb_values()





