import unreal
from .utils import get_objects_map, spawn_obj
from .spawn_boxes import spawn_boxes
from .get_area_obj_list import Box


def spawn_pallet(pallet_obj, box_obj_list,
                 origin_x, origin_y, origin_z):

    pallet_spawn_location = unreal.Vector(
        origin_x, origin_y, origin_z)
    pallet_spawn_rotation = unreal.Rotator(0, 0, 0)
    spawn_obj(pallet_obj["static_mesh_obj"],
              pallet_spawn_location, pallet_spawn_rotation)

    # spawn boxes on the pallet
    spawn_boxes(box_obj_list, (pallet_obj["width"], pallet_obj["length"]),
                origin_x, origin_y, origin_z + pallet_obj["height"])


if __name__ == "__main__":
    objecs_map = get_objects_map(asset_path="/Game/Assets")
    pallet_obj = None
    box_objs = []

    for obj_name, obj in objecs_map.items():
        if "Pallet" in obj_name:
            pallet_obj = obj
        elif "Box" in obj_name:
            box_objs.append(obj)

    box_obj_list = []
    for box_obj in box_objs:
        box_obj_list.append(Box(
            box_obj['static_mesh_obj'],
            box_obj['asset_name'],
            box_obj['length'],
            box_obj['width'],
            box_obj['height'],
            is_rotated=False
        ))
    n = 5
    for i in range(n):
        spawn_pallet(pallet_obj, box_obj_list,
                     i * 200, 0, 0)
