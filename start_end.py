from roads import roads
import random

VEHICLE_SIZE = 8
def generate_start():
    """生成隨機的起點"""
    road = random.choice(roads)
    lane = random.choice(road["lanes"])
    if road["type"] == "horizontal":
        start_point = (random.randint(*road["x_range"]),random.randint(lane[0],lane[1]-VEHICLE_SIZE))
    else:
        start_point = (random.randint(lane[0],lane[1]-VEHICLE_SIZE),random.randint(*road["y_range"]))
    return start_point

def generate_end():
    """生成隨機的終點"""
    road = random.choice(roads)
    lane = random.choice(road["lanes"])
    if road["type"] == "horizontal":
        end_point = (random.randint(*road["x_range"]),random.randint(lane[0],lane[1]-VEHICLE_SIZE))
    else:
        end_point = (random.randint(lane[0],lane[1]-VEHICLE_SIZE),random.randint(*road["y_range"]))
    return end_point