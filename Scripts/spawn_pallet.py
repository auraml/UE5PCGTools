import unreal
from .utils import get_objects_map, spawn_obj
from .spawn_boxes import spawn_boxes


def spawn_pallet(pallet_obj, box_objs,
                 origin_x, origin_y, origin_z):

    pallet_spawn_location = unreal.Vector(
        origin_x, origin_y, origin_z)
    pallet_spawn_rotation = unreal.Rotator(0, 0, 0)
    spawn_obj(pallet_obj["static_mesh_obj"],
              pallet_spawn_location, pallet_spawn_rotation)

    # spawn boxes on the pallet
    spawn_boxes(box_objs, (pallet_obj["width"], pallet_obj["length"]),
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
    n = 5
    for i in range(n):
        spawn_pallet(pallet_obj, box_objs,
                     i * 200, 0, 0)
