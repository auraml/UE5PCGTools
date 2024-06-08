import numpy as np
import matplotlib.pyplot as plt
import random


class PickedArea:
    def __init__(self, x1, y1, x2, y2, length, width):
        self.x1 = x1
        self.y1 = y1

        self.x2 = x2
        self.y2 = y2

        self.length = length
        self.width = width


# List of 2D areas with dimensions
areas_dimension_list = [
    (40, 50),
    (20, 40),
    (20, 20),
    (40, 80)
]

# append reverse of each area to the list
areas_dimension_list.extend([(area[1], area[0])
                            for area in areas_dimension_list])


# Total 2D area
total_area = (100, 100)

# create empty grid filled with 0 of size total_area
grid = [[0 for _ in range(total_area[0])] for _ in range(total_area[1])]


def get_all_biggest_empty_rectangles_from_grid():
    empty_rectangles = []

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                # check if the current cell is already present inside any of the empty rectangles
                is_present = False
                for empty_rectangle in empty_rectangles:
                    if empty_rectangle[0] <= i < empty_rectangle[2] and empty_rectangle[1] <= j < empty_rectangle[3]:
                        is_present = True
                        break
                if not is_present:
                    x1, y1 = i, j
                    x2, y2 = i + 1, j + 1

                    # check how far the empty rectangle can go in the x direction
                    while x2 < len(grid) and grid[x2][j] == 0:
                        x2 += 1

                    # check how far the empty rectangle can go in the y direction and
                    while y2 < len(grid[0]) and all(grid[k][y2] == 0 for k in range(x1, x2)):
                        y2 += 1

                    empty_rectangles.append((x1, y1, x2, y2))

    # shuffle the empty rectangles
    random.shuffle(empty_rectangles)
    return empty_rectangles


def get_area_obj_list():
    global grid, areas_dimension_list

    area_obj_list = []

    max_tries = 20
    while max_tries > 0:
        random.shuffle(areas_dimension_list)
        for picked_area in areas_dimension_list:
            available_grids = get_all_biggest_empty_rectangles_from_grid()

            if len(available_grids) == 0:
                print("No more space left")
                return area_obj_list

            # check if the picked area fits in any of the available grids
            for available_grid in available_grids:
                x1, y1, x2, y2 = available_grid
                if x2 - x1 >= picked_area[0] and y2 - y1 >= picked_area[1]:
                    # yes, it can fit

                    # with margin
                    margin_x = x2 - x1 - picked_area[0]
                    margin_y = y2 - y1 - picked_area[1]
                    rand_x = random.randint(0, margin_x)
                    rand_y = random.randint(0, margin_y)
                    picked_x1 = x1 + rand_x
                    picked_y1 = y1 + rand_y
                    picked_x2 = picked_x1 + picked_area[0]
                    picked_y2 = picked_y1 + picked_area[1]

                    # without margin
                    # picked_x1 = x1
                    # picked_y1 = y1
                    # picked_x2 = picked_x1 + picked_area[0]
                    # picked_y2 = picked_y1 + picked_area[1]

                    area_obj_list.append(PickedArea(
                        picked_x1, picked_y1, picked_x2, picked_y2,
                        picked_area[0], picked_area[1]))

                    print(
                        f"Area {picked_area} fits at ({picked_x1}, {picked_y1}), ({picked_x2}, {picked_y2})")

                    for i in range(picked_x1, picked_x2):
                        for j in range(picked_y1, picked_y2):
                            grid[i][j] = 1
                    break
        max_tries -= 1

    # print area_obj_list
    print("\nArea objects: ")
    for each in area_obj_list:
        print(each.x1, each.y1, each.x2, each.y2,
              " dims:", each.length, each.width)

    return area_obj_list


area_obj_list = get_area_obj_list()
colors = ['red', 'blue', 'green', 'purple', 'black', 'orange', 'pink',
          'magenta', 'brown', 'gray', 'olive', 'teal', 'navy']

# for each in area_obj_list - plot areas in different colors with area number in the center
for i, each in enumerate(area_obj_list):
    plt.fill([each.x1, each.x2, each.x2, each.x1], [
             each.y1, each.y1, each.y2, each.y2], colors[i % len(colors)])
    plt.text((each.x1 + each.x2) / 2, (each.y1 + each.y2) / 2, str(i + 1),
             horizontalalignment='center', verticalalignment='center', fontsize=12, color='white')
plt.xlim(0, total_area[0])
plt.ylim(0, total_area[1])
plt.gca().invert_yaxis()
plt.show()
