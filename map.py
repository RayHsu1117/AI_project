# map.py

import pygame
import sys
import random
import math

# 初始化 Pygame
pygame.init()

# 路徑與路口尺寸
ROAD_WIDTH = 40  # 道路寬度
YELLOWLINE_SIZE = 10  # 黃線寬度

# 顏色設定
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
# UP = (0, 1)
# DOWN = (0, -1)
# LEFT = (-1, 0)
# RIGHT = (1, 0)

class Road:
    def __init__(self, range_coords, direction):
        """
        初始化道路物件
        :param range_coords: (x1, x2, y1, y2) 定義道路的範圍
        :param direction: 道路方向，必須是 'UP', 'DOWN', 'LEFT', 'RIGHT'
        """
        # 排序座標，確保 x1 < x2 且 y1 < y2
        self.x1, self.x2 = sorted(range_coords[:2])
        self.y1, self.y2 = sorted(range_coords[2:])

        self.direction = direction
        self.road_width = 45  # 道路寬度
        self.color = GRAY  # 道路顏色
        self.borders = []  # 初始化邊界資訊
        self.calculate_borders()

    def draw_road(self, screen):
        """
        繪製道路
        """
        pygame.draw.rect(screen, self.color, (self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1))

    def calculate_borders(self):
        """
        計算道路的邊界，存為兩條線段
        """
        if self.direction in ['UP', 'DOWN']:  # 垂直道路
            self.borders = [
                ((self.x1, self.y1), (self.x1, self.y2)),  # 左邊界
                ((self.x2, self.y1), (self.x2, self.y2))   # 右邊界
            ]
        elif self.direction in ['LEFT', 'RIGHT']:  # 水平道路
            self.borders = [
                ((self.x1, self.y1), (self.x2, self.y1)),  # 上邊界
                ((self.x1, self.y2), (self.x2, self.y2))   # 下邊界
            ]

    def draw_borders(self, screen):
        """
        在 Pygame 畫面上繪製邊界
        """
        border_width = 2  # 邊界線寬
        if self.direction == "UP":
            pygame.draw.line(screen, YELLOW, self.borders[0][0], self.borders[0][1], border_width)
            pygame.draw.line(screen, BLACK, self.borders[1][0], self.borders[1][1], border_width)
        elif self.direction == "DOWN":
            pygame.draw.line(screen, BLACK, self.borders[0][0], self.borders[0][1], border_width)
            pygame.draw.line(screen, YELLOW, self.borders[1][0], self.borders[1][1], border_width)
        elif self.direction == "LEFT":
            pygame.draw.line(screen, BLACK, self.borders[0][0], self.borders[0][1], border_width)
            pygame.draw.line(screen, YELLOW, self.borders[1][0], self.borders[1][1], border_width)
        elif self.direction == "RIGHT":
            pygame.draw.line(screen, YELLOW, self.borders[0][0], self.borders[0][1], border_width)
            pygame.draw.line(screen, BLACK, self.borders[1][0], self.borders[1][1], border_width)    


class Intersection:
    def __init__(self, range_coords):
        """
        初始化路口物件
        :param range_coords: (x1, x2, y1, y2) 定義路口的範圍
        """
        self.x1, self.x2 = sorted(range_coords[:2])
        self.y1, self.y2 = sorted(range_coords[2:])
        self.color = GRAY  # 路口顏色

    def draw_intersection(self, screen):
        """
        繪製路口
        """
        pygame.draw.rect(screen, self.color, (self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1))
       

''' road命名規則:
1. 水平方向第一位數字是基數，垂直方向第一位數字是偶數
2. 依據行進方向分為 1上 2下 3左 4右，第二位數字由此決定
3. 第三位數字由左到右排序
'''

roads = {
    'road_131': Road((45, 200, 0, 20), 'LEFT'),
    'road_132': Road((245, 355, 0, 20), 'LEFT'),
    'road_133': Road((400, 555, 0, 20), 'LEFT'),
    'road_141': Road((45, 200, 25, 45), 'RIGHT'),
    'road_142': Road((245, 355, 25, 45), 'RIGHT'),
    'road_143': Road((400, 555, 25, 45), 'RIGHT'),

    'road_331': Road((45, 200, 200, 220), 'LEFT'),
    'road_332': Road((245, 355, 200, 220), 'LEFT'),
    'road_333': Road((400, 555, 200, 220), 'LEFT'),
    'road_341': Road((45, 200, 225, 245), 'RIGHT'),
    'road_342': Road((245, 355, 225, 245), 'RIGHT'),
    'road_343': Road((400, 555, 225, 245), 'RIGHT'),

    'road_531': Road((45, 200, 355, 375), 'LEFT'),
    'road_532': Road((245, 355, 355, 375), 'LEFT'),
    'road_533': Road((400, 555, 355, 375), 'LEFT'),
    'road_541': Road((45, 200, 380, 400), 'RIGHT'),
    'road_542': Road((245, 355, 380, 400), 'RIGHT'),
    'road_543': Road((400, 555, 380, 400), 'RIGHT'),

    'road_731': Road((45, 200, 555, 575), 'LEFT'),
    'road_732': Road((245, 355, 555, 575), 'LEFT'),
    'road_733': Road((400, 555, 555, 575), 'LEFT'),
    'road_741': Road((45, 200, 580, 600), 'RIGHT'),
    'road_742': Road((245, 355, 580, 600), 'RIGHT'),
    'road_743': Road((400, 555, 580, 600), 'RIGHT'),

    'road_221': Road((0, 20, 45, 200), 'DOWN'),
    'road_222': Road((0, 20, 245, 355), 'DOWN'),
    'road_223': Road((0, 20, 400, 555), 'DOWN'),
    'road_211': Road((25, 45, 45, 200), 'UP'),
    'road_212': Road((25, 45, 245, 355), 'UP'),
    'road_213': Road((25, 45, 400, 555), 'UP'),

    'road_421': Road((200, 220, 45, 200), 'DOWN'),
    'road_422': Road((200, 220, 245, 355), 'DOWN'),
    'road_423': Road((200, 220, 400, 555), 'DOWN'),
    'road_411': Road((225, 245, 45, 200), 'UP'),
    'road_412': Road((225, 245, 245, 355), 'UP'),
    'road_413': Road((225, 245, 400, 555), 'UP'),

    'road_621': Road((355, 375, 45, 200), 'DOWN'),
    'road_622': Road((355, 375, 245, 355), 'DOWN'),
    'road_623': Road((355, 375, 400, 555), 'DOWN'),
    'road_611': Road((380, 400, 45, 200), 'UP'),
    'road_612': Road((380, 400, 245, 355), 'UP'),
    'road_613': Road((380, 400, 400, 555), 'UP'),

    'road_821': Road((555, 575, 45, 200), 'DOWN'),
    'road_822': Road((555, 575, 245, 355), 'DOWN'),
    'road_823': Road((555, 575, 400, 555), 'DOWN'),
    'road_811': Road((580, 600, 45, 200), 'UP'),
    'road_812': Road((580, 600, 245, 355), 'UP'),
    'road_813': Road((580, 600, 400, 555), 'UP')
}
    
road_couples = [
    ('road_131','road_141'),('road_132','road_142'),('road_133','road_143'),('road_331','road_341'),('road_332','road_342'),('road_333','road_343'),('road_531','road_541'),('road_532','road_542'),('road_533','road_543'),('road_731','road_741'),('road_732','road_742'),('road_733','road_743'),('road_221','road_211'),('road_222','road_212'),('road_223','road_213'),('road_421','road_411'),('road_422','road_412'),('road_423','road_413'),('road_621','road_611'),('road_622','road_612'),('road_623','road_613'),('road_821','road_811'),('road_822','road_812'),('road_823','road_813')
]

intersections = {
    'intersection_1': Intersection((0, 45, 0, 45)),
    'intersection_2': Intersection((200, 245, 0, 45)),
    'intersection_3': Intersection((355, 400, 0, 45)),
    'intersection_4': Intersection((555, 600, 0, 45)),

    'intersection_5': Intersection((0, 45, 200, 245)),
    'intersection_6': Intersection((200, 245, 200, 245)),
    'intersection_7': Intersection((355, 400, 200, 245)),
    'intersection_8': Intersection((555, 600, 200, 245)),

    'intersection_9': Intersection((0, 45, 355, 400)),
    'intersection_10': Intersection((200, 245, 355, 400)),
    'intersection_11': Intersection((355, 400, 355, 400)),
    'intersection_12': Intersection((555, 600, 355, 400)),
    
    'intersection_13': Intersection((0, 45, 555, 600)),
    'intersection_14': Intersection((200, 245, 555, 600)),
    'intersection_15': Intersection((355, 400, 555, 600)),
    'intersection_16': Intersection((555, 600, 555, 600))
}

