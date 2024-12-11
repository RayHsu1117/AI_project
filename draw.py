# draw.py
import pygame
from map import roads, intersections, road_couples
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ROAD_COLOR = (128, 128, 128)
YELLOW = (255, 255, 0)

def draw_roads(screen):
    """繪製所有道路"""
    screen.fill(WHITE)
    for intersection in intersections:
        intersections[intersection].draw_intersection(screen) 
    for road_name, road in roads.items():
        road.draw_road(screen)
        road.draw_borders(screen)
        
        # 繪製方向箭頭
        mid_x = (road.x1 + road.x2) // 2
        mid_y = (road.y1 + road.y2) // 2
        draw_arrow(screen, mid_x, mid_y, road.direction)

    for road_couple in road_couples:
        lane1 = roads[road_couple[0]]
        lane2 = road_couple[1]
        if lane1.direction == 'DOWN':
            pygame.draw.line(screen,(200,200,200),(lane1.x2+3,lane1.y1),(lane1.x2+3,lane1.y2),3)
        elif lane1.direction == 'LEFT':
            pygame.draw.line(screen,(200,200,200),(lane1.x1,lane1.y2+3),(lane1.x2,lane1.y2+3),3) 

    # 繪製邊界
    pygame.draw.line(screen, BLACK, (0, 0), (600, 0), 2)
    pygame.draw.line(screen, BLACK, (0, 0), (0, 600), 2)
    pygame.draw.line(screen, BLACK, (600, 0), (600, 600), 2)
    pygame.draw.line(screen, BLACK, (0, 600), (600, 600), 2)

def draw_arrow(screen, x, y, direction):
    """在給定位置繪製箭頭以表示方向"""
    arrow_color = (255, 255, 255)  # 白色箭頭
    arrow_size = 4  # 縮小的箭頭大小
    if direction == "UP":
        points = [(x, y - arrow_size), (x - arrow_size, y + arrow_size), (x + arrow_size, y + arrow_size)]
    elif direction == "DOWN":
        points = [(x, y + arrow_size), (x - arrow_size, y - arrow_size), (x + arrow_size, y - arrow_size)]
    elif direction == "LEFT":
        points = [(x - arrow_size, y), (x + arrow_size, y - arrow_size), (x + arrow_size, y + arrow_size)]
    elif direction == "RIGHT":
        points = [(x + arrow_size, y), (x - arrow_size, y - arrow_size), (x - arrow_size, y + arrow_size)]
    pygame.draw.polygon(screen, arrow_color, points)
    