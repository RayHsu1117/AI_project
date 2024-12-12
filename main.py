# main.py
import pygame
from draw import draw_roads
# from roads import roads
from vehicle import generate_vehicles
import random

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((602, 602))

# 初始化車輛
VEHICLE_AMOUNT = 10
vehicles = generate_vehicles(VEHICLE_AMOUNT)

# 主程式
def main():
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = True
                for vehicle in vehicles:
                    if vehicle.reached_destination == False:
                        flag = False
                        print("There is a vehicle not achieving arrival. ID: "+str(vehicle.vehicle_id))
                if flag == True:
                    print("All vehicles arrived.")
                pygame.quit()
                return

        # 繪製場景
        draw_roads(screen)
        
        for vehicle in vehicles:
            vehicle.move(vehicles)  # 更新車輛位置
            vehicle.draw(screen)  # 繪製車輛
            vehicle.draw_end(screen)  # 繪製目標位置

        pygame.display.flip()
        clock.tick(30)  # 控制幀率

if __name__ == "__main__":
    main()
