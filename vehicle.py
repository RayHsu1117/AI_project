# vehicle.py
from collections import deque
import pygame
from map import roads
from map import road_couples
from map import intersections
import random

VEHICLE_SIZE = 15
CAR_COLOR = (255, 0, 0)  # 紅色
CAR_REACHED_COLOR = (255, 165, 0)  # 橘色
# 車輛編號計數器
vehicle_counter = 1
# 每次移動的步長
step = 2

class Vehicle:
    def __init__(self, start, destination,start_road,destination_road, vehicle_id):
        self.x, self.y = start
        self.path = deque(self.calculate_path(start, destination))  # 計算路徑
        self.start = start
        self.destination = destination
        self.reached_destination = False  # 車輛是否到達終點
        self.start_road = start_road
        self.destination_road = destination_road
        self.vehicle_id = vehicle_id  # 使用傳入的車號

        self.previous_place = self.find_place(self.x, self.y)
        self.current_place = self.previous_place



    def calculate_path(self, start, destination):
        """計算車輛移動的路徑"""
        sx, sy = start
        dx, dy = destination
        path = []
        
        start_road = self.find_place(sx, sy)
        dest_road = self.find_place(dx, dy)
        print("start: "+start_road)
        print(roads[start_road].direction)
        print("dest: "+dest_road)
        print(roads[dest_road].direction)
        

        # 簡單直線移動邏輯 (分別處理 x 和 y)
        if sx != dx:
            for x in range(sx, dx, step if dx > sx else -step):
                path.append((x, sy))
        if sy != dy:
            for y in range(sy, dy, step if dy > sy else -step):
                path.append((dx, y))
    
        # 確保包含最終目標點
        path.append(destination)
        return path

    def move(self):
        #"""讓車輛沿路徑移動"""
        #if not self.reached_destination and self.path:
        #    self.x, self.y = self.path.popleft()
        #    #print(self.find_place(self.x, self.y))
        #if not self.path:  # 如果路徑空了，標記為到達終點
        #    self.reached_destination = True

        #簡易greedy
        if self.is_on_road() is True:
                direction = roads[self.current_place].direction
                if direction == 'UP':
                    self.y -= step
                elif direction == 'DOWN':
                    self.y += step
                elif direction == 'LEFT':
                    self.x -= step
                else:
                    self.x += step
            #else:





    def is_on_road(self):
        if (((self.x >= 45 and self.x+VEHICLE_SIZE <= 200) or
           (self.x >= 245 and self.x+VEHICLE_SIZE <= 355) or
           (self.x >= 400 and self.x+VEHICLE_SIZE <= 555)) and
           ((self.y >= 0 and self.y+VEHICLE_SIZE <= 45) or
            (self.y >= 200 and self.y+VEHICLE_SIZE <= 245) or
            (self.y >= 355 and self.y+VEHICLE_SIZE <= 400) or
            (self.y >= 555 and self.y+VEHICLE_SIZE <= 600))):
            return True
        if (((self.y >= 45 and self.y+VEHICLE_SIZE <= 200) or
            (self.y >= 245 and self.y+VEHICLE_SIZE <= 355) or
            (self.y >= 400 and self.y+VEHICLE_SIZE <= 555)) and
            ((self.x >= 0 and self.x+VEHICLE_SIZE <= 45) or
            (self.x >= 200 and self.x+VEHICLE_SIZE <= 245) or
            (self.x >= 355 and self.x+VEHICLE_SIZE <= 400) or
            (self.x >= 555 and self.x+VEHICLE_SIZE <= 600))):
            return True
        return False
        

    def find_place(self, x, y):
        """
        判斷車輛位置屬於哪條道路或哪個路口
        :param vehicle_coords: 車輛左上角坐標 (x, y)，格式為 (x, y)
        :param roads: 道路字典
        :param intersections: 路口字典
        :return: 位於的道路或路口名稱
        """

        # 計算車輛的範圍 (bounding box)
        vehicle_box = (
            x,
            x + VEHICLE_SIZE,
            y,
            y + VEHICLE_SIZE
        )

        # 檢查是否與某個路口有重疊
        for name, intersection in intersections.items():
            if (
                vehicle_box[0] < intersection.x2 and
                vehicle_box[1] > intersection.x1 and
                vehicle_box[2] < intersection.y2 and
                vehicle_box[3] > intersection.y1
            ):
                return name

        # 檢查是否與某條道路有重疊
        for name, road in roads.items():
            if (
                vehicle_box[0] <= road.x2 and
                vehicle_box[1] >= road.x1 and
                vehicle_box[2] <= road.y2 and
                vehicle_box[3] >= road.y1
            ):
                return name

        # 若不在任何道路或路口
        return "Not on any road or intersection"

    def draw(self, screen):
        """繪製車輛"""
        color = CAR_REACHED_COLOR if self.reached_destination else CAR_COLOR
        pygame.draw.rect(screen, color, (self.x, self.y, VEHICLE_SIZE, VEHICLE_SIZE))
    
        # 顯示車號
        font = pygame.font.Font(None, 24)
        text = font.render(str(self.vehicle_id), True, (0, 0, 0))  # 車號顯示為黑色
    
        # 計算車號顯示的位置，使其位於車輛方框的中心
        text_rect = text.get_rect(center=(self.x + VEHICLE_SIZE // 2, self.y + VEHICLE_SIZE // 2))
        screen.blit(text, text_rect)  # 把車號渲染到畫面

    def draw_end(self, screen):
        """繪製終點並顯示車號"""
        pygame.draw.rect(screen, (0, 255, 0), (self.destination[0], self.destination[1], VEHICLE_SIZE, VEHICLE_SIZE))
    
        # 顯示車號
        font = pygame.font.Font(None, 24)
        text = font.render(str(self.vehicle_id), True, (0, 0, 0))  # 車號顯示為黑色
    
        # 計算車號顯示的位置，使其位於終點方框的中心
        text_rect = text.get_rect(center=(self.destination[0] + VEHICLE_SIZE // 2, self.destination[1] + VEHICLE_SIZE // 2))
        screen.blit(text, text_rect)  # 把車號渲染到畫面


def generate_vehicle():
    """在隨機道路上隨機生成車輛"""
    global vehicle_counter  # 引用全局車輛編號變數
    try:
        start_point, start_road = generate_random()
        destination_point, destination_road = generate_random()
        
        # 創建車輛並將當前車號傳入
        vehicle = Vehicle(start_point, destination_point, start_road, destination_road, vehicle_counter)
        
        # 車號遞增
        vehicle_counter += 1
        
        return vehicle

    except Exception as e:
        print(f"Error generating vehicle : {e}")
        return None

def generate_random():
    """生成隨機的點"""
    road = random.choice(list(roads.keys()))
    if(roads[road].direction == "LEFT" or roads[road].direction == "RIGHT"):
        point = (random.randint(roads[road].x1,roads[road].x2-VEHICLE_SIZE),random.randint(roads[road].y1,roads[road].y2-VEHICLE_SIZE))
    else:    
        point = (random.randint(roads[road].x1,roads[road].x2-VEHICLE_SIZE),random.randint(roads[road].y1,roads[road].y2-VEHICLE_SIZE))
    return point,road
