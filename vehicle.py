# vehicle.py
import pygame
import math
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
step = 4 # 當調整至5及以上時會出問題
# 迴轉與左轉的移動幅度
TURN_SHIFT = 25
# 安全距離
SAFTY_DISTANCE = math.floor(2.5*VEHICLE_SIZE)
# 與終點坐標的誤差
ERROR_DISTANCE = 5

class Vehicle:
    def __init__(self, start, destination,start_road,destination_road, vehicle_id, start_time = 1):
        self.x, self.y = start
        self.start = start
        self.destination = destination
        self.reached_destination = False  # 車輛是否到達終點
        self.start_road = start_road # 起點所在路名
        self.destination_road = destination_road # 終點所在路名
        self.vehicle_id = vehicle_id  # 使用傳入的車號

        self.start_time = start_time  # Record when the vehicle was generated
        self.time_to_reach = None  # Record when the vehicle reaches its destination

        self.previous_place = start_road
        self.current_place = start_road
        self.current_direction = roads[self.current_place].direction # 初始位置一定是在道路上
        self.most_front = 0 # 用於正在進入十字路口時的前進距離上限

        self.has_action = True
        self.action = None
        self.most_front_turn = 0 # 用於在十字路口路中央時的前進距離上限 (用於左轉)
        self.most_left_turn = 0 # 用於在十字路口路中央時的左進距離上限 (用於迴轉)

        self.stop = True
        self.just_inter_intersection = False # 是否位於十字路口前(以及要進去與已進去)
        self.inter_intersection = False

    def need_stop_direct(self, vehicles): # 考慮在道路直行時是否需停(是否在小於安全距離的情況下在開在別臺車後面)
        """這個 branch 上不考慮了"""
        self.stop = False
        return False

    def need_stop_before_intersection(self, vehicles):
        """這個 branch 上不考慮了"""
        return False
    
    def adjust_location(self): # 調整使車在路中央
        if self.current_direction == 'UP':
            self.x = roads[self.current_place].x1+3
        elif self.current_direction == 'DOWN':
            self.x = roads[self.current_place].x1+2
        elif self.current_direction == 'LEFT':
            self.y = roads[self.current_place].y1+2
        elif self.current_direction == 'RIGHT':
            self.y = roads[self.current_place].y1+3

    def move(self, vehicles, total_frames):
        #print(self.find_place(self.x, self.y))
        #print(self.has_action)
        if self.reached_destination:
            return

        dx, dy = self.destination
        delta_x = dx-self.x
        delta_y = dy-self.y

        if self.is_on_road(self.x, self.y):
            # 已完成轉彎動作因此將相關flags設為false，並根據所在道路方向記錄行車方向
            if self.has_action:
                self.is_middle = False
                self.has_action = False
                self.just_inter_intersection = False
                self.inter_intersection = False
                self.current_place = self.find_place(self.x, self.y)
                self.current_direction = roads[self.current_place].direction
                self.adjust_location()
                if self.current_direction == 'UP':
                    self.most_front = roads[self.current_place].y1-VEHICLE_SIZE-2
                elif self.current_direction == 'DOWN':
                    self.most_front = roads[self.current_place].y2+2
                elif self.current_direction == 'LEFT':
                    self.most_front = roads[self.current_place].x1-VEHICLE_SIZE-2
                else:
                    self.most_front = roads[self.current_place].x2+2

            # 在路上的車只能一直走到路口前方
            if self.need_stop_direct(vehicles):
                pass
            elif self.current_direction == 'UP':
                self.y -= step
            elif self.current_direction == 'DOWN':
                self.y += step
            elif self.current_direction == 'LEFT':
                self.x -= step
            else:
                self.x += step
        else:
            # 先走到路口中央
            if self.just_inter_intersection == False:
                self.just_inter_intersection = True
                self.stop = True
                self.previous_place = self.current_place
                self.current_place = self.find_place(self.x, self.y)
            if self.just_inter_intersection == True and self.stop == True:
                if self.need_stop_before_intersection(vehicles):
                    self.stop = True
                else:
                    self.stop = False
            elif not self.has_action:
                if self.inter_intersection == False:
                    self.inter_intersection = True
                if self.current_direction == 'UP' and self.y > self.most_front:
                    self.y -= step
                elif self.current_direction == 'DOWN' and self.y < self.most_front:
                    self.y += step
                elif self.current_direction == 'LEFT' and self.x > self.most_front:
                    self.x -= step
                elif self.current_direction == 'RIGHT' and self.x < self.most_front:
                    self.x += step
                else:
                    self.action = self.greedy_agent() # 策略
                    self.has_action = True
                    if self.current_direction == 'UP':
                        self.most_front_turn = intersections[self.current_place].y1+2
                        self.most_left_turn = intersections[self.current_place].x1+2
                    elif self.current_direction == 'DOWN':
                        self.most_front_turn = intersections[self.current_place].y2-VEHICLE_SIZE-2
                        self.most_left_turn = intersections[self.current_place].x2-VEHICLE_SIZE-2
                    elif self.current_direction == 'LEFT':
                        self.most_front_turn = intersections[self.current_place].x1+2
                        self.most_left_turn = intersections[self.current_place].y2-VEHICLE_SIZE-2
                    elif self.current_direction == 'RIGHT':
                        self.most_front_turn = intersections[self.current_place].x2-VEHICLE_SIZE-2
                        self.most_left_turn = intersections[self.current_place].y1+2
            # 到了路口中央馬上執行行動 (行動後總是會走到另外一條道路上，到時候self.has_action會變回false)
            # 在此之前可先決定策略，並存進self.action中，之後直接套用self.do_action(self.action)
            else:
                self.do_action(self.action) # 'AHEAD': 直行; 'BACK': 迴轉; 'LEFT': 左轉; 'RIGHT': 右轉
            
        if abs(delta_x) < ERROR_DISTANCE and abs(delta_y) < ERROR_DISTANCE: # 容錯誤差
            self.reached_destination = True
            self.time_to_reach = total_frames
            print("Vehicle "+str(self.vehicle_id)+" arrives.")

    def do_action(self, direction):
        # 這裡的direction是指對車子而言的欲轉彎方向，而self.current_direction為旁觀者所看的車頭朝向方向
        if direction == 'AHEAD': # 直行
            if self.current_direction == 'UP':
                self.y -= step
            elif self.current_direction == 'DOWN':
                self.y += step
            elif self.current_direction == 'LEFT':
                self.x -= step
            elif self.current_direction == 'RIGHT':
                self.x += step
        elif direction == 'BACK': # 迴轉 (我父親時常這麼做，所以這是合理的行為)
            if self.current_direction == 'UP':
                if self.x > self.most_left_turn:
                    self.x -= step
                elif self.x < intersections[self.current_place].x1+2:
                    self.x = intersections[self.current_place].x1+2
                else:
                    self.y += step
            elif self.current_direction == 'DOWN':
                if self.x < self.most_left_turn:
                    self.x += step
                elif self.x > intersections[self.current_place].x2-VEHICLE_SIZE-2:
                    self.x = intersections[self.current_place].x2-VEHICLE_SIZE-2
                else:
                    self.y -= step
            elif self.current_direction == 'LEFT':
                if self.y < self.most_left_turn:
                    self.y += step
                elif self.y > intersections[self.current_place].y2-VEHICLE_SIZE-2:
                    self.y = intersections[self.current_place].y2-VEHICLE_SIZE-2
                else:
                    self.x += step
            elif self.current_direction == 'RIGHT':
                if self.y > self.most_left_turn:
                    self.y -= step
                elif self.y < intersections[self.current_place].y1+2:
                    self.y = intersections[self.current_place].y1+2
                else:
                    self.x -= step
        elif direction == 'LEFT': # 左轉
            if self.current_direction == 'UP':
                if self.y > self.most_front_turn:
                    self.y -= step
                elif self.y < intersections[self.current_place].y1+2:
                    self.y = intersections[self.current_place].y1+2
                else:
                    self.x -= step
            elif self.current_direction == 'DOWN':
                if self.y < self.most_front_turn:
                    self.y += step
                elif self.y > intersections[self.current_place].y2-VEHICLE_SIZE-2:
                    self.y = intersections[self.current_place].y2-VEHICLE_SIZE-2
                else:
                    self.x += step
            elif self.current_direction == 'LEFT':
                if self.x > self.most_front_turn:
                    self.x -= step
                elif self.x < intersections[self.current_place].x1+2:
                    self.x = intersections[self.current_place].x1+2
                else:
                    self.y += step
            elif self.current_direction == 'RIGHT':
                if self.x < self.most_front_turn:
                    self.x += step
                elif self.x > intersections[self.current_place].x2-VEHICLE_SIZE-2:
                    self.x = intersections[self.current_place].x2-VEHICLE_SIZE-2
                else:
                    self.y -= step
        elif direction == 'RIGHT': # 右轉
            if self.current_direction == 'UP':
                if self.y < intersections[self.current_place].y2-VEHICLE_SIZE-2:
                    self.y = intersections[self.current_place].y2-VEHICLE_SIZE-2
                self.x += step
            elif self.current_direction == 'DOWN':
                if self.y > intersections[self.current_place].y1+2:
                    self.y = intersections[self.current_place].y1+2
                self.x -= step
            elif self.current_direction == 'LEFT':
                self.y -= step
                if self.x < intersections[self.current_place].x2-VEHICLE_SIZE-2:
                    self.x = intersections[self.current_place].x2-VEHICLE_SIZE-2
            elif self.current_direction == 'RIGHT':
                self.y += step
                if self.x > intersections[self.current_place].x1+2:
                    self.x = intersections[self.current_place].x1+2
        else:
            print("Wrong.")
            
    def greedy_agent(self): # 這個策略似乎非常喜歡迴轉
        dx, dy = self.destination
        action = self.is_near(self.destination_road)
        if action is None:
            delta_block_x = self.cut_corners_block_counter(self.x, dx)
            delta_block_y = self.cut_corners_block_counter(self.y, dy)
            if self.current_direction == 'UP':
                if delta_block_x >= 1:
                    return 'RIGHT'
                elif delta_block_x <= -1:
                    return 'LEFT'
                elif delta_block_y >= 1:
                    return 'BACK'
                elif delta_block_y <= -1:
                    return 'AHEAD'
            elif self.current_direction == 'DOWN':
                if delta_block_x >= 1:
                    return 'LEFT'
                elif delta_block_x <= -1:
                    return 'RIGHT'
                elif delta_block_y >= 1:
                    return 'AHEAD'
                elif delta_block_y <= -1:
                    return 'BACK'
            elif self.current_direction == 'LEFT':
                if delta_block_x >= 1:
                    return 'BACK'
                elif delta_block_x <= -1:
                    return 'AHEAD'
                elif delta_block_y >= 1:
                    return 'LEFT'
                elif delta_block_y <= -1:
                    return 'RIGHT'
            elif self.current_direction == 'RIGHT':
                if delta_block_x >= 1:
                    return 'AHEAD'
                elif delta_block_x <= -1:
                    return 'BACK'
                elif delta_block_y >= 1:
                    return 'RIGHT'
                elif delta_block_y <= -1:
                    return 'LEFT'
            else:
                print("Not_Well_designed")
                return 'BACK'
        else:
            return action
    
    def is_near(self, dest_road): # if is_near: 表示只要一或二個動作就可以到目的地了; 如果是會回傳動作，如果不是則回傳None
        extend_vertical = 45 # 假設車子前進或後退45單位
        extend_horizon = 45 # 假設車子前進或後退45單位
        if self.current_direction == 'UP': # 車頭朝前
            future_road = self.find_place(self.x, self.y-extend_vertical)
            if future_road == dest_road or self.is_pair(future_road, dest_road):
                return 'AHEAD'
            future_road = self.find_place(self.x, self.y+extend_vertical)
            if self.is_pair(future_road, dest_road) or future_road == dest_road:
                return 'BACK'
            future_road = self.find_place(self.x-extend_horizon, self.y)
            if self.is_pair(future_road, dest_road) or future_road == dest_road:
                return 'LEFT'
            future_road = self.find_place(self.x+extend_horizon, self.y)
            if future_road == dest_road or self.is_pair(future_road, dest_road):
                return 'RIGHT'
        elif self.current_direction == 'DOWN': # 車頭朝後
            future_road = self.find_place(self.x, self.y+extend_vertical)
            if future_road == dest_road or self.is_pair(future_road, dest_road):
                return 'AHEAD'
            future_road = self.find_place(self.x, self.y-extend_vertical)
            if self.is_pair(future_road, dest_road) or future_road == dest_road:
                return 'BACK'
            future_road = self.find_place(self.x+extend_horizon, self.y)
            if self.is_pair(future_road, dest_road) or future_road == dest_road:
                return 'LEFT'
            future_road = self.find_place(self.x-extend_horizon, self.y)
            if future_road == dest_road or self.is_pair(future_road, dest_road):
                return 'RIGHT'
        elif self.current_direction == 'LEFT': # 車頭朝左
            future_road = self.find_place(self.x-extend_horizon, self.y)
            if future_road == dest_road or self.is_pair(future_road, dest_road):
                return 'AHEAD'
            future_road = self.find_place(self.x+extend_horizon, self.y)
            if self.is_pair(future_road, dest_road) or future_road == dest_road:
                return 'BACK'
            future_road = self.find_place(self.x, self.y+extend_vertical)
            if self.is_pair(future_road, dest_road) or future_road == dest_road:
                return 'LEFT'
            future_road = self.find_place(self.x, self.y-extend_vertical)
            if future_road == dest_road or self.is_pair(future_road, dest_road):
                return 'RIGHT'
        elif self.current_direction == 'RIGHT': # 車頭朝右
            future_road = self.find_place(self.x+extend_horizon, self.y)
            if future_road == dest_road or self.is_pair(future_road, dest_road):
                return 'AHEAD'
            future_road = self.find_place(self.x-extend_horizon, self.y)
            if self.is_pair(future_road, dest_road) or future_road == dest_road:
                return 'BACK'
            future_road = self.find_place(self.x, self.y-extend_vertical)
            if self.is_pair(future_road, dest_road) or future_road == dest_road:
                return 'LEFT'
            future_road = self.find_place(self.x, self.y+extend_vertical)
            if future_road == dest_road or self.is_pair(future_road, dest_road):
                return 'RIGHT'
        else:
            return None

    def cut_corners_block_counter(self, self_ordinate, dest_ordinate): # 由於地圖的對稱性所以得以投機取巧地不須區分x與y
        # 0 45   200 245   355 400   555 600
        self_block = self.cut_corners_switch_case(self_ordinate)
        dest_block = self.cut_corners_switch_case(dest_ordinate)
        return dest_block - self_block
            
    def cut_corners_switch_case(self, number): # 由於地圖的對稱性所以投機取巧地寫了這個分類程式以減少程式碼長度
        # 分類成立基於起點與終點都在道路上且不會重疊到十字路口
        if 0 <= number and number < 45:
            return 0.5
        elif number < 200:
            return 1
        elif number < 245:
            return 1.5
        elif number < 355:
            return 2
        elif number < 400:
            return 2.5
        elif number < 555:
            return 3
        else:
            return 3.5  

    def is_on_road(self, x, y):
        if (((x >= 45 and x+VEHICLE_SIZE <= 200) or
           (x >= 245 and x+VEHICLE_SIZE <= 355) or
           (x >= 400 and x+VEHICLE_SIZE <= 555)) and
           ((y >= 0 and y+VEHICLE_SIZE <= 45) or
            (y >= 200 and y+VEHICLE_SIZE <= 245) or
            (y >= 355 and y+VEHICLE_SIZE <= 400) or
            (y >= 555 and y+VEHICLE_SIZE <= 600))):
            return True
        if (((y >= 45 and y+VEHICLE_SIZE <= 200) or
            (y >= 245 and y+VEHICLE_SIZE <= 355) or
            (y >= 400 and y+VEHICLE_SIZE <= 555)) and
            ((x >= 0 and x+VEHICLE_SIZE <= 45) or
            (x >= 200 and x+VEHICLE_SIZE <= 245) or
            (x >= 355 and x+VEHICLE_SIZE <= 400) or
            (x >= 555 and x+VEHICLE_SIZE <= 600))):
            return True
        return False
        
    def is_pair(self, road1, road2):
        return (road1, road2) in road_couples or (road2, road1) in road_couples

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

        # 檢查是否與某條道路有重疊 (只有車子全部都在車道內才能算是在車道內)
        for name, road in roads.items():
            if (
                vehicle_box[0] >= road.x1 and
                vehicle_box[1] <= road.x2 and
                vehicle_box[2] >= road.y1 and
                vehicle_box[3] <= road.y2
            ):
                return name

        # 檢查是否與某個路口有重疊 (只要有一邊踏進十字路口就算是在十字路口內了)
        for name, intersection in intersections.items():
            if (# 上邊或下邊在內
                (vehicle_box[0] >= intersection.x1 and vehicle_box[1] <= intersection.x2 and vehicle_box[2] <= intersection.y2 and vehicle_box[3] >= intersection.y1)
                or # 左邊或右邊在內
                (vehicle_box[2] >= intersection.y1 and vehicle_box[3] <= intersection.y2 and vehicle_box[0] <= intersection.x2 and vehicle_box[1] >= intersection.x1)
            ):
                return name

        # 若不在任何道路或路口
        return 'Not on any road or intersection'

    def draw_car(self, screen):
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


def generate_vehicles(amount):
    """在隨機道路上隨機生成車輛"""
    vehicles = []
    current_amount = 0

    # 第一台車
    start_point, start_road = pick_random_location()
    destination_point, destination_road = pick_random_location()
    current_amount += 1
    vehicle = Vehicle(start_point, destination_point, start_road, destination_road, current_amount)
    vehicles.append(vehicle)
    
    # 之後的車
    while current_amount < amount:
        start_point, start_road = pick_random_location()
        destination_point, destination_road = pick_random_location()
        is_all_apart = True
        for gotten_vehicle in vehicles:
            if not is_apart(start_point, start_road, gotten_vehicle.start, gotten_vehicle.start_road) or not is_apart(destination_point, destination_road, gotten_vehicle.destination, gotten_vehicle.destination_road):
                is_all_apart = False
                break
        if is_all_apart:
            current_amount += 1
            vehicle = Vehicle(start_point, destination_point, start_road, destination_road, current_amount)
            vehicles.append(vehicle)
    
    return vehicles

def pick_random_location():
    random_road = random.choice(list(roads.keys()))
    x1, x2, y1, y2, direction = roads[random_road].x1, roads[random_road].x2, roads[random_road].y1, roads[random_road].y2, roads[random_road].direction
    if direction == 'UP':
        point = (x1+3, random.randint(y1, y2-VEHICLE_SIZE-2))
    elif direction == 'DOWN':
        point = (x1+2, random.randint(y1, y2-VEHICLE_SIZE-2))
    elif direction == 'LEFT':
        point = (random.randint(x1, x2-VEHICLE_SIZE-2), y1+2)
    elif direction == 'RIGHT':
        point = (random.randint(x1, x2-VEHICLE_SIZE-2), y1+3)
    return point, random_road

def is_apart(point1, road1, point2, road2):
    if road1 != road2:
        return True
    else:
        direction = roads[road1].direction
        x1, y1 = point1
        x2, y2 = point2
        if direction == 'UP' or direction == 'DOWN':
            if abs(y1-y2) > 3*VEHICLE_SIZE:
                return True
        elif direction == 'LEFT' or direction == 'RIGHT':
            if abs(x1-x2) > 3*VEHICLE_SIZE:
                return True
    return False

def car_crash(vehicles):
    """檢查車輛是否有相撞並記錄結果"""
    for i in range(len(vehicles)):
        # 已到達終點的不用計算
        if(vehicles[i].reached_destination):
            continue
        for j in range(i + 1, len(vehicles)):
            # 已到達終點的不用計算
            if(vehicles[j].reached_destination):
                continue

            # 獲取車輛位置範圍
            x1, y1 = vehicles[i].x, vehicles[i].y
            x2, y2 = vehicles[j].x, vehicles[j].y
            
            # 碰撞條件：兩車的 x, y 範圍重疊
            if (abs(x1 - x2) < (VEHICLE_SIZE-2)) and (abs(y1 - y2) < (VEHICLE_SIZE-2)):
                return True
    return False

def every_vehicle_reached_end(vehicles):
    for vehicle in vehicles:
        if not vehicle.reached_destination:
            return False
    return True

