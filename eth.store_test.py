import subprocess
import json
import sys

def run_program(program):
    try:
        result = subprocess.run(program, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing Go program {program}: {e}")
        return None
    
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

    days = config.get("days", [])

    start_day = days.get("start_day")
    end_day = days.get("end_day")
    batch_size = days.get("batch_size")
    
    if end_day < start_day or batch_size < 1:
        print(f"Error: Invalid configuration: start_day = {start_day}, end_day = {end_day}, batch_size = {batch_size}")
        sys.exit(1)

    go_command = config.get("go_command", []) + [f"-days={start_day},{end_day}"]
    dotnet_command = config.get("dotnet_command", []) + [f"-days={start_day},{end_day}"]

    for i in range(start_day, end_day + 1, batch_size):    
        go_results = run_program(go_command)
        dotnet_results = run_program(dotnet_command)
        print(go_results, dotnet_results)   

        if go_results != dotnet_results:
            print(f"Error: eth.store results = {go_results} != eth.store.net = {dotnet_results}")
                        
    print("All tests passed")
    sys.exit(0)




