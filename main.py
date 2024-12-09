# main.py
import pygame
from draw import draw_roads
# from roads import roads
from vehicle import generate_vehicle
import random

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((600, 600))

# 初始化車輛

vehicles = []
for i in range(5):
    vehicle = generate_vehicle()
    print(type(vehicle))
    vehicles.append(vehicle)
# 主程序
def main():
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # 繪製場景
        draw_roads(screen)
        
        for vehicle in vehicles:
            # vehicle.move()
            vehicle.draw(screen)
            vehicle.draw_end(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
