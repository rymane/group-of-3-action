# group-of-3-action, course-automation for DevOps@KTH

A Github action for the DevOps course at KTH, that looks at pull requests and checks if the number of studens is appropriate for the task. This will post a comment on the pull request with info about whether it's an acceptable group size or not. Since the course has a requirement that groups of 3 need a remarkable submission our action also adds a label to the pull request if the group has 3 students so that the TAs can take a more careful look at the proposal.

## How to use
Here is an example of how to use the action in a .yml file:
```
name: "Workflow for group-of-3-action"
on:
  pull_request_target:
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # Checkout latest version of repo
      - uses: actions/checkout@v2
        name: "Checkout"
      # Use trilom/file_changes_action to get changed and added files
      - name: "Get file changes"
        id: get_file_changes
        uses: trilom/file-changes-action@v1.2.4
      # Get Github event path and escape %, \n and \r characters
      - id: echoPayload
        run: |
          payload=$(cat $GITHUB_EVENT_PATH)
          payload="${payload//'%'/'%25'}"
          payload="${payload//$'\n'/'%0A'}"
          payload="${payload//$'\r'/'%0D'}"
          echo "::set-output name=payload::$payload"
      # Our action, validTasks and validTasksGroupThree can be changed if the course changes
      - uses: rymane/group-of-3-action/action@main
        with: 
          github-token: ${{ secrets.GITHUB_TOKEN }}
          payload: ${{ steps.echoPayload.outputs.payload}}
          filesAdded: ${{ steps.get_file_changes.outputs.files_added}}
          filesChanged: ${{ steps.get_file_changes.outputs.files_modified }}
          validTasks: course-automation/demo/essay/executable-tutorial/feedback/open-source/presentation
          validTasksGroupThree: demo/essay/open-source
```
### Inputs
- github-token - Github token that provides access for several functions, in this case writing comments.
- payload - The github event path from the pull request. This provides information about the repo, both main and head. It also provides the pull request number.
- filesAdded - The names of the files that were added in the pull request.
- filesChanged - The names of the files that were changed in the pull request.
- validTasks - the tasks available for students in the DevOps course.
- validTasksGroupThree - the tasks in the DevOps course where it is allowed to be a group of three.

**NOTE** The last 2 inputs, ```validTasks, validTasksGroupThree``` are set to 2021's group rules. If this were to change in following years this input should change to reflect that.

### Tests
The directory **contributions** is made for testing. It contains 2 additional directories, named after valid tasks in the course. To test, perform these steps:

1. Checkout a new testing branch
2. Change something in one of the test files
3. Commit and push the changes
4. Create a new pull request

This will trigger the workflow, and a comment will be written on the pull request. If the test was made on a "submission" with 3 names, a "GroupOfThree" label will also be added to the pull request.