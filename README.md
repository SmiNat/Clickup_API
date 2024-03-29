# Manual for using ClickUp API

## Introduction
To use the ClickUp API effectively, a good understanding of the CickUp Hierarchy and
URL construction is required.
For official documentation see:
- https://help.clickup.com/hc/en-us
- https://clickup.com/api/


## ClickUp Hierarchy

Official documentation:
https://help.clickup.com/hc/en-us/articles/13856392825367-Intro-to-the-Hierarchy
![Clickup Hierarchy](clickup_api_screenshots/hierarchy.png)

In practice:
![Clickup Project Hierarchy](clickup_api_screenshots/project_hierarchy.png)


## Getting credentials
### Token

![Get token - Step 1](clickup_api_screenshots/token_step_1.png)
![Get token - Step 2](clickup_api_screenshots/token_step_2.png)

https://clickup.com/api/developer-portal/authentication/


## Using credentials
### Postman

![Postman - token use](clickup_api_screenshots/token_postman.png)

### ClickUpAPI Class (OOP)
Using ClickUp API via Python class ClickUpAPI requires token as an authentication key.
There are two ways of using token credentials in ClickUpAPI class:

    1. Setting credentials (token_value) at initiating class instance (required):

        instance_name = ClickUpAPI(token=token_value)

    An instance cannot be created without a token. Validation of token credentials is
    executed at request calls made with the use of each method.
    Token used at instance initiation is a default token used in request header and
    therefore can be used to all class methods.

    2. Overriding token used for request header at each request made by selected
    instance methods (optional).

        instance_name.instance_method(token=new_token)

    User can easily change token value for each request method made through instance
    method if this method accepts token value as a parameter. If token parameter is not
    set, request will use token value used to initiate an instance.

### ClickUpAPI - FastAPI
For FastAPI methods token is set in enums.py file or in each endpoint.
Request header always uses the token given at a each request endpoint. If user does not
wish to set token for each request, token query parameter can be ommited (None value)
as long as there is a token specified in enums.py file.

To start a FastAPI based on ClickUp API use commend:
> uvicorn clickup_api_fastapi.main:app --reload


## ClickUp API main URL address
*https://app.clickup.com/api/v2*

### ClickUpAPI Class (OOP)
Basic url address for each request is set in main.py file in ClickUpAPI class.

### ClickUpAPI - FastAPI
Basic url address for each request is set in enums.py file.


## Methods based on ClickUp API

### ClickUp requests implemented in OOP / FastAPI

#### GET request                        - implemented method
- GET Authorized Teams (Workspaces)     - get_authorized_teams_workspaces
- GET Authorized User                   - get_authorized_user
- GET Teams                             - get_teams
- GET Spaces                            - get_spaces
- GET Space                             - get_space
- GET Folders                           - get_folders
- GET Folder                            - get_folder
- GET Lists                             - get_lists
- GET List                              - get_list
- GET Folderless Lists                  - get_folderless_lists
- GET Tasks                             - get_tasks
    - Note: custom_fields parameter not implemented
- GET Task                              - get_task
- GET User                              - get_user
- GET Time Entries Within a Date Range  - get_time_entries
- GET Task Comments                     - get_task_comments
- GET List Comments                     - get_list_comments
- GET Chat View Comments                - get_chat_view_comments
- GET Custom Task Types                 - get_custom_task_types
- GET Accessible Custom Fields          - get_accessible_custom_fields

#### POST/PUT request                   - implemented method
- POST Create Task                      - create_task
- PUT Update Task                       - edit_task
- POST Create Checklist                 - create_checklist
- PUT Edit Checklist                    - edit_checklist
- POST Create Checklist Item            - create_checklist_item
- PUT Edit Checklist Item               - edit_checklist_item
- POST Create Task Comment              - create_task_comment
- POST Create List Comment              - create_list_comment
- POST Create Chat View Comment         - create_chat_view_comment
- PUT Update Comment                    - update_comment
- POST Add Task Link                    - add_task_link
- POST Add Task Dependency              - add_task_dependency

#### DELETE request                     - implemented method
- DELETE Comment                        - delete_comment
- DELETE Remove Task From A List        - remove_task_from_a_list
- DELETE Task                           - delete_task
- DELETE Checklist                      - delete_checklist
- DELETE Checklist Item                 - delete_checklist_item
- DELETE Task Link                      - delete_task_link
- DELETE Dependency                     - delete_task_dependency

### New methods for using ClikUp API requests
- user_worktime
    - Returns a dictionary of usernames with their time tracked from time entries request.
    Use 'assignee' parameter to designate users based on their IDs.
    Use 'team_id' parameter to indicate workspaces from which time tracked should be obtained.
    Use 'start_date' and 'end_date' parameters to select date range in which users
    were tracking time for their tasks.
- user_tasks
    - Returns a dictionary with the user's ('assignee') tasks.
    Use 'team_id' parameter to indicate workspaces from which tasks should be obtained.
    Use 'start_date' and 'end_date' parameters to select the time at which the tasks
    were conducted.
- create_checklist_items
    - To simultaneously add many items to a single checklist.
    Use 'task_id' and 'checklist_name' to first create a new checklist and then to add
    items to it or use 'checklist_id' to add items to the existing checklist.
    Use 'checklist_items' (list) to add many items at once (each checklist item must
    contain 'name' (required) and can contain 'assignee' (optional)).
- create_task_with_checklist_and_items
    - To add a new task with new checklist with items in one request.
    Combines three post methods (create_task, create_checklist and create_checklist_item)
    in single request.


## ClickUp error messages

### Most common ClickUp errors returned while using API

    ECODE           Status  Message/meaning
    22P02           500     Invalid input syntax for type uuid: [id]
    ACCESS_083      401     Not found / You do not have access to this task.
    ACCESS_190      404     Not found.
    APP_001         404     Route not found - check if all required parameters are given.
    CHECK_012       500     Internal server error
    CHECK_028       400     Assignee must have access to checklist item - requires
                            Assignee id or None as a assignee parameter.
    COMM_003        500     Invalid syntax input for integer.
    CRTSK_001       400     Status not found.
    DEPENDS_009     400     Missing required options depends_on or dependency_of.
    GROUP_HELPERS_001  500  Invalid input syntax for type uuid. Check ID for field value.
    INPUT_002/03    400     Invalid ID.
    ITEM_155        400     Field must be a json parsable string (array of strings).
    ITEM_156        400     Field must be an array.
    ITEMV2_003      500     Internal server error - can be caused by incorrect data type or
                            incorrect value (eg. 'order by' non-existing type name or typing
                            string instead of a list or an integer).
    JSON_001        400     Unexpected token [value] in JSON at position [number] -
                            usually due to the lack of one of required body parameters or
                            invalid JSON (eg. extra comma)
    LOC_008         400     Unsupported Entity - probably caused by using token with not high
                            enough credentials. Try to use token with higher access or narrow down
                            request by using query parameters.
    OAUTH_017       400     Authorization header required - can be caused by not passing
                            token value (token as a empty string or None or no token in header)
    OAUTH_019       401     Oauth token not found - probably caused by using token with not high
                            enough credentials.
    OAUTH_023/27/   401     A team (Workspace) was not authorized by the user for a particular
    /57/61                  access token / invalid ID of a team / list / space / folder.
    OAUTH_040/      400     Parameter must be an array (list or tuple) - at least two elements
                            required (empty string as a second element can solve the issue in case
                            of filtering by only one element in list/tuple).
    OAUTH_062       401     Comment is required.
    OAUTH_064       400     View must be a conversation / invalid view ID.
    OUATH_066       404     Comment not found.
    OAUTH_095/97    400/500 Invalid input syntax for type uuid: "None" (or any other value)
                            - usually due to the lack of one of required parameters.
    PAGE_047        400     Must be a task view / invalid view ID.
    PUBAPITASK_008  400     Custom items must be an arra - also appears if list containsonly
                            one element. Add second element to solve the isssue. Second element
                            can be anything as long as it has correct data type
                            (eg. str or int depending on requirements).
    PUBAPITASK_009  400     Custom items must be an array of numbers - some of list elements are
                            of invalid type (integer required).
    SHARD_001       500     Invalid input syntax for integer / Incorrect data type
                            (usually string input instead of an integer) / Invalid ID.
    TEAM_110        403     Team must be on enterprise plan.
    TIMEENTRYM_006  401     Team not authorized - either user does not have required permissions
                            or 'team_id' (workspace) does not exist (invalid ID).
    TIMEENTRY_007   400     Invalid 'assignee' option. Check user_id.
    TIMEENTRY_059   You have no access - use token with higher access permissions.
    TIMEENTRY_062   400     Hierarchy ID should be integer - check space / list / folder id number.
    TIMEENTRY_065   Only one hierarchy ID could be provided - more than one hierarchy
                    parameter was given to narrow search area (e.g. space_id with folder_id)
                    - use only one hierarchy parameter per search.
    TIMEENTRY_072   500     Invalid input syntax for integer - check if date is in Epoch (integer).
    ... to be continued ...
