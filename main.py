# main.py
import pygame
from draw import draw_roads
# from roads import roads
from vehicle import generate_vehicles, car_crash, every_vehicle_reached_end
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
    running = True # add a running flag to control the main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

        # 繪製場景
        draw_roads(screen)
        
        for vehicle in vehicles:
            vehicle.move(vehicles)  # 更新車輛位置
            vehicle.draw(screen)  # 繪製車輛
            vehicle.draw_end(screen)  # 繪製目標位置
        
        # Check for collision or all vehicles reaching their destination
        if car_crash(vehicles):
            with open("simulation_results.txt", "a") as file:
                file.write(f"Collision detected\n")
            running = False  # Exit the main loop

        if every_vehicle_reached_end(vehicles):
            with open("simulation_results.txt", "a") as file:
                file.write(f"Successful\n")
            running = False  # Exit the main loop

        pygame.display.flip()
        clock.tick(30)  # 控制幀率

def ending_simulation(crash, reached):
    if crash:
        with open("simulation_results.txt", "a") as file:
            file.write(f"Collision detected\n")
        pygame.quit()
    
    if reached:
        with open("simulation_results.txt", "a") as file:
            file.write(f"Successful\n")
        pygame.quit()

if __name__ == "__main__":
    main()
