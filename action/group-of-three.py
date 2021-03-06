import sys
import json
import re
from github import Github

def process_json(payload):
    python_obj = json.loads(payload)
    # fetch main branch and pull request number
    repo_main = python_obj['pull_request']['base']['repo']['full_name']
    pull_request_number = python_obj['pull_request']['number']

    return repo_main, pull_request_number
    
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
    repo = g.get_repo(repo_main)
    Pull_request = repo.get_pull(pull_request_number)
    label = repo.get_label("GroupOfThree")
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
- Guthub token
- Payload from pull request
- List of filepaths for files added 
- List of filepaths for files changed
- Valid tasks for students to choose from
- Valid tasks for groups of 3 to choose from.
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

    repo_main, pull_request_number = process_json(payload)

    valid_files, task, student_names, num_students = check_student_pr(files_parts, valid_tasks)

    # If none of the added or changed files is a valid student submission, return nothing
    if True not in valid_files:
        return
            
    write_comment(github_token, repo_main, pull_request_number, task, num_students, valid_tasks_three)
        
        
    print(json.dumps({   
        "The students": student_names, 
        "Their task" : task,
        "The number of students": num_students
        }))


if __name__ == "__main__":
    main()