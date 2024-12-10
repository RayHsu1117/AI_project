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
    for road in roads:
        roads[road].draw_road(screen)
        roads[road].draw_borders(screen)
    for road_couple in road_couples:
        lane1 = roads[road_couple[0]]
        lane2 = road_couple[1]
        if lane1.direction == 'DOWN':
            pygame.draw.line(screen,(200,200,200),(lane1.x2+3,lane1.y1),(lane1.x2+3,lane1.y2),3)
        elif lane1.direction == 'LEFT':
            pygame.draw.line(screen,(200,200,200),(lane1.x1,lane1.y2+3),(lane1.x2,lane1.y2+3),3) 
    
    pygame.draw.line(screen, BLACK, (0, 0), (600, 0), 2)
    pygame.draw.line(screen, BLACK, (0, 0), (0, 600), 2)
    pygame.draw.line(screen, BLACK, (600, 0), (600, 600), 2)
    pygame.draw.line(screen, BLACK, (0, 600), (600, 600), 2)
    