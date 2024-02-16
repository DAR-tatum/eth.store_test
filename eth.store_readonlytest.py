import json
import sys

# TODO: Add logging to replace print statements
  
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python eth.storetest.py <config_file_path>")
        sys.exit(1)

    config_file_path = sys.argv[1]

    # Read config from JSON file
    try:
        with open(config_file_path, "r") as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        print(f"Error: Config file {config_file_path} not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in config file {config_file_path}: {e}")
        sys.exit(1)
        
    with open(config.get("go_file"), "r") as go_file:
        go_lines = go_file.readlines()
    with open(config.get("dotnet_file"), "r") as dotnet_file:
        dotnet_lines = dotnet_file.readlines()
    
    for i in range(len(go_lines)):
        if go_lines[i] != dotnet_lines[i]:
            print(f"Error: eth.store results = {go_lines[i]} != eth.store.net = {dotnet_lines[i]}")
            sys.exit(1)
    
    print("All tests passed")
    sys.exit(0)