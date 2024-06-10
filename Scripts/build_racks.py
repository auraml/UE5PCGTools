import unreal


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


def build_rack(rack_frame_obj, rack_tray_obj,
               origin_x, origin_y,
               rack_rows=2, rack_columns=2,
               top_shelf_height_offset=16):
    rack_frame = rack_frame_obj["static_mesh_obj"]
    rack_frame_length = rack_frame_obj["length"]
    rack_frame_width = rack_frame_obj["width"]
    rack_frame_height = rack_frame_obj["height"]

    rack_tray = rack_tray_obj["static_mesh_obj"]
    rack_tray_length = rack_tray_obj["length"]
    rack_tray_width = rack_tray_obj["width"]
    rack_tray_height = rack_tray_obj["height"]

    for column_index in range(rack_columns):
        for row_index in range(rack_rows):
            # spawn rack frame
            spawn_obj(
                rack_frame,
                unreal.Vector(origin_x + (column_index * rack_tray_length),
                              origin_y + 0,
                              row_index * rack_frame_height),
                unreal.Rotator(0, 0, 0)
            )
            if (column_index == rack_columns - 1):
                spawn_obj(
                    rack_frame,
                    unreal.Vector(origin_x + ((column_index+1) * rack_tray_length),
                                  origin_y + 0,
                                  row_index * rack_frame_height),
                    unreal.Rotator(0, 0, 0)
                )

            # spawn rack tray
            spawn_obj(
                rack_tray,
                unreal.Vector(
                    origin_x + (column_index * rack_tray_length),
                    origin_y + 0,
                    row_index * rack_frame_height
                ),
                unreal.Rotator(0, 0, 0)
            )

            if (row_index == rack_rows - 1):
                spawn_obj(
                    rack_tray,
                    unreal.Vector(
                        origin_x + (column_index * rack_tray_length),
                        origin_y + 0,
                        ((row_index+1) * rack_frame_height) -
                        top_shelf_height_offset
                    ),
                    unreal.Rotator(0, 0, 0)
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

    build_rack(rack_frame_obj, rack_tray_obj,
               0, 0,
               5, 10,
               16)


def build_rack_cluster(cluster_rows, cluster_columns,
                       distance_bw_cluster_rows, distance_bw_cluster_columns,
                       rack_frame_obj, rack_tray_obj,
                       rack_rows=2, rack_columns=2,
                       top_shelf_height_offset=16
                       ):
    for cluster_row_index in range(cluster_rows):
        for cluster_column_index in range(cluster_columns):
            origin_x = cluster_column_index * (
                distance_bw_cluster_columns + rack_columns * rack_tray_obj["length"])
            origin_y = cluster_row_index * (
                distance_bw_cluster_rows + rack_frame_obj["width"])

            build_rack(rack_frame_obj, rack_tray_obj,
                       origin_x, origin_y,
                       rack_rows, rack_columns,
                       top_shelf_height_offset)


def spawn_rack_cluster():
    objecs_map = get_objects_map(asset_path="/Game/Assets")
    rack_frame_obj = None
    rack_tray_obj = None

    for obj_name, obj in objecs_map.items():
        if "Rack_Frame" in obj_name:
            rack_frame_obj = obj
        elif "Rack_Tray" in obj_name:
            rack_tray_obj = obj

    build_rack_cluster(
        5, 4,
        50, 100,
        rack_frame_obj, rack_tray_obj,
        3, 4,
        16
    )


# spawn_rack()
spawn_rack_cluster()
