import json
from ..utils import get_objects_map


def generate_objects_map(index=0):
    output_json = {}

    objs_map = get_objects_map(asset_path="/Game/Assets")
    for index, obj in enumerate(objs_map):
        key = obj
        value = objs_map[obj]

        output_json[key] = {
            "id": index,
            "dimensions": [value["length"], value["width"], value["height"]],
        }

    # json dump with indent
    output_json = json.dumps(output_json, indent=2)

    # write to json file
    with open(f"D:\\UnrealProjects\\PCGTools\\Scripts\\dataset\\output\\objects_map.json", "w") as f:
        f.write(output_json)


if __name__ == "__main__":
    for i in range(1):
        generate_objects_map()
