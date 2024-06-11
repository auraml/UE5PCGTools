import unreal
import random
import json
from ..utils import get_spawned_actors


def generate_output_json(index=0):
    output_json = {}

    spawned_actors = get_spawned_actors()

    # get transform of each actor
    for actor in spawned_actors:
        location = actor.get_actor_location()
        rotation = actor.get_actor_rotation()
        static_mesh_name = actor.get_component_by_class(
            unreal.StaticMeshComponent).static_mesh.get_name()

        # add to output json
        output_json[actor.get_name()] = {
            "location": {
                "x": location.x,
                "y": location.y,
                "z": location.z
            },
            "rotation": {
                "pitch": rotation.pitch,
                "yaw": rotation.yaw,
                "roll": rotation.roll
            },
            "mesh": static_mesh_name
        }

    # json dump with indent
    output_json = json.dumps(output_json, indent=2)

    # write to json file
    with open(f"D:\\UnrealProjects\\PCGTools\\Scripts\\dataset\\output\\output\\{index}.json", "w") as f:
        f.write(output_json)


if __name__ == "__main__":
    for i in range(1):
        generate_output_json(i)
