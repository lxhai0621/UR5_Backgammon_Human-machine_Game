import time
from enum import IntEnum
import pygame
import sys
import cv2
import numpy as np
import threading
import socket
import util
import struct

t = time.localtime()
date = str(t.tm_year) + '-' + str(t.tm_mon) + '-' + str(t.tm_mday) + ' ' + str(t.tm_hour) + ':' + str(
    t.tm_min) + ':' + str(t.tm_sec)
version = 'FiveChessV1.0  time:' + date

# 基础参数设置
square_size = 40  # 单格的宽度（不是格数！是为了方便绘制棋盘用的变量
chess_size = square_size // 2 - 2  # 棋子大小
web_broad = 15  # 棋盘格数+1（nxn）
map_w = web_broad * square_size  # 棋盘长度
map_h = web_broad * square_size  # 棋盘高度
info_w = 60  # 按钮界面宽度
button_w = 120  # 按钮长宽
button_h = 45
screen_w = map_w  # 总窗口长宽
screen_h = map_h + info_w
HOST = "192.168.1.206"
#HOST = "192.168.1.128"
PORT = 30003
X1 = -0.59690
Y1 = -0.15322
X2 = -0.30469
Y2 = 0.12294
mov_x1 = -0.250
mov_x2 = -0.250
mov_x3 = -0.250
mov_x4 = -0.250
mov_x5 = -0.250
flag = 0

# 检测棋子位置

class Check:
    def __init__(self,type):
        self.camera = cv2.VideoCapture(1)
        self.length1 = 29.33
        self.length2 = 34.0
        self.top_x = 122
        self.top_y = 46
        self.type = type
        self.new_piece = 0
        thread2 = threading.Thread(target=self.serch_white, daemon=True)
        if type == 0:
            thread2.start()
        thread3 = threading.Thread(target=self.serch_black, daemon=True)
        if type == 1:
            thread3.start()

    def getlength(self):
        return self.length1, self.length2


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
            time.sleep(2)
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
                            piece_info = [round((i[0]-self.top_x)/self.length1),round ((i[1]-self.top_y)/self.length2)]
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
                    cv2.imshow('circle2', img)
                else:
                    print("没有检测到棋子")
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    def serch_black(self):
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
                        if (color < 100):
                            cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
                            cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)
                            piece_info = [round((i[0]-self.top_x)/self.length1),round ((i[1]-self.top_y)/self.length2)]  # 存储圆心的x、y坐标和半径
                            if piece_info not in white_pieces:
                                white_pieces.append(piece_info)
                    white_set = self.switch(white_pieces)
                    old_set = self.switch(old_list)
                    self.new_piece = list(white_set-old_set)
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

# 地图绘制模块

class MAP_ENUM(IntEnum):  # 用数字表示当前格的情况
    be_empty = 0,  # 无人下
    player1 = 1,  # 玩家一，执白
    player2 = 2,  # 玩家二，执黑
    out_of_range = 3,  # 出界


class Map:  # 地图类
    def __init__(self, width, height):  # 构造函数
        self.width = width
        self.height = height
        self.map = [[0 for x in range(self.width)] for y in range(self.height)]  # 存储棋盘的二维数组
        self.steps = []  # 记录步骤先后

    def get_init(self):  # 重置棋盘
        for y in range(self.height):
            for x in range(self.width):
                self.map[y][x] = 0
        self.steps = []

    def intoNextTurn(self, turn):  # 进入下一回合，交换下棋人
        if turn == MAP_ENUM.player1:
            return MAP_ENUM.player2
        else:
            return MAP_ENUM.player1

    def getLocate(self, x, y):  # 输入下标，返回具体位置
        map_x = x * square_size
        map_y = y * square_size
        return (map_x, map_y, square_size, square_size)  # 返回位置信息

    def getIndex(self, map_x, map_y):  # 输入具体位置，返回下标
        x = map_x // square_size
        y = map_y // square_size
        return (x, y)

    def isInside(self, map_x, map_y):  # 是否在有效范围内
        if (map_x <= 0 or map_x >= map_w or
                map_y <= 0 or map_y >= map_h):
            return False
        return True

    def isEmpty(self, x, y):  # 当前格子是否已经有棋子
        return (self.map[y][x] == 0)

    def click(self, x, y, type):  # 点击的下棋动作
        self.map[y][x] = type.value  # 下棋
        self.steps.append((x, y))  # 记录步骤信息

    def printChessPiece(self, screen):  # 绘制棋子
        player_one = (255, 245, 238)  # 象牙白
        player_two = (41, 36, 33)  # 烟灰
        player_color = [player_one, player_two]
        for i in range(len(self.steps)):
            x, y = self.steps[i]
            map_x, map_y, width, height = self.getLocate(x, y)
            pos, radius = (map_x + width // 2, map_y + height // 2), chess_size
            turn = self.map[y][x]
            pygame.draw.circle(screen, player_color[turn - 1], pos, radius)  # 画棋子

    def drawBoard(self, screen):  # 画棋盘
        color = (0, 0, 0)  # 线色
        for y in range(self.height):
            # 画横着的棋盘线
            start_pos, end_pos = (square_size // 2, square_size // 2 + square_size * y), (
                map_w - square_size // 2, square_size // 2 + square_size * y)
            pygame.draw.line(screen, color, start_pos, end_pos, 1)
        for x in range(self.width):
            # 画竖着的棋盘线
            start_pos, end_pos = (square_size // 2 + square_size * x, square_size // 2), (
                square_size // 2 + square_size * x, map_h - square_size // 2)
            pygame.draw.line(screen, color, start_pos, end_pos, 1)


# 高级AI模块

class SITUATION(IntEnum):  # 棋型
    NONE = 0,  # 无
    SLEEP_TWO = 1,  # 眠二
    LIVE_TWO = 2,  # 活二
    SLEEP_THREE = 3,  # 眠三
    LIVE_THREE = 4,  # 活三
    CHONG_FOUR = 5,  # 冲四
    LIVE_FOUR = 6,  # 活四
    LIVE_FIVE = 7,  # 活五


SITUATION_NUM = 8  # 长度


FIVE = SITUATION.LIVE_FIVE.value
L4, L3, L2 = SITUATION.LIVE_FOUR.value, SITUATION.LIVE_THREE.value, SITUATION.LIVE_TWO.value
S4, S3, S2 = SITUATION.CHONG_FOUR.value, SITUATION.SLEEP_THREE.value, SITUATION.SLEEP_TWO.value


class MyChessAI():
    def __init__(self, chess_len):  # 构造函数
        self.len = chess_len
        # 二维数组，每一格存的是：横评分，纵评分，左斜评分，右斜评分
        self.record = [[[0, 0, 0, 0] for i in range(chess_len)] for j in range(chess_len)]
        # 存储当前格具体棋型数量
        self.count = [[0 for i in range(SITUATION_NUM)] for j in range(2)]
        # 位置分（同条件下越靠近棋盘中央越高）
        self.position_isgreat = [
            [(web_broad - max(abs(i - web_broad / 2 + 1), abs(j - web_broad / 2 + 1))) for i in range(chess_len)]
            for j in range(chess_len)]

    def get_init(self):
        for i in range(self.len):
            for j in range(self.len):
                for k in range(4):
                    self.record[i][j][k] = 0
        for i in range(len(self.count)):
            for j in range(len(self.count[0])):
                self.count[i][j] = 0
        self.save_count = 0

    def isWin(self, board, turn):  # 当前人胜利
        return self.evaluate(board, turn, True)

    # 返回所有未下棋坐标（位置从好到坏）
    def genmove(self, board, turn):
        moves = []
        for y in range(self.len):
            for x in range(self.len):
                if board[y][x] == 0:
                    score = self.position_isgreat[y][x]
                    moves.append((score, x, y))
        moves.sort(reverse=True)
        return moves

    # 返回当前最优解下标
    def search(self, board, turn):
        moves = self.genmove(board, turn)
        bestmove = None
        max_score = -99999
        for score, x, y in moves:
            board[y][x] = turn.value
            score = self.evaluate(board, turn)
            board[y][x] = 0
            if score > max_score:
                max_score = score
                bestmove = (max_score, x, y)
        #print(bestmove[1:])
        return bestmove


    def findBestChess(self, board, turn):
        score, x, y = self.search(board, turn)
        chess = UR5(x,y)
        chess.go(x,y)
        return (x, y)


    def getScore(self, mychess, yourchess):
        mscore, oscore = 0, 0
        if mychess[FIVE] > 0:
            return (10000, 0)
        if yourchess[FIVE] > 0:
            return (0, 10000)
        if mychess[S4] >= 2:
            mychess[L4] += 1
        if yourchess[L4] > 0:
            return (0, 9050)
        if yourchess[S4] > 0:
            return (0, 9040)
        if mychess[L4] > 0:
            return (9030, 0)
        if mychess[S4] > 0 and mychess[L3] > 0:
            return (9020, 0)
        if yourchess[L3] > 0 and mychess[S4] == 0:
            return (0, 9010)
        if (mychess[L3] > 1 and yourchess[L3] == 0 and yourchess[S3] == 0):
            return (9000, 0)
        if mychess[S4] > 0:
            mscore += 2000
        if mychess[L3] > 1:
            mscore += 500
        elif mychess[L3] > 0:
            mscore += 100
        if yourchess[L3] > 1:
            oscore += 2000
        elif yourchess[L3] > 0:
            oscore += 400
        if mychess[S3] > 0:
            mscore += mychess[S3] * 10
        if yourchess[S3] > 0:
            oscore += yourchess[S3] * 10
        if mychess[L2] > 0:
            mscore += mychess[L2] * 4
        if yourchess[L2] > 0:
            oscore += yourchess[L2] * 4
        if mychess[S2] > 0:
            mscore += mychess[S2] * 4
        if yourchess[S2] > 0:
            oscore += yourchess[S2] * 4
        return (mscore, oscore)  # 自我辅助效果，counter对面效果

    # 对上述得分进行进一步处理
    def evaluate(self, board, turn, checkWin=False):
        self.get_init()
        if turn == MAP_ENUM.player1:
            me = 1
            you = 2
        else:
            me = 2
            you = 1
        for y in range(self.len):
            for x in range(self.len):
                if board[y][x] == me:
                    self.evaluatePoint(board, x, y, me, you)
                elif board[y][x] == you:
                    self.evaluatePoint(board, x, y, you, me)
        mychess = self.count[me - 1]
        yourchess = self.count[you - 1]
        if checkWin:
            return mychess[FIVE] > 0  # 检查是否已经胜利
        else:
            mscore, oscore = self.getScore(mychess, yourchess)
            return (mscore - oscore)  # 自我辅助效果，counter对面效果

    def evaluatePoint(self, board, x, y, me, you):
        direction = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 四个方向
        for i in range(4):
            if self.record[y][x][i] == 0:
                # 检查当前方向棋型
                self.getBasicSituation(board, x, y, i, direction[i], me, you, self.count[me - 1])
            else:
                self.save_count += 1

    # 把当前方向棋型存储下来，方便后续使用
    def getLine(self, board, x, y, direction, me, you):
        line = [0 for i in range(9)]
        # “光标”移到最左端
        tmp_x = x + (-5 * direction[0])
        tmp_y = y + (-5 * direction[1])
        for i in range(9):
            tmp_x += direction[0]
            tmp_y += direction[1]
            if (tmp_x < 0 or tmp_x >= self.len or tmp_y < 0 or tmp_y >= self.len):
                line[i] = you  # 出界
            else:
                line[i] = board[tmp_y][tmp_x]
        return line

    # 把当前方向的棋型识别成具体情况（如把MMMMX识别成冲四）
    def getBasicSituation(self, board, x, y, dir_index, dir, me, you, count):
        # record赋值
        def setRecord(self, x, y, left, right, dir_index, direction):
            tmp_x = x + (-5 + left) * direction[0]
            tmp_y = y + (-5 + left) * direction[1]
            for i in range(left, right):
                tmp_x += direction[0]
                tmp_y += direction[1]
                self.record[tmp_y][tmp_x][dir_index] = 1

        empty = MAP_ENUM.be_empty.value
        left_index, right_index = 4, 4
        line = self.getLine(board, x, y, dir, me, you)
        while right_index < 8:
            if line[right_index + 1] != me:
                break
            right_index += 1
        while left_index > 0:
            if line[left_index - 1] != me:
                break
            left_index -= 1
        left_range, right_range = left_index, right_index
        while right_range < 8:
            if line[right_range + 1] == you:
                break
            right_range += 1
        while left_range > 0:
            if line[left_range - 1] == you:
                break
            left_range -= 1
        chess_range = right_range - left_range + 1
        if chess_range < 5:
            setRecord(self, x, y, left_range, right_range, dir_index, dir)
            return SITUATION.NONE
        setRecord(self, x, y, left_index, right_index, dir_index, dir)
        m_range = right_index - left_index + 1
        if m_range == 5:
            count[FIVE] += 1
        # 活四冲四
        if m_range == 4:
            left_empty = right_empty = False
            if line[left_index - 1] == empty:
                left_empty = True
            if line[right_index + 1] == empty:
                right_empty = True
            if left_empty and right_empty:
                count[L4] += 1
            elif left_empty or right_empty:
                count[S4] += 1
        # 活三眠三
        if m_range == 3:
            left_empty = right_empty = False
            left_four = right_four = False
            if line[left_index - 1] == empty:
                if line[left_index - 2] == me:  # MXMMM
                    setRecord(self, x, y, left_index - 2, left_index - 1, dir_index, dir)
                    count[S4] += 1
                    left_four = True
                left_empty = True
            if line[right_index + 1] == empty:
                if line[right_index + 2] == me:  # MMMXM
                    setRecord(self, x, y, right_index + 1, right_index + 2, dir_index, dir)
                    count[S4] += 1
                    right_four = True
                right_empty = True
            if left_four or right_four:
                pass
            elif left_empty and right_empty:
                if chess_range > 5:  # XMMMXX, XXMMMX
                    count[L3] += 1
                else:  # PXMMMXP
                    count[S3] += 1
            elif left_empty or right_empty:  # PMMMX, XMMMP
                count[S3] += 1
        # 活二眠二
        if m_range == 2:
            left_empty = right_empty = False
            left_three = right_three = False
            if line[left_index - 1] == empty:
                if line[left_index - 2] == me:
                    setRecord(self, x, y, left_index - 2, left_index - 1, dir_index, dir)
                    if line[left_index - 3] == empty:
                        if line[right_index + 1] == empty:  # XMXMMX
                            count[L3] += 1
                        else:  # XMXMMP
                            count[S3] += 1
                        left_three = True
                    elif line[left_index - 3] == you:  # PMXMMX
                        if line[right_index + 1] == empty:
                            count[S3] += 1
                            left_three = True
                left_empty = True
            if line[right_index + 1] == empty:
                if line[right_index + 2] == me:
                    if line[right_index + 3] == me:  # MMXMM
                        setRecord(self, x, y, right_index + 1, right_index + 2, dir_index, dir)
                        count[S4] += 1
                        right_three = True
                    elif line[right_index + 3] == empty:
                        # setRecord(self, x, y, right_index+1, right_index+2, dir_index, dir)
                        if left_empty:  # XMMXMX
                            count[L3] += 1
                        else:  # PMMXMX
                            count[S3] += 1
                        right_three = True
                    elif left_empty:  # XMMXMP
                        count[S3] += 1
                        right_three = True
                right_empty = True
            if left_three or right_three:
                pass
            elif left_empty and right_empty:  # XMMX
                count[L2] += 1
            elif left_empty or right_empty:  # PMMX, XMMP
                count[S2] += 1
        # 特殊活二眠二（有空格
        if m_range == 1:
            left_empty = right_empty = False
            if line[left_index - 1] == empty:
                if line[left_index - 2] == me:
                    if line[left_index - 3] == empty:
                        if line[right_index + 1] == you:  # XMXMP
                            count[S2] += 1
                left_empty = True
            if line[right_index + 1] == empty:
                if line[right_index + 2] == me:
                    if line[right_index + 3] == empty:
                        if left_empty:  # XMXMX
                            count[L2] += 1
                        else:  # PMXMX
                            count[S2] += 1
                elif line[right_index + 2] == empty:
                    if line[right_index + 3] == me and line[right_index + 4] == empty:  # XMXXMX
                        count[L2] += 1
        # 以上都不是则为none棋型
        return SITUATION.NONE


# 主程序实现部分

# 控制进程按钮类（父类）
class Button:
    def __init__(self, screen, text, x, y, color, enable):  # 构造函数
        self.screen = screen
        self.width = button_w
        self.height = button_h
        self.button_color = color
        self.text_color = (255, 255, 255)  # 纯白
        self.enable = enable
        self.font = pygame.font.SysFont(None, button_h * 2 // 3)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.topleft = (x, y)
        self.text = text
        self.init_msg()

    # 重写pygame内置函数，初始化我们的按钮
    def init_msg(self):
        if self.enable:
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[0])
        else:
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[1])
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    # 根据按钮enable状态填色，具体颜色在后续子类控制
    def draw(self):
        if self.enable:
            self.screen.fill(self.button_color[0], self.rect)
        else:
            self.screen.fill(self.button_color[1], self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class WhiteStartButton(Button):  # 开始按钮（选白棋）
    def __init__(self, screen, text, x, y):  # 构造函数
        super().__init__(screen, text, x, y, [(26, 173, 25), (158, 217, 157)], True)
    def click(self, game):  # 点击，pygame内置方法
        if self.enable:  # 启动游戏并初始化，变换按钮颜色
            game.start()
            game.winner = None
            game.multiple = False
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[1])
            self.enable = False
            return True
        return False
    def unclick(self):  # 取消点击
        if not self.enable:
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[0])
            self.enable = True


class BlackStartButton(Button):  # 开始按钮（选黑棋）
    def __init__(self, screen, text, x, y):  # 构造函数
        super().__init__(screen, text, x, y, [(26, 173, 25), (158, 217, 157)], True)
    def click(self, game):  # 点击，pygame内置方法
        if self.enable:  # 启动游戏并初始化，变换按钮颜色，安排AI先手
            game.start()
            game.winner = None
            game.multiple = False
            game.useAI = True
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[1])
            self.enable = False
            return True
        return False

    def unclick(self):  # 取消点击
        if not self.enable:
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[0])
            self.enable = True


class GiveupButton(Button):  # 投降按钮（任何模式都能用
    def __init__(self, screen, text, x, y):
        super().__init__(screen, text, x, y, [(230, 67, 64), (236, 139, 137)], False)

    def click(self, game):  # 结束游戏，判断赢家
        if self.enable:
            game.is_play = False
            if game.winner is None:
                game.winner = game.map.intoNextTurn(game.player)
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[1])
            self.enable = False
            return True
        return False

    def unclick(self):  # 保持不变，填充颜色
        if not self.enable:
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[0])
            self.enable = True


class MultiStartButton(Button):  # 开始按钮（多人游戏）
    def __init__(self, screen, text, x, y):  # 构造函数
        super().__init__(screen, text, x, y, [(153, 51, 250), (221, 160, 221)], True)  # 紫色

    def click(self, game):  # 点击，pygame内置方法
        if self.enable:  # 启动游戏并初始化，变换按钮颜色
            game.start()
            game.winner = None
            game.multiple = True
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[1])
            self.enable = False
            return True
        return False

    def unclick(self):  # 取消点击
        if not self.enable:
            self.msg_image = self.font.render(self.text, True, self.text_color, self.button_color[0])
            self.enable = True


class Game:  # pygame类,以下所有功能都是根据需要重写
    def __init__(self, caption):
        # 使用pygame之前必须初始化
        pygame.init()
        self.screen = pygame.display.set_mode([screen_w, screen_h])  # 设置主屏窗口
        pygame.display.set_caption(caption)  # 设置窗口标题，即游戏名称
        self.clock = pygame.time.Clock()
        self.buttons = []
        self.buttons.append(WhiteStartButton(self.screen, 'Pick White', 10, map_h))
        self.buttons.append(BlackStartButton(self.screen, 'Pick Black', 170, map_h))
        self.buttons.append(GiveupButton(self.screen, 'Surrender', 330, map_h))
        self.buttons.append(MultiStartButton(self.screen, 'Multiple', 490, map_h))
        self.is_play = False
        self.map = Map(web_broad, web_broad)
        self.player = MAP_ENUM.player1
        self.action = None
        self.AI = MyChessAI(web_broad)
        self.useAI = False
        self.winner = None
        self.multiple = False

    def start(self):
        self.is_play = True
        self.player = MAP_ENUM.player1  # 白棋先手
        self.map.get_init()

    def play(self):
        # 画底板
        self.clock.tick(60)
        wood_color = (210, 180, 140)
        pygame.draw.rect(self.screen, wood_color, pygame.Rect(0, 0, map_w, screen_h))
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(map_w, 0, info_w, screen_h))
        # 画按钮
        for button in self.buttons:
            button.draw()
        if self.is_play and not self.isOver():
            if self.useAI and not self.multiple:
                x, y = self.AI.findBestChess(self.map.map, self.player)
                self.checkClick(x, y, True)
                self.useAI = False
            if self.action is not None:
                self.checkClick(self.action[0], self.action[1])
                self.action = None
            if not self.isOver():
                self.changeMouseShow()
        if self.isOver():
            self.showWinner()
            # self.buttons[0].enable = True
            # self.buttons[1].enable = True
            # self.buttons[2].enable = False
        self.map.drawBoard(self.screen)
        self.map.printChessPiece(self.screen)

    def changeMouseShow(self):  # 开始游戏的时候把鼠标预览切换成预览棋子的样子
        map_x, map_y = pygame.mouse.get_pos()
        x, y = self.map.getIndex(map_x, map_y)
        if self.map.isInside(map_x, map_y) and self.map.isEmpty(x, y):  # 在棋盘内且当前无棋子
            pygame.mouse.set_visible(False)
            smoke_blue = (176, 224, 230)
            pos, radius = (map_x, map_y), chess_size
            pygame.draw.circle(self.screen, smoke_blue, pos, radius)
        else:
            pygame.mouse.set_visible(True)

    def checkClick(self, x, y, isAI=False):  # 后续处理
        self.map.click(x, y, self.player)
        if self.AI.isWin(self.map.map, self.player):
            self.winner = self.player
            self.click_button(self.buttons[2])
        else:
            self.player = self.map.intoNextTurn(self.player)
            if not isAI:
                self.useAI = True

    def mouseClick(self, map_x, map_y):  # 处理下棋动作
        if self.is_play and self.map.isInside(map_x, map_y) and not self.isOver():
            x, y = map_x, map_y
            if self.map.isEmpty(x, y):
                self.action = (x, y)

    def isOver(self):  # 中断条件
        return self.winner is not None

    def showWinner(self):  # 输出胜者
        def showFont(screen, text, location_x, locaiton_y, height):
            font = pygame.font.SysFont(None, height)
            font_image = font.render(text, True, (255, 215, 0), (255, 255, 255))  # 金黄色
            font_image_rect = font_image.get_rect()
            font_image_rect.x = location_x
            font_image_rect.y = locaiton_y
            screen.blit(font_image, font_image_rect)

        if self.winner == MAP_ENUM.player1:
            str = 'White Wins!'
        else:
            str = 'Black Wins!'
        showFont(self.screen, str, map_w / 5, screen_h / 8, 100)  # 居上中，字号100
        pygame.mouse.set_visible(True)

    def click_button(self, button):
        if button.click(self):
            for tmp in self.buttons:
                if tmp != button:
                    tmp.unclick()

    def check_buttons(self, mouse_x, mouse_y):
        for button in self.buttons:
            if button.rect.collidepoint(mouse_x, mouse_y):
                self.click_button(button)
                break

class UR5:
    def __init__(self, x, y):
        self.x1 = x
        self.y1 = y

    def get_current_tcp(self):
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((HOST, PORT))
        data = tcp_socket.recv(1108)
        position = struct.unpack('!6d', data[444:492])
        tcp_socket.close()
        return np.asarray(position)

    def move_to_tcp(self, target_tcp):
        tool_acc = 1.5  # 0.5
        tool_vel = 2.5  # 0.2
        tool_pos_tolerance = [0.001, 0.001, 0.001, 0.05, 0.05, 0.05]
        tcp_command = "movel(p[%f,%f,%f,%f,%f,%f],a=%f,v=%f,t=0,r=0)\n" % (
            target_tcp[0], target_tcp[1], target_tcp[2], target_tcp[3], target_tcp[4],
            target_tcp[5],
            tool_acc, tool_vel)
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((HOST, PORT))
        tcp_socket.send(str.encode(tcp_command))
        tcp_socket.close()

        actual_pos = self.get_current_tcp()
        target_rpy = util.rv2rpy(target_tcp[3], target_tcp[4], target_tcp[5])
        rpy = util.rv2rpy(actual_pos[3], actual_pos[4], actual_pos[5])
        while not (all([np.abs(actual_pos[j] - target_tcp[j]) < tool_pos_tolerance[j] for j in range(3)])
                   and all([np.abs(rpy[j] - target_rpy[j]) < tool_pos_tolerance[j + 3] for j in range(3)])):
            actual_pos = self.get_current_tcp()
            rpy = util.rv2rpy(actual_pos[3], actual_pos[4], actual_pos[5])
            time.sleep(0.01)

    def move_down(self):
        tcp = self.get_current_tcp()
        tcp[2] = 0.023
        self.move_to_tcp(tcp)

    def move_up(self):
        tcp = self.get_current_tcp()
        tcp[2] = 0.12
        self.move_to_tcp(tcp)

    def go_home(self):
        self.move_to_tcp([-0.25069, -0.02135, 0.120, 3.15, 0.1, 0.05])

    def operate_sucker(self, type):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        if type == 0:
            command = "set_digital_out(0, True)\n"
        if type == 1:
            command = "set_digital_out(0, False)\n"
        s.send(command.encode())
        s.close()
        time.sleep(1)

    def observe(self,):
        self.move_to_tcp([-0.25069, -0.02135, 0.120, 3.15, 0.1, 0.05])

    def catch(self):
        self.go_home()
        global flag
        global mov_x1
        global mov_x2
        global mov_x3
        global mov_x4
        global mov_x5
        if flag == 0:
            self.move_to_tcp([mov_x1, 0.34170, 0.120, 3.15, 0.1, 0.05])
            self.move_down()
            self.operate_sucker(1)
            self.move_up()
            self.go_home()
            mov_x1 = mov_x1 + 0.025
            print(mov_x1)
            if mov_x1 > -0.126:
                flag = 1
        elif flag == 1:
            self.move_to_tcp([mov_x2, 0.36670, 0.120, 3.15, 0.1, 0.05])
            self.move_down()
            self.operate_sucker(1)
            self.move_up()
            self.go_home()
            mov_x2 = mov_x2 + 0.025
            if mov_x2 > -0.126:
                flag = 2
        elif flag == 2:
            self.move_to_tcp([mov_x3, 0.39170, 0.120, 3.15, 0.1, 0.05])
            self.move_down()
            self.operate_sucker(1)
            self.move_up()
            self.go_home()
            mov_x3 = mov_x3 + 0.025
            if mov_x3 > -0.126:
                flag = 3
        elif flag == 3:
            self.move_to_tcp([mov_x4, 0.41670, 0.120, 3.15, 0.1, 0.05])
            self.move_down()
            self.operate_sucker(1)
            self.move_up()
            self.go_home()
            mov_x4 = mov_x4 + 0.025
            if mov_x4 > -0.126:
                flag = 4
        elif flag == 4:
            self.move_to_tcp([mov_x5, 0.44170, 0.120, 3.15, 0.1, 0.05])
            self.move_down()
            self.operate_sucker(1)
            self.move_up()
            self.go_home()
            mov_x5 = mov_x5 + 0.025

    def move_to(self, y, x):
        x = round(X2 - (X2 - X1) / 12 * x, 5)
        y = round(Y2 - (Y2 - Y1) / 12 * y, 5)
        self.move_to_tcp([x, y, 0.100, 3.15, 0.1, 0.05])
        self.operate_sucker(0)
        self.go_home()

    def go(self, x, y):
        self.catch()
        self.move_to(x, y)

if __name__ == '__main__':
    type = 0
    check = Check(type)
    game = Game(version)
    while True:
        game.play()
        pygame.display.update()
        if check.new_piece:
            mouse_x, mouse_y = check.new_piece
            game.mouseClick(mouse_x, mouse_y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                game.check_buttons(x, y)