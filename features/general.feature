Feature: General

    Scenario: Create Project
        Given I clear all test data
        Given I create a project with the name "Test Project"
         Then I should see "Test Project" in the saved projects
         When I capture the project id for "Test Project" and save it to index "next"
         Then I verify the project at index "0" has not changed

#     Scenario: Modify Project
#         Given I clear all test data
#         Given I create a project with the name "Test Project"
#          Then I should see "Test Project" in the saved projects
#          When I capture the project id for "Test Project" and save it to index "next"
#          When I modify the project at index "0" name to "Test Project 2"
#          Then I verify the project at index "0" has changed

#     Scenario: Delete Project
#         Given I clear all test data
#         Given I create a project with the name "Test Project"
#          Then I should see "Test Project" in the saved projects
#          When I delete the project at index "0"
#          Then I verify the project at index "0" has been deleted
