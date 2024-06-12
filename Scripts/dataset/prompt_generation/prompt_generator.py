import json
import os
from gpt_prompts import system_input
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(".env")
client = OpenAI()


def generate_prompt(input_config):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_input},
            {"role": "user", "content": input_config},
        ]
    )
    output = response.choices[0].message.content
    return output


if __name__ == "__main__":
    json_file_dir = "D:\\UnrealProjects\\PCGTools\\Scripts\\dataset\\output\\input"

    json_files = [os.path.join(json_file_dir, f) for f in os.listdir(
        json_file_dir) if f.endswith('.json')]

    # sort files by date creaeted
    json_files.sort(key=os.path.getctime, reverse=False)
    json_files = json_files[100:]
    print("json_files: ", json_files)

    output_dir = "D:\\UnrealProjects\\PCGTools\\Scripts\\testing\\output"
    for index, file in enumerate(json_files):
        with open(file, "r") as f:
            input_config = f.read()
            response = generate_prompt(input_config)
            output_file = os.path.join(output_dir, f"{index}.txt")
            with open(output_file, "w") as f:
                f.write(response)
                print(f"Generated prompt for {file}")
