import sys
import json
import re
from github import Github

def process_json(payload):
    python_obj = json.loads(payload)
    # fetch main branch and repo, head branch and repo (forked)
    branch_main = python_obj['pull_request']['base']['ref']
    branch_head = python_obj['pull_request']['head']['ref']
    repo_main = python_obj['pull_request']['base']['repo']['full_name']
    repo_head = python_obj['pull_request']['head']['repo']['full_name']
    pull_request_number = python_obj['pull_request']['number']

    return branch_main, branch_head, repo_main, repo_head, pull_request_number
    
# Split added and changed files
def process_added_files(files):
    file_parts = []
    for f in files:
        file_parts.append(f.split('/'))
    return file_parts

"""
Check PR to see if it is a course contribution with a path "/contributions/ .." 
and that PR is for a valid task e.g. demo, essay etc. 
Lastly, the number of students contributed to the PR is extracted.  
"""
def check_student_pr(files, valid_tasks):
    valid = True
    valid_files = []
    task = ""
    num_students = -1
    for f in files:
        if len(f) < 4:
            valid = False
        else:
            if f[0] != 'contributions':
                valid = False
            if f[1] not in valid_tasks:
                valid = False
            else:
                task = f[1]
            if not 1 <= len(f[2].split('-')) <= 3:
                valid = False
            else:
                student_names = f[2].split('-')
                num_students = len(student_names)
        valid_files.append(valid)
        valid = True

    return valid_files, task, student_names,num_students

def group_of_three(task, num_students, valid_task_three):
    valid = True
    if num_students == 3:
        if task not in valid_task_three:
            valid = False

    return valid

def write_comment(github_token, repo_main, pull_request_number, task, num_students, valid_task_three):
    g = Github(github_token)
    Pull_request = g.get_repo(repo_main).get_pull(pull_request_number)
    label = Pull_request.get_label("GroupOfThree")
    labels = Pull_request.get_labels()

    if label in labels:
        if num_students < 3:
            Pull_request.remove_from_labels("GroupOfThree")
    else: 
        if num_students == 3:
            valid_group_of_three = group_of_three(task, num_students, valid_task_three)
            if valid_group_of_three:
                comment = "This group consists of 3 students and the task is " + task + ", which is an accepted task as long as the work is ambitious."
                create_pr_comment(Pull_request, comment)
            else:
                comment = "This group consists of 3 students and the task is " + task + ", which is unfortunately not an accepted task for 3 students. Please change the task or change your group constellation."            
                create_pr_comment(Pull_request, comment)

def create_pr_comment(Pull_request, comment):
    Pull_request.create_issue_comment(comment) 
    Pull_request.set_labels("GroupOfThree")

""" 
Process the expected input from command line:
- Guthub  token
- Payload from pull request
- List of filepaths for files added 
- List of filepaths for files changed
"""
def main():
    github_token = sys.argv[1]
    

    payload = sys.argv[2]
    files_added = re.sub('[\\\"\[\]]+', '', sys.argv[3]).split(',')
    files_changed = re.sub('[\\\"\[\]]+', '', sys.argv[4]).split(',')
    valid_tasks = sys.argv[5].split('/')
    valid_tasks_three = sys.argv[6].split('/')

    file_added_parts = process_added_files(files_added)
    file_changed_parts = process_added_files(files_changed)

    # append added files and changed files into one list.
    files_parts = file_added_parts
    for f in file_changed_parts:
        files_parts.append(f)

    branch_main, branch_head, repo_main, repo_head, pull_request_number = process_json(payload)

    valid_files, task, student_names, num_students = check_student_pr(files_parts, valid_tasks)

    
    write_comment(github_token, repo_main, pull_request_number, task, num_students, valid_tasks_three)
        
        
    print(json.dumps({
        "file_added_parts": file_added_parts,
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
        "student_names": student_names,
        "num_students": num_students
        }))


if __name__ == "__main__":
    main()