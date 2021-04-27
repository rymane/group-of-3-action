import sys
import json

def process_json(payload):
    python_obj = json.load(payload)
    print(python_obj)
    
def main():
    github_token = sys.argv[1]
    payload = sys.argv[2]
    files_added = sys.argv[3]
    files_changed = sys.argv[4]
    process_json(payload)

main()
