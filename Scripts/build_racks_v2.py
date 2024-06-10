import unreal

from .spawn_box_on_pallet import spawn_pallet


def get_mesh_obj(static_mesh):
    sm_name = static_mesh.get_name()
    sm_bbox = static_mesh.get_bounding_box()

    # get min max vectors from sm_bbox
    min_vec = sm_bbox.min
    max_vec = sm_bbox.max

    # get absolute value of the difference between min and max vectors
    diff_vec = (max_vec - min_vec)
    diff_vec_x = int(diff_vec.x)
    diff_vec_y = int(diff_vec.y)
    diff_vec_z = int(diff_vec.z)

    # get pivot location of the static mesh
    pivot = static_mesh.get_bounds().origin

    return {
        "static_mesh_obj": static_mesh,
        "asset_name": sm_name,
        "length": diff_vec_x,
        "width": diff_vec_y,
        "height": diff_vec_z
    }


def get_objects_map(asset_path="/Game/Assets"):
    objects_map = {}

    # get a list of all Assets in the path.
    all_assets = unreal.EditorAssetLibrary.list_assets(asset_path)
    # load them all into memory.
    all_assets_loaded = [
        unreal.EditorAssetLibrary.load_asset(a) for a in all_assets]
    # filter the list to include only Static Meshes.
    static_mesh_assets = unreal.EditorFilterLibrary.by_class(
        all_assets_loaded, unreal.StaticMesh)

    for static_mesh in static_mesh_assets:
        objects_map[static_mesh.get_name()] = get_mesh_obj(static_mesh)
    # print(objects_map)
    return objects_map


def spawn_obj(static_mesh_obj, spawn_location, spawn_rotation):
    unreal.EditorLevelLibrary.spawn_actor_from_object(
        static_mesh_obj,
        spawn_location,
        spawn_rotation
    )


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
                pallet = rack["tray"]["pallet"]
                pallet_obj = pallet["obj"]
                box_objs = pallet["box_objs"]
                pallet_offset = pallet["offset"]

                spawn_pallet(
                    pallet_obj, box_objs,

                    (origin_x + (column_index * rack_tray_length) +
                     pallet_offset["x"]),

                    origin_y + pallet_offset["y"],

                    row_index * rack_frame_height + pallet_offset["z"],
                )

                spawn_pallet(
                    pallet_obj, box_objs,

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
            "columns": 2,
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


# spawn_rack()
spawn_rack_cluster()
