import unreal

from .spawn_pallet import spawn_pallet
from .utils import get_objects_map, spawn_obj
from .get_area_obj_list import Box


def build_rack(config_json, origin_x, origin_y, origin_z=0):
    rack = config_json["cluster"]["rack"]
    rack_frame_obj = rack["frame_obj"]
    rack_tray_obj = rack["tray"]["obj"]

    rack_rows = rack["rows"]
    rack_columns = rack["columns"]

    rack_frame_sm = rack_frame_obj["static_mesh_obj"]
    rack_frame_height = rack_frame_obj["height"]

    rack_tray_sm = rack_tray_obj["static_mesh_obj"]
    rack_tray_length = rack_tray_obj["length"]
    rack_tray_height = rack_tray_obj["height"]

    # build box objects list
    if "pallet" in rack["tray"]:
        pallet = rack["tray"]["pallet"]
        box_objs = pallet["box_objs"]
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

    for column_index in range(rack_columns):
        for row_index in range(rack_rows):
            # spawn rack frame
            spawn_obj(
                rack_frame_sm,
                unreal.Vector(origin_x + (column_index * rack_tray_length),
                              origin_y + 0,
                              row_index * rack_frame_height),
                unreal.Rotator(0, 0, 0)
            )
            if (column_index == rack_columns - 1):
                spawn_obj(
                    rack_frame_sm,
                    unreal.Vector(origin_x + ((column_index+1) * rack_tray_length),
                                  origin_y + 0,
                                  row_index * rack_frame_height),
                    unreal.Rotator(0, 0, 0)
                )

            # spawn rack tray
            spawn_obj(
                rack_tray_sm,
                unreal.Vector(
                    origin_x + (column_index * rack_tray_length),
                    origin_y + 0,
                    row_index * rack_frame_height
                ),
                unreal.Rotator(0, 0, 0)
            )

            if (row_index == rack_rows - 1):
                spawn_obj(
                    rack_tray_sm,
                    unreal.Vector(
                        origin_x + (column_index * rack_tray_length),
                        origin_y + 0,
                        ((row_index+1) * rack_frame_height) - rack_tray_height
                    ),
                    unreal.Rotator(0, 0, 0)
                )

            # spawn pallets
            if "pallet" in rack["tray"]:
                pallet_obj = pallet["obj"]
                pallet_offset = pallet["offset"]

                spawn_pallet(
                    pallet_obj, box_obj_list,

                    (origin_x + (column_index * rack_tray_length) +
                     pallet_offset["x"]),

                    origin_y + pallet_offset["y"],

                    row_index * rack_frame_height + pallet_offset["z"],
                )

                spawn_pallet(
                    pallet_obj, box_obj_list,

                    (origin_x + (column_index * rack_tray_length) +
                     pallet_offset["x"]*2 + pallet_obj["length"]),

                    origin_y + pallet_offset["y"],

                    row_index * rack_frame_height + pallet_offset["z"]
                )


def spawn_rack():
    objecs_map = get_objects_map(asset_path="/Game/Assets")
    rack_frame_obj = None
    rack_tray_obj = None

    for obj_name, obj in objecs_map.items():
        if "Rack_Frame" in obj_name:
            rack_frame_obj = obj
        elif "Rack_Tray" in obj_name:
            rack_tray_obj = obj

    config_json = {
        "cluster": {
            "rows": 5,
            "columns": 4,

            "distance": {
                "rows": 50,
                "columns": 100
            },
            "rack": {
                "rows": 3,
                "columns": 2,
                "frame_obj": rack_frame_obj,
                "tray":
                {
                    "obj": rack_tray_obj,
                    # "pallet": {
                    #     "obj": pallet_obj,
                    #     "box_objs": box_objs,
                    #     "offset": {
                    #         "x": 20,
                    #         "y": 0,
                    #         "z": 11
                    #     }
                    # }
                },
            }

        }
    }

    build_rack(config_json, 0, 0, 0)


if __name__ == "__main__":
    spawn_rack()
