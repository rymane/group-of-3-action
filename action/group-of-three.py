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
    

def process_added_files(files):
    file_parts = []
    for f in files:
        file_parts.append(f.split('/'))
    return file_parts

def check_student_pr(files):
    valid = True
    valid_files = []
    valid_tasks = ['course-automation', 'demo', 'essay', 'executable-tutorial', 'feedback', 'open-source', 'presentation']
    task = ""
    num_students = -1
    for f in files:
        if not len(f) >= 4:
            valid = False
        if f[0] != 'contributions':
            valid = False
        if f[1] not in valid_tasks:
            valid = False
        if not 1 <= len(f[2].split('-')) <= 3:
            valid = False
        valid_files.append(valid)
        valid = True

    for i, vf in valid_files:
        # get task and number of studens from first valid changed/added file
        if vf == True:
            task = files[i][1]
            num_students = len(files[i][2].split('-'))
            break

    return valid_files, task, num_students

def main():
    github_token = sys.argv[1]
    payload = sys.argv[2]
    files_added = re.sub('[\\\"\[\]]+', '', sys.argv[3]).split(',')
    files_changed = re.sub('[\\\"\[\]]+', '', sys.argv[4]).split(',')

    file_added_parts = process_added_files(files_added)
    file_changed_parts = process_added_files(files_changed)

    files_parts = file_added_parts
    for f in file_changed_parts:
        files_parts.append(f)

    valid_files, task, num_students = check_student_pr(files_parts)

    branch_main, branch_head, repo_main, repo_head, pull_request_number = process_json(payload)

    print(json.dumps({
        "file-parts": file_added_parts,
        "files_added" : files_added,
        "files_changed" : files_changed,
        "files_changed_parts" : file_changed_parts,
        "main": branch_main,
        "head" : branch_head,
        "main-repo": repo_main,
        "head-repo": repo_head,
        "pr-num" : pull_request_number,
        "valid_files" : valid_files,
        "task" : task,
        "num_students": num_students
    })) 
    #with open('payload.json') as f:
    

    #process_json(payload)

    

if __name__ == "__main__":
    main()