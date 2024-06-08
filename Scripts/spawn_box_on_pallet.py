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


def spawn_boxes_on_pallet(pallet_obj, box_objs,
                          start_i=0, i_distance_multiplier=100):
    from .get_area_obj_list import get_area_obj_list, Box, plot_area_in_grid

    pallet_spawn_location = unreal.Vector(
        start_i * i_distance_multiplier, 0, 0)
    pallet_spawn_rotation = unreal.Rotator(0, 0, 0)
    spawn_obj(pallet_obj["static_mesh_obj"],
              pallet_spawn_location, pallet_spawn_rotation)

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
        # box_obj_list.append(Box(
        #     box_obj['static_mesh_obj'],
        #     box_obj['asset_name'],
        #     box_obj['length'],
        #     box_obj['width'],
        #     box_obj['height'],
        #     is_rotated=True
        # ))

    area_obj_list = get_area_obj_list(
        (pallet_obj['width'], pallet_obj['length']),
        pallet_obj['height'],
        box_obj_list,
        is_with_margin=True,
        start_i=start_i,
        i_distance_multiplier=i_distance_multiplier
    )

    for each in area_obj_list:
        print(
            f"Start spawning, {each.box_obj.asset_name} at {each.x1}, {each.y1}, {each.z1}")
        spawn_obj(each.box_obj.static_mesh_obj,
                  unreal.Vector(each.x1, each.y1, each.z1),
                  unreal.Rotator(0, 0, 0))

    # plot_area_in_grid(
    #     area_obj_list, (pallet_obj['length'], pallet_obj['width']))


def spawn(n=1):
    objecs_map = get_objects_map(asset_path="/Game/Assets")
    pallet_obj = None
    box_objs = []

    for obj_name, obj in objecs_map.items():
        if "Pallet" in obj_name:
            pallet_obj = obj
        elif "Box" in obj_name:
            box_objs.append(obj)
    for i in range(n):
        spawn_boxes_on_pallet(pallet_obj, box_objs, i, 200)


spawn(n=5)
