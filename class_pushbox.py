import turtle
import level
import cv2
import numpy as np
import mediapipe as mp
from cvzone.HandTrackingModule import HandDetector
ms = turtle.Screen()
ms.setup(450, 650, 200, 0)
ms.bgcolor('Beige')
ms.title('推箱子小游戏')
ms.register_shape('wall.gif')
ms.register_shape('o.gif')
ms.register_shape('p.gif')
ms.register_shape('box.gif')
ms.register_shape('boxc.gif')
ms.tracer(0)

levels = level.level_list()


class Pen(turtle.Turtle):
    def __init__(self, pic):
        super().__init__()
        self.shape(pic) # 设置画笔
        self.penup() # 让画笔抬起
    def move(self, x, y, px, py):
        gox, goy = x+px, y+py # 计算目标坐标
        if (gox, goy) in go_space: # 检查坐标是否落入指定范围内
            self.goto(gox, goy)
        if (gox+px, goy+py) in go_space and (gox, goy) in box_space:
            for i in box_list: # 遍历找到与画笔位置匹配的方块
                if i.pos() == (gox, goy):
                    go_space.append(i.pos())
                    box_space.remove(i.pos()) # 将方块从原先位置移除
                    i.goto(gox+px, goy+py)
                    self.goto(gox, goy)
                    go_space.remove(i.pos())
                    box_space.append(i.pos())
                    if i.pos() in correct_box_space:
                        i.shape('boxc.gif') # 箱子到指定位置，改变图片
                    else:
                        i.shape('box.gif')
                    if set(box_space) == set(correct_box_space):
                        text.show_win() # 所有箱子抵达，游戏胜利

    """定义画笔移动方式"""
    # 画笔向上   
    def go_up(self):
        self.move(self.xcor(), self.ycor(), 0, 50)
    # 画笔向下
    def go_down(self):
        self.move(self.xcor(), self.ycor(), 0, -50)
    # 画笔向左
    def go_left(self):
        self.move(self.xcor(), self.ycor(), -50, 0)
    # 画笔向右
    def go_right(self):
        self.move(self.xcor(), self.ycor(), 50, 0)


class Game():
    def paint(self):
        i_date = len(levels[num-1])
        j_date = len(levels[num-1][0])
        for i in range(i_date):
            for j in range(j_date):
                x = -j_date*25+25+j*50
                y = i_date*25-25-i*50
                # 绘制并记录箱子目的地
                if levels[num-1][i][j] == 'O':
                    correct_box.goto(x, y)
                    correct_box.stamp()
                    go_space.append((x, y))
                    correct_box_space.append((x, y))
        for i in range(i_date):
            for j in range(j_date):
                x = -j_date*25+25+j*50
                y = i_date*25-25-i*50
                # 记录空位
                if levels[num-1][i][j] == ' ':
                    go_space.append((x, y))
                # 绘制墙壁
                if levels[num-1][i][j] == 'X':
                    wall.goto(x, y)
                    wall.stamp()
                # 绘制玩家，并记录玩家初始位置
                if levels[num-1][i][j] == 'P':
                    player.goto(x, y)
                    go_space.append((x, y))
                # 绘制箱子，记录箱子位置
                if levels[num-1][i][j] == 'B':
                    box = Pen('box.gif')
                    box.goto(x, y)
                    box_list.append(box)
                    box_space.append((x, y))


# 关卡交互提示
class ShowMessage(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.pencolor('Brown1')
        self.ht()

    def message(self):
        self.goto(0, 290)
        self.write(f'第{num}关', align='center', font=('楷体', 20, 'bold'))
        self.goto(0, 270)
        self.write('按空格进入下一关', align='center', font=('楷体', 15, 'bold'))
        self.goto(0, 250)
        self.write('退出游戏请按Q', align='center', font=('楷体', 15, 'bold'))

    def show_win(self):
        global num
        if num == len(levels):
            num = 1
            self.goto(0, 0)
            self.write('你已通过全部关', align='center', font=('黑体', 30, 'bold'))
            self.goto(0, -50)
            self.write('返回第一关轻按空格键', align='center', font=('黑体', 30, 'bold'))
        else:
            num = num+1
            self.goto(0, 0)
            self.write('恭喜过关', align='center', font=('黑体', 30, 'bold'))
            self.goto(0, -50)
            self.write('进入下一关请按空格键', align='center', font=('黑体', 30, 'bold'))


def init():
    text.clear()
    wall.clear()
    correct_box.clear()
    for i in box_list:
        i.ht()
        del(i)
    box_list.clear()
    box_space.clear()
    go_space.clear()
    correct_box_space.clear()
    game.paint()
    text.message()



def choose():
    global num
    a = ms.numinput('选择关卡', '你的选择（请输入1-5）', 1)
    if a is None:
        a = num
    num = int(a)
    init()
    ms.listen()



num = 1
correct_box_space = []
box_list = []
box_space = []
go_space = []
wall = Pen('wall.gif')
correct_box = Pen('o.gif')
player = Pen('p.gif')
game = Game()
game.paint()
text = ShowMessage()
text.message()

ms.listen()
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)
flag=False
finger_count = 0
while True:
    success, img = cap.read() # 获取图像帧
    # 找到那只手和它的标志
    hands, img = detector.findHands(img)  
    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # 21个手部标志点
        bbox1 = hand1["bbox"]  # 边界框信息x,y,w,h
        centerPoint1 = hand1['center']  # 手的中心cx cy
        handType1 = hand1["type"]  # 识别左右手
        fingers1 = detector.fingersUp(hand1)
        # 记录并在屏幕中显示伸出手指数量
        if fingers1:
            finger_count = fingers1.count(1)
            cv2.putText(img, f"Finger Count: {finger_count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    # 根据手指数量确定玩家移动的方向（上：5，下：4，左：3，右：2）
    if not flag:  # 如果标志为 False
        if finger_count== 5:
            player.go_up()
            flag = True  # 设置标志为 True
        elif finger_count == 4:
            player.go_down()
            flag = True
        elif finger_count == 3:
            player.go_left()
            flag = True
        elif finger_count == 2:
            player.go_right()
            flag = True
    if finger_count==0:
        flag = False
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(1) & 0xFF== ord(' '):  # 检测空格键按下事件
        init()  # 初始化下一关
        prev_hand_side = None  # 重置手势方向
    ms.update()
cap.release()
cv2.destroyAllWindows()