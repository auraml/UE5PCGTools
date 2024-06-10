import random


class Box:
    def __init__(self, static_mesh_obj, asset_name, length, width, height, is_rotated=False):
        self.static_mesh_obj = static_mesh_obj
        self.asset_name = asset_name

        self.length = length
        self.width = width
        self.height = height

        self.is_rotated = is_rotated


class PickedVolume:
    def __init__(self, x1, y1, z1, x2, y2, z2, box_obj):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1

        self.x2 = x2
        self.y2 = y2
        self.z2 = z2

        self.box_obj = box_obj


def get_all_biggest_empty_rectangles_from_grid(grid):
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


def get_area_obj_list(total_area, box_obj_list,
                      is_with_margin=True,
                      origin_x=0, origin_y=0, origin_z=0):
    # create empty grid filled with 0 of size total_area
    grid = [[0 for _ in range(total_area[0])] for _ in range(total_area[1])]

    area_obj_list = []

    max_tries = 3
    while max_tries > 0:
        random.shuffle(box_obj_list)
        for picked_box_obj in box_obj_list:
            available_grids = get_all_biggest_empty_rectangles_from_grid(grid)

            if len(available_grids) == 0:
                print("No more space left")
                return area_obj_list

            # check if the picked area fits in any of the available grids
            for available_grid in available_grids:
                x1, y1, x2, y2 = available_grid
                if x2 - x1 >= picked_box_obj.length and y2 - y1 >= picked_box_obj.width:
                    # yes, it can fit

                    if is_with_margin:
                        # with margin
                        margin_x = x2 - x1 - picked_box_obj.length
                        margin_y = y2 - y1 - picked_box_obj.width
                        rand_x = random.randint(0, margin_x)
                        rand_y = random.randint(0, margin_y)
                        picked_x1 = x1 + rand_x
                        picked_y1 = y1 + rand_y
                        picked_x2 = picked_x1 + picked_box_obj.length
                        picked_y2 = picked_y1 + picked_box_obj.width
                    else:
                        # without margin
                        picked_x1 = x1
                        picked_y1 = y1
                        picked_x2 = picked_x1 + picked_box_obj.length
                        picked_y2 = picked_y1 + picked_box_obj.width

                    area_obj_list.append(PickedVolume(
                        (origin_x) + picked_x1,
                        (origin_y) + picked_y1,
                        (origin_z),
                        (origin_x) + picked_x2,
                        (origin_y) + picked_y2,
                        (origin_z) + picked_box_obj.height,
                        picked_box_obj))

                    for i in range(picked_x1, picked_x2):
                        for j in range(picked_y1, picked_y2):
                            grid[i][j] = 1
                    break
        max_tries -= 1

    # # print area_obj_list
    # print("\nArea objects: ")
    # for each in area_obj_list:
    #     print(each.x1, each.y1, each.z1,
    #           each.x2, each.y2, each.z2,
    #           each.box_obj.asset_name)

    return area_obj_list


def plot_area_in_grid(area_obj_list, total_area):
    import matplotlib.pyplot as plt
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


if __name__ == "__main__":
    # List of 2D areas with dimensions
    box_obj_list = [
        Box("box1", "Box 1", 20, 20, 20, False),
        Box("box2", "Box 2", 20, 20, 20, True),

        Box("box3", "Box 3", 40, 50, 20, False),
        Box("box4", "Box 4", 40, 50, 20, True),

        Box("box5", "Box 5", 20, 40, 20, False),
        Box("box6", "Box 6", 20, 40, 20, True),

        Box("box7", "Box 7", 40, 80, 20, False),
        Box("box8", "Box 8", 40, 80, 20, True)
    ]

    # Total 2D area
    pallet_dims = [100, 100, 20]
    total_area = [pallet_dims[0], pallet_dims[1]]
    initial_height = pallet_dims[2]  # pallet height

    area_obj_list = get_area_obj_list(
        total_area,
        box_obj_list,
        True,
        0, 0, initial_height)
    plot_area_in_grid(area_obj_list, total_area)
