import sys
import json
import re

def process_json(payload):
    python_obj = json.loads(payload)
    # fetch main branch, head branch, main repo and repo head
    branch_main = python_obj['pull_request']['base']['ref']
    branch_head = python_obj['pull_request']['head']['ref']
    repo_main = python_obj['pull_request']['base']['repo']['full_name']
    repo_head = python_obj['pull_request']['head']['repo']['full_name']
    pull_request_number = python_obj['pull_request']['number']

    return branch_main, branch_head, repo_main, repo_head, pull_request_number
    

def process_added_files(files_added):
    file_parts = []
    has_readme_file = False
    for f in files_added:
        file_parts.append(f.split('/'))
    return file_parts

def main():
    github_token = sys.argv[1]
    payload = sys.argv[2]
    files_added = sys.argv[3]
    files_changed = sys.argv[4]
    files_changed2 = files_changed.split(",")
    files_changed3 = []
    for f in files_changed2:
        files_changed3.append = re.sub(['^\\\"\[\]]+', '', f)
    print(json.dumps({
        "files":files_changed,
        "files2":files_changed2
        }))

    file_parts = process_added_files(files_added)
    file_changed_parts = process_added_files(files_changed)

    branch_main, branch_head, repo_main, repo_head, pull_request_number = process_json(payload)

    print(json.dumps({
        "file-parts": file_parts,
        "files_added" : files_added,
        "files_changed" : files_changed,
        "files_changed_parts" : file_changed_parts,
        "main": branch_main,
        "head" : branch_head,
        "main-repo": repo_main,
        "head-repo": repo_head,
        "pr-num" : pull_request_number
    })) 
    #with open('payload.json') as f:
    

    #process_json(payload)

    

if __name__ == "__main__":
    main()