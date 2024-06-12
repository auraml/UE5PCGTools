system_input = """You are an expert 3D engineer. Given an input JSON file describing a racks cluster system, your task is to write a concise text prompt with keys and values to help a language model clearly understand and then build a 3D racks system from it.

The racks cluster includes the following five components:

1. Cluster: Comprising multiple racks arranged in rows and columns.
2. Rack: Each rack is constructed using a Rack Frame and Rack Trays based on specified rows and columns.
3. Tray: Trays within a rack where pallets are placed.
4. Pallet: Positioned on trays, each pallet holds boxes.
5. Box: Boxes are randomly arranged on top of each pallet.

The output text prompt should be brief, selectively including some, but not all, key details from the input JSON.

Ensure each output is unique, employing different wording and phrases to describe the keys and values for the input JSON.
"""


user_input = '''
{
  "cluster": {
    "rows": 2,
    "columns": 5,
    "distance": {
      "rows": 133,
      "columns": 480
    },
    "rack": {
      "rows": 3,
      "columns": 4,
      "tray": {
        "pallet": {
          "offset": {
            "x": 13,
            "y": 0,
            "z": 11
          }
        }
      }
    }
  }
}
'''
