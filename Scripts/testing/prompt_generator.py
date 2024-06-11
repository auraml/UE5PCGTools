from ..utils import clear_level, add_objects_to_json
from ..spawn_racks_cluster import spawn_rack_cluster
from ..dataset.input_json_generator import generate_input_config_json
from ..dataset.output_json_generator import generate_output_json

import json


def generate_prompt(config_json):
    ...


if __name__ == "__main__":
    # read json file
    with open("D:\\UnrealProjects\\PCGTools\\Scripts\\input_json.json", "r") as f:
        input_config = json.load(f)
        generate_prompt(json.loads(input_config))


"""
{
  "cluster": {
    "rows": 1,
    "columns": 4,
    "distance": {
      "rows": 411,
      "columns": 383
    },
    "rack": {
      "rows": 2,
      "columns": 3,
      "tray": {
        "pallet": {
          "offset": {
            "x": 19,
            "y": 0,
            "z": 11
          }
        }
      }
    }
  }
}
"""
