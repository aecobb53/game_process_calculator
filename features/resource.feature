Feature: General Resource
    Scenario: Create Resource
        Given I clear all test data
        Given I create a project with the name "Test Project"
        Given I create a resource with the name "Test Resource" and the project name "Test Project"
         Then I should see "Test Resource" in the saved resources
#          When I capture the project id for "Test Resource" and save it to index "next"
#          Then I verify the project at index "0" has not changed

#     Scenario: Modify Resource
#         Given I clear all test data
#         Given I create a project with the name "Test Project"
#          Then I should see "Test Resource" in the saved projects
#          When I capture the project id for "Test Resource" and save it to index "next"
#          When I modify the project at index "0" name to "Test Resource 2"
#          Then I verify the project at index "0" has changed

#     Scenario: Delete Resource
#         Given I clear all test data
#         Given I create a project with the name "Test Project"
#          Then I should see "Test Resource" in the saved projects
#          When I delete the project at index "0"
#          Then I verify the project at index "0" has been deleted

#     Scenario: Export Resource
#         Given I clear all test data
#         Given I create a project with the name "Test Project"
#          Then I verify the "projects" export "matches" "example_export_projects_1.json"

#     Scenario: Import Resource
#         Given I clear all test data
#         Given I import projects from "example_import_projects.json"
#          Then I verify the "projects" export "exactly matches" "example_export_projects_2.json"

# # Feature: Bad Data Resource
# # Feature: Erroring Resource
