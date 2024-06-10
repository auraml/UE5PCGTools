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


if __name__ == "__main__":
    print(get_objects_map(asset_path="/Game/Assets"))
