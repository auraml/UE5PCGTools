from .utils import get_objects_map
from .spawn_rack import build_rack


def build_rack_cluster(config_json):
    cluster = config_json["cluster"]
    cluster_rows = cluster["rows"]
    cluster_columns = cluster["columns"]

    distance_bw_cluster_rows = cluster["distance"]["rows"]
    distance_bw_cluster_columns = cluster["distance"]["columns"]

    rack = cluster["rack"]
    rack_columns = rack["columns"]

    rack_frame_obj = rack["frame_obj"]
    rack_tray_obj = rack["tray"]["obj"]

    for cluster_row_index in range(cluster_rows):
        for cluster_column_index in range(cluster_columns):
            origin_x = cluster_column_index * (
                distance_bw_cluster_columns + rack_columns * rack_tray_obj["length"])
            origin_y = cluster_row_index * (
                distance_bw_cluster_rows + rack_frame_obj["width"])
            build_rack(config_json, origin_x, origin_y, 0)


def spawn_rack_cluster():
    objecs_map = get_objects_map(asset_path="/Game/Assets")
    rack_frame_obj = None
    rack_tray_obj = None
    pallet_obj = None
    box_objs = []

    for obj_name, obj in objecs_map.items():
        if "Rack_Frame" in obj_name:
            rack_frame_obj = obj
        elif "Rack_Tray" in obj_name:
            rack_tray_obj = obj
        elif "Pallet" in obj_name:
            pallet_obj = obj
        elif "Box" in obj_name:
            box_objs.append(obj)

    config_json = {
        "cluster": {
            "rows": 3,
            "columns": 4,
            "distance": {
                "rows": 200,
                "columns": 100
            },
            "rack": {
                "rows": 3,
                "columns": 2,
                "frame_obj": rack_frame_obj,
                "tray":
                {
                    "obj": rack_tray_obj,
                    "pallet": {
                        "obj": pallet_obj,
                        "box_objs": box_objs,
                        "offset": {
                            "x": 15,
                            "y": 0,
                            "z": 11
                        }
                    }
                },
            }
        }
    }

    build_rack_cluster(config_json)


if __name__ == "__main__":
    spawn_rack_cluster()
