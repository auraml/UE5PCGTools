from .utils import add_objects_to_json
from .spawn_rack import build_rack
import json


def spawn_rack_cluster(config_json):
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


if __name__ == "__main__":
    config_json = None
    file_path = "D:\\UnrealProjects\\PCGTools\\Scripts\\input_json.json"
    with open(file_path, "r") as f:
        config_json = json.load(f)

    config_json = add_objects_to_json(config_json)
    spawn_rack_cluster(config_json)
