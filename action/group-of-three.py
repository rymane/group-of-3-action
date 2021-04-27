import sys
import json

def process_json(payload):
    python_obj = json.load(payload)
    # fetch main branch, head branch, main repo and repo head
    branch_main = python_obj["pull_request"]["base"]["ref"]
    branch_head = python_obj["pull_request"]["head"]["ref"]
    repo_main = python_obj["pull_request"]["base"]["repo"]["full_name"]
    repo_head = python_obj["pull_request"]["head"]["repo"]["full_name"]
    pull_request_number = python_obj["pull_request"]["number"]

    return branch_main, branch_head, repo_main, repo_head, pull_request_number
    

def process_added_files(files_added):
    
    has_readme_file = False
    file_parts = []
    for f in files_added:
        file_parts.append(f.split('/'))

    print(json.dumps('\\'))

    print(json.dumps({
        "file-parts": file_parts
    }))    


def main():
    github_token = sys.argv[1]
    payload = sys.argv[2]
    process_added_files(sys.argv[3])
    files_changed = sys.argv[4]
    #with open('payload.json') as f:
    branch_main, branch_head, repo_main, repo_head, pull_request_number = process_json(payload)

    #process_json(payload)

main()