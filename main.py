# main.py
import pygame
from draw import draw_roads
from vehicle import generate_vehicle
from map import roads, intersections, ROAD_WIDTH # 導入道路資料
import random

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((600, 600))

# 設定要初始化幾台車
how_many_cars = 1
# 初始化車輛s
vehicles = []
for i in range(how_many_cars):
    vehicle = generate_vehicle()
    vehicles.append(vehicle)

def create_directed_graph_with_turning(roads, intersections, segment_length=40):
    """
    創建一個包含十字路口轉彎處理的有向圖。
    :param roads: 道路物件的字典
    :param intersections: 路口物件的字典
    :param segment_length: 每段道路劃分的節點距離
    :return: 有向圖
    """
    graph = {}
    
    # 遍歷所有道路，離散化道路為若干節點
    for road_name, road in roads.items():
        # 根據方向劃分道路節點
        if road.direction in ['LEFT', 'RIGHT']:
            num_segments = (road.x2 - road.x1) // segment_length
            for i in range(num_segments + 1):
                node = (road.x1 + i * segment_length, road.y1)
                if node not in graph:
                    graph[node] = []

                # 與下一節點連接
                if i < num_segments:
                    next_node = (road.x1 + (i + 1) * segment_length, road.y1)
                    graph[node].append(next_node)
                    graph[next_node] = graph.get(next_node, [])
                    graph[next_node].append(node)

        elif road.direction in ['UP', 'DOWN']:
            num_segments = (road.y2 - road.y1) // segment_length
            for i in range(num_segments + 1):
                node = (road.x1, road.y1 + i * segment_length)
                if node not in graph:
                    graph[node] = []

                # 與下一節點連接
                if i < num_segments:
                    next_node = (road.x1, road.y1 + (i + 1) * segment_length)
                    graph[node].append(next_node)
                    graph[next_node] = graph.get(next_node, [])
                    graph[next_node].append(node)
    
    # 添加路口節點
    for intersection_name, intersection in intersections.items():
        intersection_center = ((intersection.x1 + intersection.x2) // 2, (intersection.y1 + intersection.y2) // 2)
        if intersection_center not in graph:
            graph[intersection_center] = []

        # 添加過渡節點
        turning_nodes = generate_turning_nodes(intersection)
        graph.update(turning_nodes)

    return graph


def generate_turning_nodes(intersection):
    """
    生成路口的過渡節點，用於處理右轉和左轉。
    只生成與實際道路相連的方向的過渡節點。
    :param intersection: 路口物件
    :return: 過渡節點的鄰接表結構
    """
    x_center = (intersection.x1 + intersection.x2) // 2
    y_center = (intersection.y1 + intersection.y2) // 2
    nodes = {}

    # 檢查路口的四個方向是否有道路連接
    connected_directions = {
        "UP": any(
            road.direction == "DOWN" and road.x1 <= x_center <= road.x2 and road.y2 == intersection.y1
            for road in roads.values()
        ),
        "DOWN": any(
            road.direction == "UP" and road.x1 <= x_center <= road.x2 and road.y1 == intersection.y2
            for road in roads.values()
        ),
        "LEFT": any(
            road.direction == "RIGHT" and road.y1 <= y_center <= road.y2 and road.x2 == intersection.x1
            for road in roads.values()
        ),
        "RIGHT": any(
            road.direction == "LEFT" and road.y1 <= y_center <= road.y2 and road.x1 == intersection.x2
            for road in roads.values()
        ),
    }

    # 添加過渡節點，僅對連接的方向生效
    if connected_directions["RIGHT"]:
        right_turn_node = (x_center + ROAD_WIDTH, y_center)
        nodes[right_turn_node] = [(x_center, y_center)]
        nodes[(x_center, y_center)] = nodes.get((x_center, y_center), []) + [right_turn_node]
    if connected_directions["LEFT"]:
        left_turn_node = (x_center - ROAD_WIDTH, y_center)
        nodes[left_turn_node] = [(x_center, y_center)]
        nodes[(x_center, y_center)] = nodes.get((x_center, y_center), []) + [left_turn_node]
    if connected_directions["UP"]:
        up_turn_node = (x_center, y_center - ROAD_WIDTH)
        nodes[up_turn_node] = [(x_center, y_center)]
        nodes[(x_center, y_center)] = nodes.get((x_center, y_center), []) + [up_turn_node]
    if connected_directions["DOWN"]:
        down_turn_node = (x_center, y_center + ROAD_WIDTH)
        nodes[down_turn_node] = [(x_center, y_center)]
        nodes[(x_center, y_center)] = nodes.get((x_center, y_center), []) + [down_turn_node]

    return nodes

# 主程序
def main():

    print("Start")
    intersection = intersections['intersection_1']
    turning_nodes = generate_turning_nodes(intersection)
    
    if turning_nodes is None:
        print("No turning nodes generated.")
    else:
        print("Turning nodes generated.")

    for node, neighbors in turning_nodes.items():
        print(f"路口節點: {node}, 鄰居: {neighbors}")
        print("Hi")

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # 繪製場景
        draw_roads(screen)
        
        for vehicle in vehicles:
            vehicle.move("UP")
            vehicle.draw(screen)
            vehicle.draw_end(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
