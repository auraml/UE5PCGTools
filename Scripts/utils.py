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
        # filter by SM name
        name = static_mesh.get_name()
        if "Rack" in name or "Pallet" in name or "Box" in name:
            objects_map[static_mesh.get_name()] = get_mesh_obj(static_mesh)
    return objects_map


def spawn_obj(static_mesh_obj, spawn_location, spawn_rotation):
    new_actor = unreal.EditorLevelLibrary.spawn_actor_from_object(
        static_mesh_obj,
        spawn_location,
        spawn_rotation
    )
    return new_actor


def add_objects_to_json(config_json):
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

    config_json["cluster"]["rack"]["frame_obj"] = rack_frame_obj
    config_json["cluster"]["rack"]["tray"]["obj"] = rack_tray_obj
    config_json["cluster"]["rack"]["tray"]["pallet"]["obj"] = pallet_obj
    config_json["cluster"]["rack"]["tray"]["pallet"]["box_objs"] = box_objs
    return config_json


def get_spawned_actors():
    spawned_actors = []
    editor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    actors = editor_subsystem.get_all_level_actors()

    for actor in actors:
        static_mesh_components = actor.get_components_by_class(
            unreal.StaticMeshComponent)

        for smc in static_mesh_components:
            static_mesh_name = smc.static_mesh.get_name()
            if ("Rack" in static_mesh_name or
                    "Box" in static_mesh_name or
                    "Pallet" in static_mesh_name):
                spawned_actors.append(actor)
    return spawned_actors


def clear_level():
    actors = get_spawned_actors()
    for actor in actors:
        actor.destroy_actor()


if __name__ == "__main__":
    # print(get_objects_map(asset_path="/Game/Assets"))
    # clear_level()
    ...
