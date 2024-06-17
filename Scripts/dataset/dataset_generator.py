from ..utils import clear_level, add_objects_to_json
from ..spawn_racks_cluster import spawn_rack_cluster
from .input_json_generator import generate_input_config_json
from .output_json_generator import generate_output_json
from datetime import datetime

if __name__ == "__main__":
    clear_level()
    for i in range(0, 1000):
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        print(f"Generating dataset {i}: {current_time}")
        clear_level()
        config_json = generate_input_config_json(i)
        config_json_with_objs = add_objects_to_json(config_json)
        spawn_rack_cluster(config_json_with_objs)
        generate_output_json(i)
