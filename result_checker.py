import json
import sys

def validate_results():
    try:
        with open('results/github_runner.json') as f:
            data = json.load(f)
        
        if not data.get('correctly_sorted', False):
            print("Error: Sorting validation failed!")
            return 1
            
        print("Validation passed: Results are correctly sorted")
        return 0
        
    except FileNotFoundError:
        print("Error: Results file not found")
        return 1
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in results file")
        return 1

if __name__ == "__main__":
    sys.exit(validate_results())
