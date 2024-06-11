import unreal
import json
from ..utils import get_spawned_actors


def generate_output_json(index=0):
    output_json = {}

    spawned_actors = get_spawned_actors()

    for actor in spawned_actors:
        location = actor.get_actor_location()
        static_mesh_name = actor.get_component_by_class(
            unreal.StaticMeshComponent).static_mesh.get_name()
        if static_mesh_name in output_json:
            output_json[static_mesh_name].append(
                [int(location.x), int(location.y), int(location.z)]
            )
        else:
            output_json[static_mesh_name] = [[
                int(location.x), int(location.y), int(location.z)]]

    # json dump with indent
    output_json_dump = json.dumps(output_json, indent=2)

    # write to json file
    with open(f"D:\\UnrealProjects\\PCGTools\\Scripts\\dataset\\output\\output\\{index}.json", "w") as f:
        f.write(output_json_dump)

    return output_json


if __name__ == "__main__":
    for i in range(1):
        generate_output_json(i)
