import json
from .utils import spawn_obj, get_objects_map, clear_level
import unreal

objecs_map = get_objects_map(asset_path="/Game/Assets")


def get_object_from_sm_name(sm_name):
    for obj_name, obj in objecs_map.items():
        if sm_name in obj_name:
            return obj["static_mesh_obj"]
    return None


if __name__ == "__main__":
    clear_level()

    with open("D:\\UnrealProjects\\PCGTools\\Scripts\\dataset\\llama3_output.json", "r") as f:
        output_json = json.load(f)

        for sm_name in output_json:
            sm_obj = get_object_from_sm_name(sm_name)
            if (sm_obj is None):
                continue

            transform_list = output_json[sm_name]
            for transform in transform_list:
                spawn_location = unreal.Vector(
                    transform[0], transform[1], transform[2])
                spawn_rotation = unreal.Rotator(0, 0, 0)
                spawn_obj(
                    sm_obj,
                    spawn_location,
                    spawn_rotation
                )
