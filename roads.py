roads = [
    {
        "name": "road1",
        "type": "horizontal",
        "x_range": (0, 800),
        "y_range": (200, 230),
        "lanes": [(203, 213), (216, 227)],
        "separation": [(213, 216)],
        "borders": [(200, 203), (227, 230)]
    },
    {
        "name": "road2",
        "type": "vertical",
        "x_range": (150, 180),
        "y_range": (0, 700),
        "lanes": [(153, 163), (166, 177)],
        "separation": [(163, 166)],
        "borders": [(150, 153), (177, 180)]
    },
    {
        "name": "road3",
        "type": "vertical",
        "x_range": (430, 460),
        "y_range": (0, 700),
        "lanes": [(433, 443), (446, 457)],
        "separation": [(443, 446)],
        "borders": [(430, 433), (457, 460)]
    },
    {
        "name": "road5",
        "type": "horizontal",
        "x_range": (0, 800),
        "y_range": (400, 430),
        "lanes": [(403, 413), (416, 427)],
        "separation": [(413, 416)],
        "borders": [(400, 403), (427, 430)]
    },
]

intersections=[
    {
        "name":"road1_road2",
        "area":(200,230,150,180),
        "zone":
        {
            "1": (153,163,203,213),
            "2": (166,177,203,213),
            "3": (153,163,216,227),
            "4": (166,177,216,227)
        }
    },
    {
        "name":"road1_road3",
        "area":(200,230,430,460),
        "zone":
        {
            "1": (433,443,203,213),
            "2": (446,457,203,213),
            "3": (433,443,216,227),
            "4": (446,457,216,227)
        }
    },
    {
        "name":"road5_road2",
        "area":(150,180,400,430),
        "zone":
        {
            "1": (153,163,403,413),
            "2": (166,177,403,413),
            "3": (153,163,416,427),
            "4": (166,177,416,427)
        }
    },
    {
        "name":"road5_road3",
        "area":(400,430,430,460),
        "zone":
        {
            "1": (433,443,403,413),
            "2": (446,457,403,413),
            "3": (433,443,416,427),
            "4": (446,457,416,427)
        }
    }
]

def get_road_data(road_name):
    for road in roads:
        if road["name"] == road_name:
            return road
    return None

def find_nearest_intersection(current_x,current_y,road_name):
    nearest_intersection = None
    min_distance = float("inf")
    for intersection in intersections:
        distance = (current_x - intersection["area"][0])**2 + (current_y - intersection["area"][2])**2
        if distance < min_distance:
            min_distance = distance
            nearest_intersection = intersection
    return nearest_intersection
  