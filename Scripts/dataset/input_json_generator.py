import random
import json


def generate_input_config_json(index=0):
    rack_cluster_rows_range = (1, 5)
    rack_cluster_columns_range = (1, 5)
    distance_bw_racks_rows = (10, 500)
    distance_bw_racks_columns = (10, 500)
    rack_rows_range = (1, 5)
    rack_columns_range = (1, 5)
    pallet_offset_x_range = (10, 20)

    rack_cluster_rows = random.randint(*rack_cluster_rows_range)
    rack_cluster_columns = random.randint(*rack_cluster_columns_range)
    distance_bw_racks_rows = random.randint(*distance_bw_racks_rows)
    distance_bw_racks_columns = random.randint(*distance_bw_racks_columns)
    rack_rows = random.randint(*rack_rows_range)
    rack_columns = random.randint(*rack_columns_range)
    pallet_offset_x = random.randint(*pallet_offset_x_range)

    config_json = {
        "cluster": {
            "rows": rack_cluster_rows,
            "columns": rack_cluster_columns,
            "distance": {
                "rows": distance_bw_racks_rows,
                "columns": distance_bw_racks_columns
            },
            "rack": {
                "rows": rack_rows,
                "columns": rack_columns,
                # "frame_obj": rack_frame_obj,
                "tray":
                {
                    # "obj": rack_tray_obj,
                    "pallet": {
                        # "obj": pallet_obj,
                        # "box_objs": box_objs,
                        "offset": {
                            "x": pallet_offset_x,
                            "y": 0,
                            "z": 11
                        }
                    }
                },
            }
        }
    }

    # json dump with indent
    config_json_dump = json.dumps(config_json, indent=2)

    # write to json file
    with open(f"D:\\UnrealProjects\\PCGTools\\Scripts\\dataset\\output\\input\\{index}.json", "w") as f:
        f.write(config_json_dump)
    return config_json


if __name__ == "__main__":
    for i in range(1):
        generate_input_config_json(i)
