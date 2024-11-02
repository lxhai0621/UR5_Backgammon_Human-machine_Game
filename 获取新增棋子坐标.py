import time
import cv2
import numpy as np
import threading

class Check:
    def __init__(self,type):
        self.camera = cv2.VideoCapture(1)
        self.length1 = 30.67
        self.length2 = 32.5
        self.top_x = 98
        self.top_y = 46
        self.type = type
        self.new_piece = [7,7]

        thread1 = threading.Thread(target=self.serch_vertex, daemon=True)
        thread1.start()
        thread1.join(6)
        self.thread2 = threading.Thread(target=self.serch_white, daemon=True)
        if type == 0:
            self.thread2.start()
        self.thread3 = threading.Thread(target=self.serch_black, daemon=True)
        if type == 1:
            self.thread3.start()

    def getlength(self):

        return self.length1, self.length2

    def serch_vertex(self):
        while True:
            (grabbed, img) = self.camera.read()
            time.sleep(3)
            (grabbed, img) = self.camera.read()
            if grabbed:
                img = img[0:540, 60:600]
                img = cv2.flip(img, -1)
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                adaptive_threshold_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,7, 7)
                blur = cv2.GaussianBlur(adaptive_threshold_img, (7, 7), 0)
                edges = cv2.Canny(image=blur, threshold1=100, threshold2=300)
                circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, minDist=15, param1=5,param2=10,minRadius=4,maxRadius=8)
                circles = np.uint16(np.around(circles))
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                top_pieces = []
                for i in circles[0, :]:
                    color = gray[i[1], i[0]]
                    if (color < 100):
                        cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
                        cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)
                        piece_info = [i[0], i[1]]
                        top_pieces.append(piece_info)
                top_pieces = sorted(top_pieces, key=lambda x: sum(x))
                if len(top_pieces) >= 4:
                    x1, y1 = top_pieces[0]
                    x2, y2 = top_pieces[3]
                    self.top_x = x1
                    self.top_y = y1
                    length1 = round((x2-x1)/12,2)
                    length2 = round((y2-y1)/12,2)
                    self.length1 = length1
                    self.length2 = length2
                print(self.length1,self.length2,self.top_x,self.top_y)
                cv2.imshow('circle1', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    #     # if self.type == 0:
    #     #     self.serch_white()
    #     # if self.type == 1:
    #     #     self.serch_black()

    def switch(self,pieces):
        arr = []
        for i in pieces:
            arr.append(tuple(i))
        mySet = set(arr)
        return mySet

    def serch_white(self):
        old_list = []
        while True:
            (grabbed, img) = self.camera.read()
            time.sleep(5)
            (grabbed, img) = self.camera.read()
            if grabbed:
                img = img[0:540, 60:600]
                img = cv2.flip(img, -1)
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                adaptive_threshold_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,7, 7)
                blur = cv2.GaussianBlur(adaptive_threshold_img, (7, 7), 0)
                edges = cv2.Canny(image=blur, threshold1=100, threshold2=300)
                circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, minDist=15, param1=7, param2=22, minRadius=12,maxRadius=18)
                if circles is not None:
                    circles = np.uint16(np.around(circles))
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    white_pieces = []
                    for i in circles[0, :]:
                        color = gray[i[1], i[0]]
                        if (color > 100):
                            cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
                            cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)
                            print(i[0])
                            print(i[1])
                            piece_info = [round((i[0]-self.top_x)/self.length1),round ((i[1]-self.top_y)/self.length2)]  # 存储圆心的x、y坐标和半径
                            if piece_info not in white_pieces:
                                white_pieces.append(piece_info)
                    white_set = self.switch(white_pieces)
                    old_set = self.switch(old_list)
                    self.new_piece = list(white_set-old_set)
                    self.new_piece = [num for tup in self.new_piece for num in tup]
                    if self.new_piece:
                        print(self.new_piece)
                    else:
                        print("没有新增的棋子")
                    if len(white_pieces)>= len(old_list):
                        old_list = white_pieces
                    #print(white_pieces)
                    cv2.imshow('circle2', img)
                else:
                    print("没有检测到棋子")
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    def serch_black(self):
        old_list = []
        print("111")
        while True:
            (grabbed, img) = self.camera.read()
            time.sleep(5)
            (grabbed, img) = self.camera.read()
            if grabbed:
                img = img[0:540, 60:600]
                img = cv2.flip(img, -1)
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                adaptive_threshold_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,7, 7)
                blur = cv2.GaussianBlur(adaptive_threshold_img, (7, 7), 0)
                edges = cv2.Canny(image=blur, threshold1=100, threshold2=300)
                circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, minDist=15, param1=7, param2=22, minRadius=12,maxRadius=18)
                if circles is not None:
                    circles = np.uint16(np.around(circles))
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    black_pieces = []
                    for i in circles[0, :]:
                        color = gray[i[1], i[0]]
                        if (color < 100):
                            cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
                            cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)
                            piece_info = [round((i[0]-self.top_x)/self.length1),round ((i[1]-self.top_y)/self.length2)]  # 存储圆心的x、y坐标和半径
                            if piece_info not in black_pieces:
                                black_pieces.append(piece_info)
                    black_set = self.switch(black_pieces)
                    old_set = self.switch(old_list)
                    self.new_piece = list(black_set-old_set)
                    if self.new_piece:
                        print(self.new_piece)
                    else:
                        print("没有新增的棋子")
                    if len(black_pieces)>= len(old_list):
                        old_list = black_pieces
                    #print(white_pieces)
                    cv2.imshow('circle2', img)
                else:
                    print("没有检测到棋子")
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

if __name__ == '__main__':
    type = 0
    chack1 = Check(type)
    while True:
        length1, length2 = chack1.getlength()
        #print(mouse_x,mouse_y)

